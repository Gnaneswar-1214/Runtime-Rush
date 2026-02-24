"""
Tests for submission API routes.
"""
import pytest
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.models.challenge import Challenge
from app.models.code_fragment import CodeFragment
from app.models.test_case import TestCase


# Test database setup
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_submission_routes.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="function")
def setup_database():
    """Create tables before each test and drop after"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(setup_database):
    """Provide a database session for tests"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    user = User(
        id=uuid4(),
        username="testuser",
        email="test@example.com",
        role="participant"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_challenge(db_session, test_user):
    """Create a test challenge"""
    now = datetime.now(timezone.utc)
    challenge = Challenge(
        id=uuid4(),
        title="Test Challenge",
        description="A test challenge",
        language="python",
        correct_solution="print('hello')",
        start_time=now - timedelta(hours=1),
        end_time=now + timedelta(hours=1),
        created_by=test_user.id
    )
    db_session.add(challenge)
    
    # Add test case
    test_case = TestCase(
        id=uuid4(),
        challenge_id=challenge.id,
        input="",
        expected_output="hello",
        visible=True
    )
    db_session.add(test_case)
    
    db_session.commit()
    db_session.refresh(challenge)
    return challenge


@pytest.fixture
def ended_challenge(db_session, test_user):
    """Create an ended challenge"""
    now = datetime.now(timezone.utc)
    challenge = Challenge(
        id=uuid4(),
        title="Ended Challenge",
        description="An ended challenge",
        language="python",
        correct_solution="print('test')",
        start_time=now - timedelta(hours=2),
        end_time=now - timedelta(hours=1),
        created_by=test_user.id
    )
    db_session.add(challenge)
    db_session.commit()
    db_session.refresh(challenge)
    return challenge


def test_submit_code_success(test_challenge, test_user):
    """Test successful code submission"""
    response = client.post(
        f"/api/challenges/{test_challenge.id}/submit",
        json={
            "code": "print('hello')",
            "participant_id": str(test_user.id)
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["challenge_id"] == str(test_challenge.id)
    assert data["participant_id"] == str(test_user.id)
    assert data["code"] == "print('hello')"
    assert "timestamp" in data
    assert "is_correct" in data
    assert "validation_result" in data


def test_submit_code_challenge_not_found(test_user):
    """Test submission to non-existent challenge"""
    fake_id = uuid4()
    response = client.post(
        f"/api/challenges/{fake_id}/submit",
        json={
            "code": "print('test')",
            "participant_id": str(test_user.id)
        }
    )
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_submit_code_challenge_ended(ended_challenge, test_user):
    """Test submission to ended challenge is rejected"""
    response = client.post(
        f"/api/challenges/{ended_challenge.id}/submit",
        json={
            "code": "print('test')",
            "participant_id": str(test_user.id)
        }
    )
    
    assert response.status_code == 403
    assert "ended" in response.json()["detail"].lower()


def test_get_submission_success(test_challenge, test_user):
    """Test retrieving a submission by ID"""
    # First create a submission
    submit_response = client.post(
        f"/api/challenges/{test_challenge.id}/submit",
        json={
            "code": "print('hello')",
            "participant_id": str(test_user.id)
        }
    )
    submission_id = submit_response.json()["id"]
    
    # Now retrieve it
    response = client.get(f"/api/submissions/{submission_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == submission_id
    assert data["code"] == "print('hello')"


def test_get_submission_not_found():
    """Test retrieving non-existent submission"""
    fake_id = uuid4()
    response = client.get(f"/api/submissions/{fake_id}")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_challenge_submissions(test_challenge, test_user):
    """Test retrieving all submissions for a challenge"""
    # Create multiple submissions
    for i in range(3):
        client.post(
            f"/api/challenges/{test_challenge.id}/submit",
            json={
                "code": f"print('test{i}')",
                "participant_id": str(test_user.id)
            }
        )
    
    # Retrieve all submissions
    response = client.get(f"/api/challenges/{test_challenge.id}/submissions")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all(sub["challenge_id"] == str(test_challenge.id) for sub in data)


def test_get_challenge_submissions_empty(test_challenge):
    """Test retrieving submissions for challenge with no submissions"""
    response = client.get(f"/api/challenges/{test_challenge.id}/submissions")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_get_participant_submissions(test_challenge, test_user):
    """Test retrieving all submissions by a participant for a challenge"""
    # Create multiple submissions
    for i in range(2):
        client.post(
            f"/api/challenges/{test_challenge.id}/submit",
            json={
                "code": f"print('test{i}')",
                "participant_id": str(test_user.id)
            }
        )
    
    # Retrieve participant submissions
    response = client.get(
        f"/api/participants/{test_user.id}/submissions",
        params={"challenge_id": str(test_challenge.id)}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(sub["participant_id"] == str(test_user.id) for sub in data)
    assert all(sub["challenge_id"] == str(test_challenge.id) for sub in data)


def test_get_participant_submissions_empty(test_challenge, test_user):
    """Test retrieving submissions for participant with no submissions"""
    response = client.get(
        f"/api/participants/{test_user.id}/submissions",
        params={"challenge_id": str(test_challenge.id)}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_multiple_submissions_allowed(test_challenge, test_user):
    """Test that multiple submissions from same participant are allowed"""
    # Submit twice
    response1 = client.post(
        f"/api/challenges/{test_challenge.id}/submit",
        json={
            "code": "print('first')",
            "participant_id": str(test_user.id)
        }
    )
    
    response2 = client.post(
        f"/api/challenges/{test_challenge.id}/submit",
        json={
            "code": "print('second')",
            "participant_id": str(test_user.id)
        }
    )
    
    assert response1.status_code == 201
    assert response2.status_code == 201
    assert response1.json()["id"] != response2.json()["id"]


def test_submission_timestamp_recorded(test_challenge, test_user):
    """Test that submission timestamp is recorded"""
    before = datetime.now(timezone.utc)
    
    response = client.post(
        f"/api/challenges/{test_challenge.id}/submit",
        json={
            "code": "print('test')",
            "participant_id": str(test_user.id)
        }
    )
    
    after = datetime.now(timezone.utc)
    
    assert response.status_code == 201
    timestamp_str = response.json()["timestamp"]
    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    
    # Timestamp should be between before and after
    assert before <= timestamp <= after
