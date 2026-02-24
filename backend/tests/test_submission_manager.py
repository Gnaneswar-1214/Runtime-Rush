import pytest
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from app.managers.submission_manager import SubmissionManager, SubmissionError
from app.managers.challenge_manager import ChallengeManager
from app.models import User, Challenge, Submission


@pytest.fixture
def submission_manager(db_session):
    """Create a SubmissionManager instance with a test database session"""
    return SubmissionManager(db_session)


@pytest.fixture
def challenge_manager(db_session):
    """Create a ChallengeManager instance with a test database session"""
    return ChallengeManager(db_session)


@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    user = User(
        username="testuser",
        email="test@example.com",
        role="participant"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_organizer(db_session):
    """Create a test organizer"""
    organizer = User(
        username="organizer",
        email="organizer@example.com",
        role="organizer"
    )
    db_session.add(organizer)
    db_session.commit()
    db_session.refresh(organizer)
    return organizer


@pytest.fixture
def active_challenge(challenge_manager, test_organizer):
    """Create an active challenge (started, not ended)"""
    now = datetime.now(timezone.utc)
    challenge_data = {
        "title": "Active Challenge",
        "description": "A challenge that is currently active",
        "language": "python",
        "correct_solution": "print('Hello, World!')",
        "start_time": now - timedelta(hours=1),
        "end_time": now + timedelta(hours=1),
        "created_by": test_organizer.id,
        "fragments": [
            {"content": "print('Hello, ", "original_order": 0},
            {"content": "World!')", "original_order": 1}
        ],
        "test_cases": [
            {"input": "", "expected_output": "Hello, World!", "visible": True}
        ]
    }
    return challenge_manager.create_challenge(challenge_data)


@pytest.fixture
def ended_challenge(challenge_manager, test_organizer):
    """Create an ended challenge"""
    now = datetime.now(timezone.utc)
    challenge_data = {
        "title": "Ended Challenge",
        "description": "A challenge that has ended",
        "language": "python",
        "correct_solution": "print('Goodbye')",
        "start_time": now - timedelta(hours=2),
        "end_time": now - timedelta(hours=1),
        "created_by": test_organizer.id,
        "fragments": [
            {"content": "print('Goodbye')", "original_order": 0}
        ],
        "test_cases": [
            {"input": "", "expected_output": "Goodbye", "visible": True}
        ]
    }
    return challenge_manager.create_challenge(challenge_data)


class TestSubmitCode:
    """Tests for the submit_code method"""
    
    def test_submit_code_creates_submission(self, submission_manager, active_challenge, test_user):
        """Test that submitting code creates a submission record"""
        code = "print('Hello, World!')"
        
        submission = submission_manager.submit_code(
            challenge_id=active_challenge.id,
            participant_id=test_user.id,
            code=code
        )
        
        assert submission is not None
        assert submission.id is not None
        assert submission.challenge_id == active_challenge.id
        assert submission.participant_id == test_user.id
        assert submission.code == code
        assert submission.timestamp is not None
        assert isinstance(submission.timestamp, datetime)
    
    def test_submit_code_uses_server_timestamp(self, submission_manager, active_challenge, test_user):
        """Test that submission timestamp is set by the server"""
        before_submit = datetime.now(timezone.utc)
        
        submission = submission_manager.submit_code(
            challenge_id=active_challenge.id,
            participant_id=test_user.id,
            code="print('test')"
        )
        
        after_submit = datetime.now(timezone.utc)
        
        # Timestamp should be between before and after
        assert before_submit <= submission.timestamp <= after_submit
    
    def test_submit_code_includes_validation_result(self, submission_manager, active_challenge, test_user):
        """Test that submission includes validation result"""
        submission = submission_manager.submit_code(
            challenge_id=active_challenge.id,
            participant_id=test_user.id,
            code="print('test')"
        )
        
        assert submission.validation_result is not None
        assert isinstance(submission.validation_result, dict)
        assert "isValid" in submission.validation_result
        assert "testResults" in submission.validation_result
    
    def test_submit_code_sets_is_correct_flag(self, submission_manager, active_challenge, test_user):
        """Test that submission has is_correct flag based on validation"""
        submission = submission_manager.submit_code(
            challenge_id=active_challenge.id,
            participant_id=test_user.id,
            code="print('test')"
        )
        
        assert isinstance(submission.is_correct, bool)
    
    def test_submit_code_rejects_after_challenge_end(self, submission_manager, ended_challenge, test_user):
        """Test that submissions are rejected after challenge end time"""
        with pytest.raises(SubmissionError) as exc_info:
            submission_manager.submit_code(
                challenge_id=ended_challenge.id,
                participant_id=test_user.id,
                code="print('too late')"
            )
        
        assert "ended" in str(exc_info.value).lower()
    
    def test_submit_code_rejects_nonexistent_challenge(self, submission_manager, test_user):
        """Test that submitting to a non-existent challenge raises an error"""
        fake_challenge_id = uuid4()
        
        with pytest.raises(SubmissionError) as exc_info:
            submission_manager.submit_code(
                challenge_id=fake_challenge_id,
                participant_id=test_user.id,
                code="print('test')"
            )
        
        assert "not found" in str(exc_info.value).lower()
    
    def test_multiple_submissions_allowed(self, submission_manager, active_challenge, test_user):
        """Test that a participant can submit multiple times"""
        submission1 = submission_manager.submit_code(
            challenge_id=active_challenge.id,
            participant_id=test_user.id,
            code="print('first')"
        )
        
        submission2 = submission_manager.submit_code(
            challenge_id=active_challenge.id,
            participant_id=test_user.id,
            code="print('second')"
        )
        
        assert submission1.id != submission2.id
        assert submission1.code != submission2.code
        assert submission1.timestamp <= submission2.timestamp


class TestGetSubmission:
    """Tests for the get_submission method"""
    
    def test_get_submission_returns_submission(self, submission_manager, active_challenge, test_user):
        """Test that get_submission retrieves a submission by ID"""
        submission = submission_manager.submit_code(
            challenge_id=active_challenge.id,
            participant_id=test_user.id,
            code="print('test')"
        )
        
        retrieved = submission_manager.get_submission(submission.id)
        
        assert retrieved is not None
        assert retrieved.id == submission.id
        assert retrieved.code == submission.code
        assert retrieved.challenge_id == submission.challenge_id
        assert retrieved.participant_id == submission.participant_id
    
    def test_get_submission_returns_none_for_nonexistent(self, submission_manager):
        """Test that get_submission returns None for non-existent ID"""
        fake_id = uuid4()
        result = submission_manager.get_submission(fake_id)
        assert result is None


class TestGetSubmissionsByParticipant:
    """Tests for the get_submissions_by_participant method"""
    
    def test_get_submissions_by_participant_returns_all_submissions(
        self, submission_manager, active_challenge, test_user
    ):
        """Test that get_submissions_by_participant returns all submissions for a participant"""
        # Create multiple submissions
        submission1 = submission_manager.submit_code(
            challenge_id=active_challenge.id,
            participant_id=test_user.id,
            code="print('first')"
        )
        
        submission2 = submission_manager.submit_code(
            challenge_id=active_challenge.id,
            participant_id=test_user.id,
            code="print('second')"
        )
        
        submissions = submission_manager.get_submissions_by_participant(
            participant_id=test_user.id,
            challenge_id=active_challenge.id
        )
        
        assert len(submissions) == 2
        submission_ids = [s.id for s in submissions]
        assert submission1.id in submission_ids
        assert submission2.id in submission_ids
    
    def test_get_submissions_by_participant_orders_by_timestamp_desc(
        self, submission_manager, active_challenge, test_user
    ):
        """Test that submissions are ordered by timestamp (newest first)"""
        submission1 = submission_manager.submit_code(
            challenge_id=active_challenge.id,
            participant_id=test_user.id,
            code="print('first')"
        )
        
        submission2 = submission_manager.submit_code(
            challenge_id=active_challenge.id,
            participant_id=test_user.id,
            code="print('second')"
        )
        
        submissions = submission_manager.get_submissions_by_participant(
            participant_id=test_user.id,
            challenge_id=active_challenge.id
        )
        
        # Newest should be first
        assert submissions[0].id == submission2.id
        assert submissions[1].id == submission1.id
    
    def test_get_submissions_by_participant_filters_by_challenge(
        self, submission_manager, challenge_manager, test_user, test_organizer
    ):
        """Test that submissions are filtered by challenge"""
        now = datetime.now(timezone.utc)
        
        # Create two challenges
        challenge1_data = {
            "title": "Challenge 1",
            "description": "First challenge",
            "language": "python",
            "correct_solution": "print('1')",
            "start_time": now - timedelta(hours=1),
            "end_time": now + timedelta(hours=1),
            "created_by": test_organizer.id,
            "fragments": [{"content": "print('1')", "original_order": 0}],
            "test_cases": [{"input": "", "expected_output": "1", "visible": True}]
        }
        challenge1 = challenge_manager.create_challenge(challenge1_data)
        
        challenge2_data = {
            "title": "Challenge 2",
            "description": "Second challenge",
            "language": "python",
            "correct_solution": "print('2')",
            "start_time": now - timedelta(hours=1),
            "end_time": now + timedelta(hours=1),
            "created_by": test_organizer.id,
            "fragments": [{"content": "print('2')", "original_order": 0}],
            "test_cases": [{"input": "", "expected_output": "2", "visible": True}]
        }
        challenge2 = challenge_manager.create_challenge(challenge2_data)
        
        # Submit to both challenges
        submission_manager.submit_code(
            challenge_id=challenge1.id,
            participant_id=test_user.id,
            code="print('1')"
        )
        
        submission_manager.submit_code(
            challenge_id=challenge2.id,
            participant_id=test_user.id,
            code="print('2')"
        )
        
        # Get submissions for challenge 1 only
        submissions = submission_manager.get_submissions_by_participant(
            participant_id=test_user.id,
            challenge_id=challenge1.id
        )
        
        assert len(submissions) == 1
        assert submissions[0].challenge_id == challenge1.id
    
    def test_get_submissions_by_participant_returns_empty_for_no_submissions(
        self, submission_manager, active_challenge, test_user
    ):
        """Test that empty list is returned when participant has no submissions"""
        submissions = submission_manager.get_submissions_by_participant(
            participant_id=test_user.id,
            challenge_id=active_challenge.id
        )
        
        assert submissions == []


class TestGetSubmissionsByChallenge:
    """Tests for the get_submissions_by_challenge method"""
    
    def test_get_submissions_by_challenge_returns_all_submissions(
        self, submission_manager, active_challenge, test_user, db_session
    ):
        """Test that get_submissions_by_challenge returns all submissions for a challenge"""
        # Create another user
        user2 = User(username="user2", email="user2@example.com", role="participant")
        db_session.add(user2)
        db_session.commit()
        db_session.refresh(user2)
        
        # Create submissions from different users
        submission1 = submission_manager.submit_code(
            challenge_id=active_challenge.id,
            participant_id=test_user.id,
            code="print('user1')"
        )
        
        submission2 = submission_manager.submit_code(
            challenge_id=active_challenge.id,
            participant_id=user2.id,
            code="print('user2')"
        )
        
        submissions = submission_manager.get_submissions_by_challenge(active_challenge.id)
        
        assert len(submissions) == 2
        submission_ids = [s.id for s in submissions]
        assert submission1.id in submission_ids
        assert submission2.id in submission_ids
    
    def test_get_submissions_by_challenge_orders_by_timestamp_asc(
        self, submission_manager, active_challenge, test_user
    ):
        """Test that submissions are ordered by timestamp (oldest first)"""
        submission1 = submission_manager.submit_code(
            challenge_id=active_challenge.id,
            participant_id=test_user.id,
            code="print('first')"
        )
        
        submission2 = submission_manager.submit_code(
            challenge_id=active_challenge.id,
            participant_id=test_user.id,
            code="print('second')"
        )
        
        submissions = submission_manager.get_submissions_by_challenge(active_challenge.id)
        
        # Oldest should be first
        assert submissions[0].id == submission1.id
        assert submissions[1].id == submission2.id
    
    def test_get_submissions_by_challenge_returns_empty_for_no_submissions(
        self, submission_manager, active_challenge
    ):
        """Test that empty list is returned when challenge has no submissions"""
        submissions = submission_manager.get_submissions_by_challenge(active_challenge.id)
        assert submissions == []
