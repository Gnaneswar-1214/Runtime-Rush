"""
Property-based tests for submission data persistence.

Feature: runtime-rush-platform
"""
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from datetime import datetime, timedelta, timezone
from app.models.submission import Submission
from app.models.challenge import Challenge, TestCase
from app.models.user import User
import uuid


# Hypothesis strategies for generating test data
@st.composite
def submission_data_strategy(draw):
    """Generate valid submission data as a dictionary."""
    # Generate unique identifiers using UUID to avoid constraint violations
    unique_id = str(uuid.uuid4())[:8]
    
    # Generate text without NUL characters (0x00) which PostgreSQL doesn't accept
    code_text = draw(st.text(
        min_size=1, 
        max_size=1000,
        alphabet=st.characters(blacklist_characters='\x00')
    ))
    
    return {
        'code': code_text,
        'is_correct': draw(st.booleans()),
        'validation_result': {
            'isValid': draw(st.booleans()),
            'syntaxErrors': [],
            'testResults': [],
            'allTestsPassed': draw(st.booleans())
        },
        'unique_id': unique_id
    }


# Property 15: Submission Round-Trip Persistence
# **Validates: Requirements 6.1, 6.2, 6.3, 6.4**
class TestSubmissionRoundTripPersistence:
    """Property-based tests for submission persistence."""
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(submission_data_strategy())
    def test_submission_data_round_trip_persistence(self, db_session, submission_data):
        """
        Property 15: Submission Round-Trip Persistence
        
        For any submission with code, participant ID, and challenge ID, creating 
        the submission should store it with a server timestamp, and retrieving it 
        should return the same code, participant ID, challenge ID, and timestamp.
        
        **Validates: Requirements 6.1, 6.2, 6.3, 6.4**
        """
        unique_id = submission_data['unique_id']
        
        # Create a user (organizer) for the challenge
        organizer = User(
            username=f"org_{unique_id}",
            email=f"org_{unique_id}@test.com",
            role="organizer"
        )
        db_session.add(organizer)
        db_session.commit()
        
        # Create a user (participant) for the submission
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
        
        # Record the time before creating the submission
        time_before = datetime.now(timezone.utc)
        
        # Create the submission
        submission = Submission(
            challenge_id=challenge.id,
            participant_id=participant.id,
            code=submission_data['code'],
            is_correct=submission_data['is_correct'],
            validation_result=submission_data['validation_result']
        )
        
        db_session.add(submission)
        db_session.commit()
        submission_id = submission.id
        
        # Record the time after creating the submission
        time_after = datetime.now(timezone.utc)
        
        # Clear the session to ensure we're fetching from the database
        db_session.expire_all()
        
        # Retrieve the submission
        retrieved = db_session.query(Submission).filter(Submission.id == submission_id).first()
        
        # Verify all data is intact
        assert retrieved is not None, "Submission should be retrievable"
        assert retrieved.code == submission_data['code'], "Code should match"
        assert retrieved.participant_id == participant.id, "Participant ID should match"
        assert retrieved.challenge_id == challenge.id, "Challenge ID should match"
        assert retrieved.is_correct == submission_data['is_correct'], "Correctness flag should match"
        assert retrieved.validation_result == submission_data['validation_result'], "Validation result should match"
        
        # Verify server-side timestamp was recorded
        assert retrieved.timestamp is not None, "Timestamp should be set"
        # Timestamp should be between before and after times (with some tolerance)
        assert time_before <= retrieved.timestamp <= time_after + timedelta(seconds=1), \
            "Timestamp should be set by server during creation"


# Property 16: Multiple Submissions Allowed
# **Validates: Requirements 6.5**
class TestMultipleSubmissionsAllowed:
    """Property-based tests for multiple submissions from the same participant."""
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(st.lists(submission_data_strategy(), min_size=2, max_size=5))
    def test_multiple_submissions_allowed(self, db_session, submission_data_list):
        """
        Property 16: Multiple Submissions Allowed
        
        For any participant and challenge, submitting code multiple times should 
        result in multiple distinct submission records being stored.
        
        **Validates: Requirements 6.5**
        """
        # Use the first submission's unique_id for creating shared resources
        unique_id = submission_data_list[0]['unique_id']
        
        # Create a user (organizer) for the challenge
        organizer = User(
            username=f"org_multi_{unique_id}",
            email=f"org_multi_{unique_id}@test.com",
            role="organizer"
        )
        db_session.add(organizer)
        db_session.commit()
        
        # Create a user (participant) for the submissions
        participant = User(
            username=f"part_multi_{unique_id}",
            email=f"part_multi_{unique_id}@test.com",
            role="participant"
        )
        db_session.add(participant)
        db_session.commit()
        
        # Create a challenge
        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(hours=2)
        challenge = Challenge(
            title=f"MultiSubmit_Challenge_{unique_id}",
            description="Test challenge for multiple submissions",
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
        
        # Create multiple submissions for the same participant and challenge
        submission_ids = []
        submission_codes = []
        submission_timestamps = []
        
        for submission_data in submission_data_list:
            submission = Submission(
                challenge_id=challenge.id,
                participant_id=participant.id,
                code=submission_data['code'],
                is_correct=submission_data['is_correct'],
                validation_result=submission_data['validation_result']
            )
            
            db_session.add(submission)
            db_session.commit()
            db_session.refresh(submission)
            
            submission_ids.append(submission.id)
            submission_codes.append(submission.code)
            submission_timestamps.append(submission.timestamp)
        
        # Clear the session to ensure we're fetching from the database
        db_session.expire_all()
        
        # Retrieve all submissions for this participant and challenge
        retrieved_submissions = (
            db_session.query(Submission)
            .filter(
                Submission.participant_id == participant.id,
                Submission.challenge_id == challenge.id
            )
            .order_by(Submission.timestamp.asc())
            .all()
        )
        
        # Verify that all submissions were stored
        assert len(retrieved_submissions) == len(submission_data_list), \
            "All submissions should be stored"
        
        # Verify that each submission has a distinct ID
        retrieved_ids = [s.id for s in retrieved_submissions]
        assert len(set(retrieved_ids)) == len(submission_data_list), \
            "Each submission should have a unique ID"
        
        # Verify that all original submission IDs are present
        for submission_id in submission_ids:
            assert submission_id in retrieved_ids, \
                f"Submission {submission_id} should be retrievable"
        
        # Verify that each submission has the correct code
        retrieved_codes = [s.code for s in retrieved_submissions]
        for code in submission_codes:
            assert code in retrieved_codes, \
                "Each submission's code should be preserved"
        
        # Verify that timestamps are in chronological order (or equal)
        for i in range(len(retrieved_submissions) - 1):
            assert retrieved_submissions[i].timestamp <= retrieved_submissions[i + 1].timestamp, \
                "Submissions should be ordered chronologically"
        
        # Verify that all submissions belong to the same participant and challenge
        for submission in retrieved_submissions:
            assert submission.participant_id == participant.id, \
                "All submissions should belong to the same participant"
            assert submission.challenge_id == challenge.id, \
                "All submissions should belong to the same challenge"



# Property 17: Submissions Rejected After Challenge End
# **Validates: Requirements 6.6**
class TestSubmissionsRejectedAfterChallengeEnd:
    """Property-based tests for rejecting submissions after challenge end time."""
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(
        submission_data_strategy(),
        st.integers(min_value=1, max_value=3600)  # Time past end in seconds (1 second to 1 hour)
    )
    def test_submissions_rejected_after_challenge_end(
        self, db_session, submission_data, seconds_past_end
    ):
        """
        Property 17: Submissions Rejected After Challenge End
        
        For any challenge that has ended (current time > end time), attempting to 
        submit code should be rejected with an error.
        
        **Validates: Requirements 6.6**
        """
        from app.managers.submission_manager import SubmissionManager, SubmissionError
        
        unique_id = submission_data['unique_id']
        
        # Create a user (organizer) for the challenge
        organizer = User(
            username=f"org_ended_{unique_id}",
            email=f"org_ended_{unique_id}@test.com",
            role="organizer"
        )
        db_session.add(organizer)
        db_session.commit()
        
        # Create a user (participant) for the submission
        participant = User(
            username=f"part_ended_{unique_id}",
            email=f"part_ended_{unique_id}@test.com",
            role="participant"
        )
        db_session.add(participant)
        db_session.commit()
        
        # Create a challenge that has already ended
        # Set end_time in the past
        current_time = datetime.now(timezone.utc)
        end_time = current_time - timedelta(seconds=seconds_past_end)
        start_time = end_time - timedelta(hours=2)  # Started 2 hours before it ended
        
        challenge = Challenge(
            title=f"Ended_Challenge_{unique_id}",
            description="Test challenge that has ended",
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
        
        # Create a SubmissionManager instance
        submission_manager = SubmissionManager(db_session)
        
        # Attempt to submit code to the ended challenge
        # This should raise a SubmissionError
        with pytest.raises(SubmissionError) as exc_info:
            submission_manager.submit_code(
                challenge_id=challenge.id,
                participant_id=participant.id,
                code=submission_data['code']
            )
        
        # Verify the error message indicates the challenge has ended
        error_message = str(exc_info.value).lower()
        assert "ended" in error_message, \
            "Error message should indicate that the challenge has ended"
        
        # Verify that no submission was created in the database
        submissions = (
            db_session.query(Submission)
            .filter(
                Submission.participant_id == participant.id,
                Submission.challenge_id == challenge.id
            )
            .all()
        )
        
        assert len(submissions) == 0, \
            "No submission should be created for an ended challenge"
