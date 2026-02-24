"""
Property-based tests for session data persistence.

Feature: runtime-rush-platform
"""
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from datetime import datetime, timedelta, timezone
from app.models.session import ParticipantSession
from app.models.challenge import Challenge, TestCase
from app.models.user import User
import uuid


# Hypothesis strategies for generating test data
@st.composite
def session_data_strategy(draw):
    """Generate valid session data as a dictionary."""
    # Generate unique identifiers using UUID to avoid constraint violations
    unique_id = str(uuid.uuid4())[:8]
    
    # Generate code text without NUL characters (0x00) and surrogate characters which PostgreSQL doesn't accept
    code_text = draw(st.text(
        min_size=1, 
        max_size=5000,
        alphabet=st.characters(
            blacklist_characters='\x00',
            blacklist_categories=('Cs',)  # Exclude surrogate characters
        )
    ))
    
    return {
        'current_code': code_text,
        'unique_id': unique_id
    }


# Property 5: Session Code Round-Trip Persistence
# **Validates: Requirements 3.4, 10.2**
class TestSessionRoundTripPersistence:
    """Property-based tests for session persistence."""
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(session_data_strategy())
    def test_session_code_round_trip_persistence(self, db_session, session_data):
        """
        Property 5: Session Code Round-Trip Persistence
        
        For any participant session with code content, saving the session and then 
        retrieving it should return the same code content.
        
        **Validates: Requirements 3.4, 10.2**
        """
        unique_id = session_data['unique_id']
        
        # Create a user (organizer) for the challenge
        organizer = User(
            username=f"org_{unique_id}",
            email=f"org_{unique_id}@test.com",
            role="organizer"
        )
        db_session.add(organizer)
        db_session.commit()
        
        # Create a user (participant) for the session
        participant = User(
            username=f"part_{unique_id}",
            email=f"part_{unique_id}@test.com",
            role="participant"
        )
        db_session.add(participant)
        db_session.commit()
        
        # Create a challenge
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
        
        # Add at least one test case (required for validation)
        test_case = TestCase(
            input="",
            expected_output="hello",
            visible=True
        )
        challenge.test_cases.append(test_case)
        
        db_session.add(challenge)
        db_session.commit()
        
        # Record the time before creating the session
        time_before = datetime.now(timezone.utc)
        
        # Create the participant session
        session = ParticipantSession(
            participant_id=participant.id,
            challenge_id=challenge.id,
            current_code=session_data['current_code']
        )
        
        db_session.add(session)
        db_session.commit()
        
        # Record the time after creating the session
        time_after = datetime.now(timezone.utc)
        
        # Clear the session to ensure we're fetching from the database
        db_session.expire_all()
        
        # Retrieve the session
        retrieved = db_session.query(ParticipantSession).filter(
            ParticipantSession.participant_id == participant.id,
            ParticipantSession.challenge_id == challenge.id
        ).first()
        
        # Verify all data is intact
        assert retrieved is not None, "Session should be retrievable"
        assert retrieved.current_code == session_data['current_code'], "Code content should match exactly"
        assert retrieved.participant_id == participant.id, "Participant ID should match"
        assert retrieved.challenge_id == challenge.id, "Challenge ID should match"
        
        # Verify last_saved timestamp was recorded
        assert retrieved.last_saved is not None, "Last saved timestamp should be set"
        # Timestamp should be between before and after times (with some tolerance)
        assert time_before <= retrieved.last_saved <= time_after + timedelta(seconds=1), \
            "Last saved timestamp should be set by server during creation"
