import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from uuid import uuid4

from app.main import app
from app.database import Base, get_db
from app.models import User

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_challenge_routes.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)


@pytest.fixture(scope="function")
def setup_database():
    """Create tables before each test and drop after"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_challenge_data():
    """Sample challenge data for testing"""
    now = datetime.utcnow()
    return {
        "title": "Test Challenge",
        "description": "A test challenge description",
        "language": "python",
        "correct_solution": "print('Hello, World!')",
        "start_time": (now + timedelta(hours=1)).isoformat(),
        "end_time": (now + timedelta(hours=2)).isoformat(),
        "fragments": [
            {"content": "print('Hello", "original_order": 0},
            {"content": ", World!')", "original_order": 1}
        ],
        "test_cases": [
            {"input": "", "expected_output": "Hello, World!", "visible": True}
        ]
    }


def test_create_challenge(setup_database, sample_challenge_data):
    """Test creating a challenge"""
    response = client.post("/api/challenges", json=sample_challenge_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_challenge_data["title"]
    assert data["description"] == sample_challenge_data["description"]
    assert data["language"] == sample_challenge_data["language"]
    assert len(data["fragments"]) == 2
    assert len(data["test_cases"]) == 1
    assert "id" in data


def test_create_challenge_missing_title(setup_database, sample_challenge_data):
    """Test creating a challenge without a title"""
    del sample_challenge_data["title"]
    response = client.post("/api/challenges", json=sample_challenge_data)
    
    assert response.status_code == 400
    assert "title" in response.json()["detail"].lower()


def test_create_challenge_missing_test_cases(setup_database, sample_challenge_data):
    """Test creating a challenge without test cases"""
    sample_challenge_data["test_cases"] = []
    response = client.post("/api/challenges", json=sample_challenge_data)
    
    assert response.status_code == 400
    assert "test case" in response.json()["detail"].lower()


def test_get_challenge(setup_database, sample_challenge_data):
    """Test retrieving a challenge by ID"""
    # Create a challenge first
    create_response = client.post("/api/challenges", json=sample_challenge_data)
    challenge_id = create_response.json()["id"]
    
    # Get the challenge
    response = client.get(f"/api/challenges/{challenge_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == challenge_id
    assert data["title"] == sample_challenge_data["title"]


def test_get_nonexistent_challenge(setup_database):
    """Test retrieving a challenge that doesn't exist"""
    fake_id = str(uuid4())
    response = client.get(f"/api/challenges/{fake_id}")
    
    assert response.status_code == 404


def test_list_challenges(setup_database, sample_challenge_data):
    """Test listing all challenges"""
    # Create two challenges
    client.post("/api/challenges", json=sample_challenge_data)
    
    sample_challenge_data["title"] = "Second Challenge"
    client.post("/api/challenges", json=sample_challenge_data)
    
    # List challenges
    response = client.get("/api/challenges")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_update_challenge(setup_database, sample_challenge_data):
    """Test updating a challenge"""
    # Create a challenge first
    create_response = client.post("/api/challenges", json=sample_challenge_data)
    challenge_id = create_response.json()["id"]
    
    # Update the challenge
    update_data = {"title": "Updated Title", "description": "Updated description"}
    response = client.put(f"/api/challenges/{challenge_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated description"
    assert data["language"] == sample_challenge_data["language"]  # Unchanged


def test_update_nonexistent_challenge(setup_database):
    """Test updating a challenge that doesn't exist"""
    fake_id = str(uuid4())
    update_data = {"title": "Updated Title"}
    response = client.put(f"/api/challenges/{fake_id}", json=update_data)
    
    assert response.status_code == 404


def test_delete_challenge(setup_database, sample_challenge_data):
    """Test deleting a challenge"""
    # Create a challenge first
    create_response = client.post("/api/challenges", json=sample_challenge_data)
    challenge_id = create_response.json()["id"]
    
    # Delete the challenge
    response = client.delete(f"/api/challenges/{challenge_id}")
    
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/api/challenges/{challenge_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_challenge(setup_database):
    """Test deleting a challenge that doesn't exist"""
    fake_id = str(uuid4())
    response = client.delete(f"/api/challenges/{fake_id}")
    
    assert response.status_code == 404


def test_create_challenge_invalid_time_range(setup_database, sample_challenge_data):
    """Test creating a challenge with start time after end time"""
    now = datetime.utcnow()
    sample_challenge_data["start_time"] = (now + timedelta(hours=2)).isoformat()
    sample_challenge_data["end_time"] = (now + timedelta(hours=1)).isoformat()
    
    response = client.post("/api/challenges", json=sample_challenge_data)
    
    assert response.status_code == 400
    assert "time" in response.json()["detail"].lower()
