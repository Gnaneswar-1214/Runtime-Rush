"""
Property-based tests for challenge data persistence.

Feature: runtime-rush-platform
"""
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from datetime import datetime, timedelta
from app.models.challenge import Challenge, CodeFragment, TestCase
from app.models.user import User
import uuid


# Hypothesis strategies for generating test data
@st.composite
def challenge_data_strategy(draw):
    """Generate valid challenge data as a dictionary."""
    from datetime import timezone
    start_time = draw(st.datetimes(min_value=datetime(2024, 1, 1), max_value=datetime(2025, 12, 31), timezones=st.just(timezone.utc)))
    end_time = start_time + timedelta(hours=draw(st.integers(min_value=1, max_value=48)))
    
    # Generate unique identifiers using UUID to avoid constraint violations
    unique_id = str(uuid.uuid4())[:8]
    
    return {
        'title': draw(st.text(min_size=1, max_size=100, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Zs')))),
        'description': draw(st.text(min_size=1, max_size=500)),
        'language': draw(st.sampled_from(['python'])),
        'correct_solution': draw(st.text(min_size=1, max_size=500)),
        'start_time': start_time,
        'end_time': end_time,
        'num_fragments': draw(st.integers(min_value=1, max_value=5)),
        'num_test_cases': draw(st.integers(min_value=1, max_value=5)),
        'unique_id': unique_id
    }


# Property 1: Challenge Data Round-Trip Persistence
# **Validates: Requirements 1.1, 1.2, 1.3, 1.5, 2.1**
class TestChallengeRoundTripPersistence:
    """Property-based tests for challenge persistence."""
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(challenge_data_strategy())
    def test_challenge_data_round_trip_persistence(self, db_session, challenge_data):
        """
        Property 1: Challenge Data Round-Trip Persistence
        
        For any valid challenge with title, description, language, code fragments, 
        correct solution, and test cases, creating the challenge and then retrieving 
        it should return an equivalent challenge with all data intact.
        
        **Validates: Requirements 1.1, 1.2, 1.3, 1.5, 2.1**
        """
        # Create a user (organizer) first with unique username and email
        unique_id = challenge_data['unique_id']
        user = User(
            username=f"org_{unique_id}",
            email=f"org_{unique_id}@test.com",
            role="organizer"
        )
        db_session.add(user)
        db_session.commit()
        
        # Create the challenge
        challenge = Challenge(
            title=challenge_data['title'],
            description=challenge_data['description'],
            language=challenge_data['language'],
            correct_solution=challenge_data['correct_solution'],
            start_time=challenge_data['start_time'],
            end_time=challenge_data['end_time'],
            created_by=user.id
        )
        
        # Add code fragments
        num_fragments = challenge_data['num_fragments']
        for i in range(num_fragments):
            fragment = CodeFragment(
                content=f"fragment_{i}_content",
                original_order=i
            )
            challenge.fragments.append(fragment)
        
        # Add test cases
        num_test_cases = challenge_data['num_test_cases']
        for i in range(num_test_cases):
            test_case = TestCase(
                input=f"input_{i}",
                expected_output=f"output_{i}",
                visible=(i % 2 == 0)  # Alternate visible/hidden
            )
            challenge.test_cases.append(test_case)
        
        # Create the challenge
        db_session.add(challenge)
        db_session.commit()
        challenge_id = challenge.id
        
        # Clear the session to ensure we're fetching from the database
        db_session.expire_all()
        
        # Retrieve the challenge
        retrieved = db_session.query(Challenge).filter(Challenge.id == challenge_id).first()
        
        # Verify all data is intact
        assert retrieved is not None, "Challenge should be retrievable"
        assert retrieved.title == challenge_data['title'], "Title should match"
        assert retrieved.description == challenge_data['description'], "Description should match"
        assert retrieved.language == challenge_data['language'], "Language should match"
        assert retrieved.correct_solution == challenge_data['correct_solution'], "Correct solution should match"
        assert retrieved.start_time == challenge_data['start_time'], "Start time should match"
        assert retrieved.end_time == challenge_data['end_time'], "End time should match"
        assert retrieved.created_by == user.id, "Creator should match"
        
        # Verify fragments
        assert len(retrieved.fragments) == num_fragments, f"Should have {num_fragments} fragments"
        for i, fragment in enumerate(sorted(retrieved.fragments, key=lambda f: f.original_order)):
            assert fragment.content == f"fragment_{i}_content", f"Fragment {i} content should match"
            assert fragment.original_order == i, f"Fragment {i} order should match"
        
        # Verify test cases
        assert len(retrieved.test_cases) == num_test_cases, f"Should have {num_test_cases} test cases"
        retrieved_test_cases = sorted(retrieved.test_cases, key=lambda tc: tc.input)
        for i, test_case in enumerate(retrieved_test_cases):
            assert test_case.input == f"input_{i}", f"Test case {i} input should match"
            assert test_case.expected_output == f"output_{i}", f"Test case {i} output should match"
            assert test_case.visible == (i % 2 == 0), f"Test case {i} visibility should match"
