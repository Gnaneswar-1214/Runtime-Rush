"""
Unit tests for SessionManager class.

Feature: runtime-rush-platform
"""
import pytest
from datetime import datetime, timedelta, timezone
from app.managers.session_manager import SessionManager
from app.models import User, Challenge, TestCase, ParticipantSession
import uuid


@pytest.fixture
def session_manager(db_session):
    """Create a SessionManager instance with a test database session."""
    return SessionManager(db_session)


@pytest.fixture
def test_participant(db_session):
    """Create a test participant user."""
    unique_id = str(uuid.uuid4())[:8]
    participant = User(
        username=f"participant_{unique_id}",
        email=f"participant_{unique_id}@test.com",
        role="participant"
    )
    db_session.add(participant)
    db_session.commit()
    return participant


@pytest.fixture
def test_challenge(db_session):
    """Create a test challenge."""
    unique_id = str(uuid.uuid4())[:8]
    organizer = User(
        username=f"organizer_{unique_id}",
        email=f"organizer_{unique_id}@test.com",
        role="organizer"
    )
    db_session.add(organizer)
    db_session.commit()
    
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(hours=2)
    challenge = Challenge(
        title=f"Challenge_{unique_id}",
        description="Test challenge",
        language="python",
        correct_solution="print('hello')",
        start_time=start_time,
        end_time=end_time,
        created_by=organizer.id
    )
    
    # Add required test case
    test_case = TestCase(
        input="",
        expected_output="hello",
        visible=True
    )
    challenge.test_cases.append(test_case)
    
    db_session.add(challenge)
    db_session.commit()
    return challenge


class TestSessionManager:
    """Unit tests for SessionManager functionality."""
    
    def test_save_session_creates_new_session(self, session_manager, test_participant, test_challenge):
        """Test that save_session creates a new session when none exists."""
        code = "print('Hello, World!')"
        
        # Save the session
        session = session_manager.save_session(
            participant_id=test_participant.id,
            challenge_id=test_challenge.id,
            current_code=code
        )
        
        # Verify session was created
        assert session is not None
        assert session.participant_id == test_participant.id
        assert session.challenge_id == test_challenge.id
        assert session.current_code == code
        assert session.last_saved is not None
    
    def test_save_session_updates_existing_session(self, session_manager, test_participant, test_challenge, db_session):
        """Test that save_session updates an existing session (upsert behavior)."""
        # Create initial session
        initial_code = "print('first version')"
        session1 = session_manager.save_session(
            participant_id=test_participant.id,
            challenge_id=test_challenge.id,
            current_code=initial_code
        )
        initial_timestamp = session1.last_saved
        
        # Update the session with new code
        updated_code = "print('second version')"
        session2 = session_manager.save_session(
            participant_id=test_participant.id,
            challenge_id=test_challenge.id,
            current_code=updated_code
        )
        
        # Verify session was updated, not duplicated
        assert session2.participant_id == test_participant.id
        assert session2.challenge_id == test_challenge.id
        assert session2.current_code == updated_code
        assert session2.last_saved >= initial_timestamp
        
        # Verify only one session exists in database
        all_sessions = db_session.query(ParticipantSession).filter(
            ParticipantSession.participant_id == test_participant.id,
            ParticipantSession.challenge_id == test_challenge.id
        ).all()
        assert len(all_sessions) == 1
    
    def test_get_session_returns_existing_session(self, session_manager, test_participant, test_challenge):
        """Test that get_session retrieves an existing session."""
        code = "print('test code')"
        
        # Save a session
        saved_session = session_manager.save_session(
            participant_id=test_participant.id,
            challenge_id=test_challenge.id,
            current_code=code
        )
        
        # Retrieve the session
        retrieved_session = session_manager.get_session(
            participant_id=test_participant.id,
            challenge_id=test_challenge.id
        )
        
        # Verify retrieved session matches saved session
        assert retrieved_session is not None
        assert retrieved_session.participant_id == saved_session.participant_id
        assert retrieved_session.challenge_id == saved_session.challenge_id
        assert retrieved_session.current_code == saved_session.current_code
    
    def test_get_session_returns_none_when_not_found(self, session_manager):
        """Test that get_session returns None when session doesn't exist."""
        # Try to get a non-existent session
        session = session_manager.get_session(
            participant_id=uuid.uuid4(),
            challenge_id=uuid.uuid4()
        )
        
        assert session is None
    
    def test_auto_save_creates_session(self, session_manager, test_participant, test_challenge):
        """Test that auto_save creates a new session."""
        code = "print('auto-saved code')"
        
        # Auto-save the session
        session = session_manager.auto_save(
            participant_id=test_participant.id,
            challenge_id=test_challenge.id,
            code=code
        )
        
        # Verify session was created
        assert session is not None
        assert session.current_code == code
    
    def test_auto_save_updates_existing_session(self, session_manager, test_participant, test_challenge):
        """Test that auto_save updates an existing session."""
        # Create initial session
        initial_code = "print('initial')"
        session_manager.save_session(
            participant_id=test_participant.id,
            challenge_id=test_challenge.id,
            current_code=initial_code
        )
        
        # Auto-save with new code
        updated_code = "print('auto-saved update')"
        session = session_manager.auto_save(
            participant_id=test_participant.id,
            challenge_id=test_challenge.id,
            code=updated_code
        )
        
        # Verify session was updated
        assert session.current_code == updated_code
    
    def test_session_isolation_different_participants(self, session_manager, test_challenge, db_session):
        """Test that sessions are isolated between different participants."""
        # Create two participants
        unique_id1 = str(uuid.uuid4())[:8]
        participant1 = User(
            username=f"participant1_{unique_id1}",
            email=f"participant1_{unique_id1}@test.com",
            role="participant"
        )
        db_session.add(participant1)
        
        unique_id2 = str(uuid.uuid4())[:8]
        participant2 = User(
            username=f"participant2_{unique_id2}",
            email=f"participant2_{unique_id2}@test.com",
            role="participant"
        )
        db_session.add(participant2)
        db_session.commit()
        
        # Save sessions for both participants
        code1 = "print('participant 1 code')"
        code2 = "print('participant 2 code')"
        
        session_manager.save_session(participant1.id, test_challenge.id, code1)
        session_manager.save_session(participant2.id, test_challenge.id, code2)
        
        # Retrieve sessions
        retrieved1 = session_manager.get_session(participant1.id, test_challenge.id)
        retrieved2 = session_manager.get_session(participant2.id, test_challenge.id)
        
        # Verify sessions are isolated
        assert retrieved1.current_code == code1
        assert retrieved2.current_code == code2
        assert retrieved1.current_code != retrieved2.current_code
    
    def test_session_isolation_different_challenges(self, session_manager, test_participant, db_session):
        """Test that sessions are isolated between different challenges."""
        # Create two challenges
        unique_id1 = str(uuid.uuid4())[:8]
        organizer = User(
            username=f"organizer_{unique_id1}",
            email=f"organizer_{unique_id1}@test.com",
            role="organizer"
        )
        db_session.add(organizer)
        db_session.commit()
        
        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(hours=2)
        
        challenge1 = Challenge(
            title=f"Challenge1_{unique_id1}",
            description="Test challenge 1",
            language="python",
            correct_solution="print('hello')",
            start_time=start_time,
            end_time=end_time,
            created_by=organizer.id
        )
        test_case1 = TestCase(input="", expected_output="hello", visible=True)
        challenge1.test_cases.append(test_case1)
        db_session.add(challenge1)
        
        challenge2 = Challenge(
            title=f"Challenge2_{unique_id1}",
            description="Test challenge 2",
            language="python",
            correct_solution="print('world')",
            start_time=start_time,
            end_time=end_time,
            created_by=organizer.id
        )
        test_case2 = TestCase(input="", expected_output="world", visible=True)
        challenge2.test_cases.append(test_case2)
        db_session.add(challenge2)
        db_session.commit()
        
        # Save sessions for both challenges
        code1 = "print('challenge 1 code')"
        code2 = "print('challenge 2 code')"
        
        session_manager.save_session(test_participant.id, challenge1.id, code1)
        session_manager.save_session(test_participant.id, challenge2.id, code2)
        
        # Retrieve sessions
        retrieved1 = session_manager.get_session(test_participant.id, challenge1.id)
        retrieved2 = session_manager.get_session(test_participant.id, challenge2.id)
        
        # Verify sessions are isolated
        assert retrieved1.current_code == code1
        assert retrieved2.current_code == code2
        assert retrieved1.current_code != retrieved2.current_code
    
    def test_session_persists_after_challenge_end(self, session_manager, test_participant, db_session):
        """Test that session data persists even after challenge ends."""
        # Create a challenge that has already ended
        unique_id = str(uuid.uuid4())[:8]
        organizer = User(
            username=f"organizer_{unique_id}",
            email=f"organizer_{unique_id}@test.com",
            role="organizer"
        )
        db_session.add(organizer)
        db_session.commit()
        
        # Challenge that ended 1 hour ago
        end_time = datetime.now(timezone.utc) - timedelta(hours=1)
        start_time = end_time - timedelta(hours=2)
        
        ended_challenge = Challenge(
            title=f"EndedChallenge_{unique_id}",
            description="Ended challenge",
            language="python",
            correct_solution="print('test')",
            start_time=start_time,
            end_time=end_time,
            created_by=organizer.id
        )
        test_case = TestCase(input="", expected_output="test", visible=True)
        ended_challenge.test_cases.append(test_case)
        db_session.add(ended_challenge)
        db_session.commit()
        
        # Save a session for the ended challenge
        code = "print('code from ended challenge')"
        session_manager.save_session(test_participant.id, ended_challenge.id, code)
        
        # Retrieve the session
        retrieved = session_manager.get_session(test_participant.id, ended_challenge.id)
        
        # Verify session persists even after challenge end
        assert retrieved is not None
        assert retrieved.current_code == code
    
    def test_save_session_with_empty_code(self, session_manager, test_participant, test_challenge):
        """Test that save_session handles empty code strings."""
        empty_code = ""
        
        # Save session with empty code
        session = session_manager.save_session(
            participant_id=test_participant.id,
            challenge_id=test_challenge.id,
            current_code=empty_code
        )
        
        # Verify session was created with empty code
        assert session is not None
        assert session.current_code == ""
    
    def test_save_session_with_large_code(self, session_manager, test_participant, test_challenge):
        """Test that save_session handles large code strings."""
        # Create a large code string (10KB)
        large_code = "# " + "x" * 10000
        
        # Save session with large code
        session = session_manager.save_session(
            participant_id=test_participant.id,
            challenge_id=test_challenge.id,
            current_code=large_code
        )
        
        # Verify session was created with large code
        assert session is not None
        assert session.current_code == large_code
        assert len(session.current_code) > 10000
