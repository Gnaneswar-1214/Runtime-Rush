import pytest
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from app.managers.winner_manager import WinnerManager, WinnerError
from app.managers.challenge_manager import ChallengeManager
from app.managers.submission_manager import SubmissionManager
from app.models import User, Challenge, Submission, Winner


@pytest.fixture
def winner_manager(db_session):
    return WinnerManager(db_session)


@pytest.fixture
def challenge_manager(db_session):
    return ChallengeManager(db_session)


@pytest.fixture
def submission_manager(db_session):
    return SubmissionManager(db_session)


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
def test_challenge(db_session, challenge_manager):
    """Create a test challenge"""
    challenge_data = {
        "title": "Test Challenge",
        "description": "A test challenge",
        "language": "python",
        "correct_solution": "print('hello')",
        "start_time": datetime.now(timezone.utc) - timedelta(hours=1),
        "end_time": datetime.now(timezone.utc) + timedelta(hours=1),
        "fragments": [
            {"content": "print('hello')", "original_order": 0}
        ],
        "test_cases": [
            {"input": "", "expected_output": "hello", "visible": True}
        ]
    }
    return challenge_manager.create_challenge(challenge_data)


class TestDeclareWinner:
    """Tests for declareWinner method"""
    
    def test_declare_winner_success(
        self, winner_manager, submission_manager, test_challenge, test_user
    ):
        """Test successful winner declaration"""
        # Create a correct submission
        submission = submission_manager.submit_code(
            challenge_id=test_challenge.id,
            participant_id=test_user.id,
            code="print('hello')"
        )
        
        # Declare winner
        winner = winner_manager.declare_winner(
            challenge_id=test_challenge.id,
            submission_id=submission.id
        )
        
        # Verify winner was created
        assert winner is not None
        assert winner.challenge_id == test_challenge.id
        assert winner.participant_id == test_user.id
        assert winner.submission_id == submission.id
        assert winner.timestamp == submission.timestamp
        assert winner.declared_at is not None
    
    def test_declare_winner_immutability(
        self, winner_manager, submission_manager, test_challenge, test_user, db_session
    ):
        """Test that winner cannot be changed once declared (immutability)"""
        # Create first correct submission
        submission1 = submission_manager.submit_code(
            challenge_id=test_challenge.id,
            participant_id=test_user.id,
            code="print('hello')"
        )
        
        # Declare first winner
        winner1 = winner_manager.declare_winner(
            challenge_id=test_challenge.id,
            submission_id=submission1.id
        )
        
        # Create second user and submission
        user2 = User(
            id=uuid4(),
            username="testuser2",
            email="test2@example.com",
            role="participant"
        )
        db_session.add(user2)
        db_session.commit()
        
        submission2 = submission_manager.submit_code(
            challenge_id=test_challenge.id,
            participant_id=user2.id,
            code="print('hello')"
        )
        
        # Attempt to declare second winner should fail
        with pytest.raises(WinnerError) as exc_info:
            winner_manager.declare_winner(
                challenge_id=test_challenge.id,
                submission_id=submission2.id
            )
        
        assert "Winner already declared" in str(exc_info.value)
        
        # Verify original winner is unchanged
        current_winner = winner_manager.get_winner(test_challenge.id)
        assert current_winner.submission_id == submission1.id
        assert current_winner.participant_id == test_user.id
    
    def test_declare_winner_submission_not_found(
        self, winner_manager, test_challenge
    ):
        """Test declaring winner with non-existent submission"""
        fake_submission_id = uuid4()
        
        with pytest.raises(WinnerError) as exc_info:
            winner_manager.declare_winner(
                challenge_id=test_challenge.id,
                submission_id=fake_submission_id
            )
        
        assert "not found" in str(exc_info.value)
    
    def test_declare_winner_incorrect_submission(
        self, winner_manager, test_challenge, test_user, db_session
    ):
        """Test declaring winner with incorrect submission"""
        # Create an incorrect submission manually
        incorrect_submission = Submission(
            id=uuid4(),
            challenge_id=test_challenge.id,
            participant_id=test_user.id,
            code="print('wrong')",
            is_correct=False,
            validation_result={"allTestsPassed": False}
        )
        db_session.add(incorrect_submission)
        db_session.commit()
        
        # Attempt to declare winner with incorrect submission
        with pytest.raises(WinnerError) as exc_info:
            winner_manager.declare_winner(
                challenge_id=test_challenge.id,
                submission_id=incorrect_submission.id
            )
        
        assert "not correct" in str(exc_info.value)
    
    def test_declare_winner_wrong_challenge(
        self, winner_manager, submission_manager, challenge_manager, 
        test_challenge, test_user
    ):
        """Test declaring winner with submission from different challenge"""
        # Create another challenge
        challenge_data = {
            "title": "Another Challenge",
            "description": "Another test challenge",
            "language": "python",
            "correct_solution": "print('world')",
            "start_time": datetime.now(timezone.utc) - timedelta(hours=1),
            "end_time": datetime.now(timezone.utc) + timedelta(hours=1),
            "fragments": [
                {"content": "print('world')", "original_order": 0}
            ],
            "test_cases": [
                {"input": "", "expected_output": "world", "visible": True}
            ]
        }
        challenge2 = challenge_manager.create_challenge(challenge_data)
        
        # Create submission for challenge2
        submission = submission_manager.submit_code(
            challenge_id=challenge2.id,
            participant_id=test_user.id,
            code="print('world')"
        )
        
        # Try to declare winner for challenge1 with submission from challenge2
        with pytest.raises(WinnerError) as exc_info:
            winner_manager.declare_winner(
                challenge_id=test_challenge.id,
                submission_id=submission.id
            )
        
        assert "does not belong to challenge" in str(exc_info.value)


class TestGetWinner:
    """Tests for getWinner method"""
    
    def test_get_winner_exists(
        self, winner_manager, submission_manager, test_challenge, test_user
    ):
        """Test retrieving an existing winner"""
        # Create submission and declare winner
        submission = submission_manager.submit_code(
            challenge_id=test_challenge.id,
            participant_id=test_user.id,
            code="print('hello')"
        )
        
        winner_manager.declare_winner(
            challenge_id=test_challenge.id,
            submission_id=submission.id
        )
        
        # Retrieve winner
        winner = winner_manager.get_winner(test_challenge.id)
        
        assert winner is not None
        assert winner.challenge_id == test_challenge.id
        assert winner.participant_id == test_user.id
        assert winner.submission_id == submission.id
    
    def test_get_winner_not_exists(self, winner_manager, test_challenge):
        """Test retrieving winner when none declared"""
        winner = winner_manager.get_winner(test_challenge.id)
        assert winner is None
    
    def test_get_winner_nonexistent_challenge(self, winner_manager):
        """Test retrieving winner for non-existent challenge"""
        fake_challenge_id = uuid4()
        winner = winner_manager.get_winner(fake_challenge_id)
        assert winner is None


class TestGetLeaderboard:
    """Tests for getLeaderboard method"""
    
    def test_get_leaderboard_chronological_order(
        self, winner_manager, submission_manager, test_challenge, test_user, db_session
    ):
        """Test leaderboard returns correct submissions in chronological order"""
        # Create multiple users and submissions with different timestamps
        users = []
        submissions = []
        
        for i in range(3):
            user = User(
                id=uuid4(),
                username=f"user{i}",
                email=f"user{i}@example.com",
                role="participant"
            )
            db_session.add(user)
            users.append(user)
        
        db_session.commit()
        
        # Create submissions with explicit timestamps
        base_time = datetime.now(timezone.utc)
        for i, user in enumerate(users):
            submission = Submission(
                id=uuid4(),
                challenge_id=test_challenge.id,
                participant_id=user.id,
                code="print('hello')",
                is_correct=True,
                validation_result={"allTestsPassed": True},
                timestamp=base_time + timedelta(seconds=i)
            )
            db_session.add(submission)
            submissions.append(submission)
        
        db_session.commit()
        
        # Get leaderboard
        leaderboard = winner_manager.get_leaderboard(test_challenge.id)
        
        # Verify chronological ordering (earliest first)
        assert len(leaderboard) == 3
        for i in range(3):
            assert leaderboard[i].participant_id == users[i].id
            assert leaderboard[i].timestamp == submissions[i].timestamp
        
        # Verify timestamps are in ascending order
        for i in range(len(leaderboard) - 1):
            assert leaderboard[i].timestamp < leaderboard[i + 1].timestamp
    
    def test_get_leaderboard_only_correct_submissions(
        self, winner_manager, test_challenge, test_user, db_session
    ):
        """Test leaderboard only includes correct submissions"""
        # Create mix of correct and incorrect submissions
        correct_submission = Submission(
            id=uuid4(),
            challenge_id=test_challenge.id,
            participant_id=test_user.id,
            code="print('hello')",
            is_correct=True,
            validation_result={"allTestsPassed": True}
        )
        
        incorrect_submission = Submission(
            id=uuid4(),
            challenge_id=test_challenge.id,
            participant_id=test_user.id,
            code="print('wrong')",
            is_correct=False,
            validation_result={"allTestsPassed": False}
        )
        
        db_session.add(correct_submission)
        db_session.add(incorrect_submission)
        db_session.commit()
        
        # Get leaderboard
        leaderboard = winner_manager.get_leaderboard(test_challenge.id)
        
        # Should only contain correct submission
        assert len(leaderboard) == 1
        assert leaderboard[0].id == correct_submission.id
        assert leaderboard[0].is_correct is True
    
    def test_get_leaderboard_empty(self, winner_manager, test_challenge):
        """Test leaderboard when no correct submissions exist"""
        leaderboard = winner_manager.get_leaderboard(test_challenge.id)
        assert len(leaderboard) == 0
    
    def test_get_leaderboard_first_is_winner(
        self, winner_manager, submission_manager, test_challenge, db_session
    ):
        """Test that first submission in leaderboard is the winner"""
        # Create multiple users and submissions
        users = []
        for i in range(3):
            user = User(
                id=uuid4(),
                username=f"user{i}",
                email=f"user{i}@example.com",
                role="participant"
            )
            db_session.add(user)
            users.append(user)
        
        db_session.commit()
        
        # Create submissions with different timestamps
        base_time = datetime.now(timezone.utc)
        submissions = []
        for i, user in enumerate(users):
            submission = Submission(
                id=uuid4(),
                challenge_id=test_challenge.id,
                participant_id=user.id,
                code="print('hello')",
                is_correct=True,
                validation_result={"allTestsPassed": True},
                timestamp=base_time + timedelta(seconds=i)
            )
            db_session.add(submission)
            submissions.append(submission)
        
        db_session.commit()
        
        # Declare winner (should be first submission)
        winner = winner_manager.declare_winner(
            challenge_id=test_challenge.id,
            submission_id=submissions[0].id
        )
        
        # Get leaderboard
        leaderboard = winner_manager.get_leaderboard(test_challenge.id)
        
        # First in leaderboard should be the winner
        assert leaderboard[0].id == winner.submission_id
        assert leaderboard[0].participant_id == winner.participant_id
        assert leaderboard[0].timestamp == winner.timestamp



# Property-based tests using Hypothesis
from hypothesis import given, strategies as st, settings, HealthCheck


@st.composite
def multiple_correct_submissions_strategy(draw):
    """
    Generate a list of correct submissions with different timestamps.
    Returns a list of tuples: (participant_id, timestamp_offset_seconds)
    
    The strategy ensures:
    - At least 2 submissions (to test winner selection)
    - Each submission has a unique timestamp
    - Timestamps are in random order (not necessarily chronological)
    """
    num_submissions = draw(st.integers(min_value=2, max_value=10))
    
    # Generate unique timestamp offsets (in seconds)
    # Using a set to ensure uniqueness, then converting to sorted list
    timestamp_offsets = draw(
        st.lists(
            st.integers(min_value=0, max_value=3600),  # 0 to 1 hour in seconds
            min_size=num_submissions,
            max_size=num_submissions,
            unique=True
        )
    )
    
    # Shuffle the offsets to simulate random submission order
    shuffled_offsets = draw(st.permutations(timestamp_offsets))
    
    # Generate participant data with unique identifiers using UUIDs
    submissions_data = []
    for i, offset in enumerate(shuffled_offsets):
        unique_id = str(uuid4())[:8]  # Use first 8 chars of UUID for uniqueness
        participant_data = {
            'username': f'participant_{unique_id}',
            'email': f'participant_{unique_id}@example.com',
            'timestamp_offset': offset
        }
        submissions_data.append(participant_data)
    
    return submissions_data


class TestFirstCorrectSubmissionWinsProperty:
    """
    Property-based tests for first correct submission wins.
    
    Feature: runtime-rush-platform
    """
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(multiple_correct_submissions_strategy())
    def test_first_correct_submission_wins(
        self, db_session, submissions_data
    ):
        """
        Property 18: First Correct Submission Wins
        
        For any challenge with multiple correct submissions, the winner should be 
        the submission with the earliest timestamp.
        
        **Validates: Requirements 7.1, 7.2**
        """
        # Create managers
        challenge_manager = ChallengeManager(db_session)
        
        # Create a test challenge
        challenge_data = {
            "title": "Property Test Challenge",
            "description": "Testing first correct submission wins",
            "language": "python",
            "correct_solution": "print('hello')",
            "start_time": datetime.now(timezone.utc) - timedelta(hours=1),
            "end_time": datetime.now(timezone.utc) + timedelta(hours=1),
            "fragments": [
                {"content": "print('hello')", "original_order": 0}
            ],
            "test_cases": [
                {"input": "", "expected_output": "hello", "visible": True}
            ]
        }
        challenge = challenge_manager.create_challenge(challenge_data)
        
        # Create users and submissions with the generated data
        base_time = datetime.now(timezone.utc)
        users = []
        submissions = []
        earliest_timestamp = None
        earliest_submission = None
        
        for data in submissions_data:
            # Create user
            user = User(
                id=uuid4(),
                username=data['username'],
                email=data['email'],
                role="participant"
            )
            db_session.add(user)
            users.append(user)
        
        db_session.commit()
        
        # Create submissions with specified timestamps
        for i, data in enumerate(submissions_data):
            timestamp = base_time + timedelta(seconds=data['timestamp_offset'])
            
            submission = Submission(
                id=uuid4(),
                challenge_id=challenge.id,
                participant_id=users[i].id,
                code="print('hello')",
                is_correct=True,
                validation_result={"allTestsPassed": True},
                timestamp=timestamp
            )
            db_session.add(submission)
            submissions.append(submission)
            
            # Track the earliest submission
            if earliest_timestamp is None or timestamp < earliest_timestamp:
                earliest_timestamp = timestamp
                earliest_submission = submission
        
        db_session.commit()
        
        # Declare winner using the first submission (by creation order, not timestamp)
        # The system should identify the correct winner based on timestamp
        winner_manager = WinnerManager(db_session)
        
        # Get leaderboard to find the actual first submission by timestamp
        leaderboard = winner_manager.get_leaderboard(challenge.id)
        
        # The first submission in the leaderboard should be the one with earliest timestamp
        assert len(leaderboard) > 0, "Leaderboard should contain submissions"
        first_in_leaderboard = leaderboard[0]
        
        # Verify that the first in leaderboard is indeed the earliest submission
        assert first_in_leaderboard.id == earliest_submission.id, \
            f"First submission in leaderboard should be the earliest by timestamp"
        assert first_in_leaderboard.timestamp == earliest_timestamp, \
            f"First submission timestamp should be the earliest"
        
        # Declare the winner (should be the earliest submission)
        winner = winner_manager.declare_winner(
            challenge_id=challenge.id,
            submission_id=first_in_leaderboard.id
        )
        
        # Verify winner properties
        assert winner.submission_id == earliest_submission.id, \
            "Winner should be the submission with earliest timestamp"
        assert winner.participant_id == earliest_submission.participant_id, \
            "Winner participant should match earliest submission"
        assert winner.timestamp == earliest_timestamp, \
            "Winner timestamp should be the earliest"
        
        # Verify that all submissions in leaderboard are in chronological order
        for i in range(len(leaderboard) - 1):
            assert leaderboard[i].timestamp <= leaderboard[i + 1].timestamp, \
                "Leaderboard should be ordered chronologically (earliest first)"
        
        # Verify winner immutability - trying to declare another winner should fail
        if len(submissions) > 1:
            second_submission = [s for s in submissions if s.id != earliest_submission.id][0]
            with pytest.raises(WinnerError) as exc_info:
                winner_manager.declare_winner(
                    challenge_id=challenge.id,
                    submission_id=second_submission.id
                )
            assert "already declared" in str(exc_info.value).lower()


@st.composite
def winner_immutability_strategy(draw):
    """
    Generate data for testing winner immutability.
    Returns a tuple of (num_attempts, submission_indices)
    
    The strategy ensures:
    - At least 2 correct submissions exist
    - Multiple attempts to change the winner (2-5 attempts)
    - Different submissions are used in each attempt
    """
    num_submissions = draw(st.integers(min_value=2, max_value=5))
    num_attempts = draw(st.integers(min_value=2, max_value=5))
    
    # Generate indices for which submissions to use in change attempts
    # These will be different from the first (winner) submission
    attempt_indices = draw(
        st.lists(
            st.integers(min_value=1, max_value=num_submissions - 1),
            min_size=num_attempts,
            max_size=num_attempts
        )
    )
    
    return (num_submissions, attempt_indices)


class TestWinnerImmutabilityProperty:
    """
    Property-based tests for winner immutability.
    
    Feature: runtime-rush-platform
    """
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(winner_immutability_strategy())
    def test_winner_immutability(
        self, db_session, test_data
    ):
        """
        Property 19: Winner Immutability
        
        For any challenge with a declared winner, attempting to declare a different 
        winner should fail, and the original winner should remain unchanged.
        
        **Validates: Requirements 7.4**
        """
        num_submissions, attempt_indices = test_data
        
        # Create managers
        challenge_manager = ChallengeManager(db_session)
        winner_manager = WinnerManager(db_session)
        
        # Create a test challenge
        challenge_data = {
            "title": "Winner Immutability Test",
            "description": "Testing winner cannot be changed",
            "language": "python",
            "correct_solution": "print('test')",
            "start_time": datetime.now(timezone.utc) - timedelta(hours=1),
            "end_time": datetime.now(timezone.utc) + timedelta(hours=1),
            "fragments": [
                {"content": "print('test')", "original_order": 0}
            ],
            "test_cases": [
                {"input": "", "expected_output": "test", "visible": True}
            ]
        }
        challenge = challenge_manager.create_challenge(challenge_data)
        
        # Create multiple users and correct submissions
        users = []
        submissions = []
        
        for i in range(num_submissions):
            user = User(
                id=uuid4(),
                username=f"user_{uuid4().hex[:8]}",
                email=f"user_{uuid4().hex[:8]}@example.com",
                role="participant"
            )
            db_session.add(user)
            users.append(user)
        
        db_session.commit()
        
        # Create correct submissions
        base_time = datetime.now(timezone.utc)
        for i, user in enumerate(users):
            submission = Submission(
                id=uuid4(),
                challenge_id=challenge.id,
                participant_id=user.id,
                code="print('test')",
                is_correct=True,
                validation_result={"allTestsPassed": True},
                timestamp=base_time + timedelta(seconds=i)
            )
            db_session.add(submission)
            submissions.append(submission)
        
        db_session.commit()
        
        # Declare the first winner
        original_winner = winner_manager.declare_winner(
            challenge_id=challenge.id,
            submission_id=submissions[0].id
        )
        
        # Store original winner details
        original_winner_id = original_winner.submission_id
        original_participant_id = original_winner.participant_id
        original_timestamp = original_winner.timestamp
        original_declared_at = original_winner.declared_at
        
        # Attempt to declare different winners multiple times
        for attempt_idx in attempt_indices:
            # Try to declare a different submission as winner
            different_submission = submissions[attempt_idx]
            
            # This should fail with WinnerError
            with pytest.raises(WinnerError) as exc_info:
                winner_manager.declare_winner(
                    challenge_id=challenge.id,
                    submission_id=different_submission.id
                )
            
            # Verify error message indicates winner already declared
            assert "already declared" in str(exc_info.value).lower(), \
                "Error message should indicate winner already declared"
            
            # Verify the original winner remains unchanged
            current_winner = winner_manager.get_winner(challenge.id)
            assert current_winner is not None, "Winner should still exist"
            assert current_winner.submission_id == original_winner_id, \
                "Winner submission_id should remain unchanged"
            assert current_winner.participant_id == original_participant_id, \
                "Winner participant_id should remain unchanged"
            assert current_winner.timestamp == original_timestamp, \
                "Winner timestamp should remain unchanged"
            assert current_winner.declared_at == original_declared_at, \
                "Winner declared_at should remain unchanged"
            assert current_winner.challenge_id == challenge.id, \
                "Winner challenge_id should remain unchanged"
        
        # Final verification: winner is still the original
        final_winner = winner_manager.get_winner(challenge.id)
        assert final_winner.submission_id == original_winner_id, \
            "After all attempts, winner should still be the original"
        assert final_winner.participant_id == original_participant_id, \
            "After all attempts, winner participant should still be the original"


@st.composite
def leaderboard_submissions_strategy(draw):
    """
    Generate data for testing leaderboard chronological ordering.
    Returns a list of submission data with randomized timestamps.
    
    The strategy ensures:
    - At least 2 correct submissions (to test ordering)
    - Timestamps are unique and in random order
    - Mix of correct and incorrect submissions
    """
    num_correct = draw(st.integers(min_value=2, max_value=10))
    num_incorrect = draw(st.integers(min_value=0, max_value=5))
    
    # Generate unique timestamp offsets for correct submissions
    correct_offsets = draw(
        st.lists(
            st.integers(min_value=0, max_value=7200),  # 0 to 2 hours in seconds
            min_size=num_correct,
            max_size=num_correct,
            unique=True
        )
    )
    
    # Shuffle to simulate random submission order (not chronological)
    shuffled_offsets = draw(st.permutations(correct_offsets))
    
    # Generate submission data
    submissions_data = []
    
    # Add correct submissions with shuffled timestamps
    for offset in shuffled_offsets:
        unique_id = str(uuid4())[:8]
        submissions_data.append({
            'username': f'correct_user_{unique_id}',
            'email': f'correct_{unique_id}@example.com',
            'timestamp_offset': offset,
            'is_correct': True
        })
    
    # Add incorrect submissions with random timestamps
    for i in range(num_incorrect):
        unique_id = str(uuid4())[:8]
        offset = draw(st.integers(min_value=0, max_value=7200))
        submissions_data.append({
            'username': f'incorrect_user_{unique_id}',
            'email': f'incorrect_{unique_id}@example.com',
            'timestamp_offset': offset,
            'is_correct': False
        })
    
    # Shuffle all submissions together
    shuffled_all = draw(st.permutations(submissions_data))
    
    return shuffled_all


class TestLeaderboardChronologicalOrderingProperty:
    """
    Property-based tests for leaderboard chronological ordering.
    
    Feature: runtime-rush-platform
    """
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(leaderboard_submissions_strategy())
    def test_leaderboard_chronological_ordering(
        self, db_session, submissions_data
    ):
        """
        Property 20: Leaderboard Chronological Ordering
        
        For any challenge with multiple correct submissions, retrieving the leaderboard 
        should return submissions ordered by timestamp (earliest first).
        
        **Validates: Requirements 7.5**
        """
        # Create managers
        challenge_manager = ChallengeManager(db_session)
        winner_manager = WinnerManager(db_session)
        
        # Create a test challenge
        challenge_data = {
            "title": "Leaderboard Ordering Test",
            "description": "Testing leaderboard chronological ordering",
            "language": "python",
            "correct_solution": "print('result')",
            "start_time": datetime.now(timezone.utc) - timedelta(hours=1),
            "end_time": datetime.now(timezone.utc) + timedelta(hours=1),
            "fragments": [
                {"content": "print('result')", "original_order": 0}
            ],
            "test_cases": [
                {"input": "", "expected_output": "result", "visible": True}
            ]
        }
        challenge = challenge_manager.create_challenge(challenge_data)
        
        # Create users and submissions
        base_time = datetime.now(timezone.utc)
        correct_submissions = []
        
        for data in submissions_data:
            # Create user
            user = User(
                id=uuid4(),
                username=data['username'],
                email=data['email'],
                role="participant"
            )
            db_session.add(user)
            db_session.flush()
            
            # Create submission with specified timestamp
            timestamp = base_time + timedelta(seconds=data['timestamp_offset'])
            
            submission = Submission(
                id=uuid4(),
                challenge_id=challenge.id,
                participant_id=user.id,
                code="print('result')" if data['is_correct'] else "print('wrong')",
                is_correct=data['is_correct'],
                validation_result={"allTestsPassed": data['is_correct']},
                timestamp=timestamp
            )
            db_session.add(submission)
            
            # Track correct submissions for verification
            if data['is_correct']:
                correct_submissions.append({
                    'submission': submission,
                    'timestamp': timestamp
                })
        
        db_session.commit()
        
        # Get leaderboard
        leaderboard = winner_manager.get_leaderboard(challenge.id)
        
        # Property 1: Leaderboard should only contain correct submissions
        assert len(leaderboard) == len([s for s in submissions_data if s['is_correct']]), \
            "Leaderboard should contain exactly the number of correct submissions"
        
        for submission in leaderboard:
            assert submission.is_correct is True, \
                "All submissions in leaderboard must be correct"
        
        # Property 2: Leaderboard should be ordered chronologically (earliest first)
        for i in range(len(leaderboard) - 1):
            assert leaderboard[i].timestamp <= leaderboard[i + 1].timestamp, \
                f"Leaderboard must be ordered chronologically: " \
                f"submission at index {i} (timestamp {leaderboard[i].timestamp}) " \
                f"should be before or equal to submission at index {i+1} " \
                f"(timestamp {leaderboard[i+1].timestamp})"
        
        # Property 3: All correct submissions should be in the leaderboard
        leaderboard_ids = {s.id for s in leaderboard}
        correct_submission_ids = {s['submission'].id for s in correct_submissions}
        
        assert leaderboard_ids == correct_submission_ids, \
            "Leaderboard should contain all and only correct submissions"
        
        # Property 4: First submission in leaderboard has the earliest timestamp
        if len(leaderboard) > 0:
            earliest_timestamp = min(s['timestamp'] for s in correct_submissions)
            assert leaderboard[0].timestamp == earliest_timestamp, \
                "First submission in leaderboard should have the earliest timestamp"
        
        # Property 5: Last submission in leaderboard has the latest timestamp
        if len(leaderboard) > 0:
            latest_timestamp = max(s['timestamp'] for s in correct_submissions)
            assert leaderboard[-1].timestamp == latest_timestamp, \
                "Last submission in leaderboard should have the latest timestamp"
        
        # Property 6: Timestamps in leaderboard match original submission timestamps
        for lb_submission in leaderboard:
            # Find the corresponding original submission
            original = next(
                (s for s in correct_submissions if s['submission'].id == lb_submission.id),
                None
            )
            assert original is not None, \
                f"Leaderboard submission {lb_submission.id} should exist in original submissions"
            assert lb_submission.timestamp == original['timestamp'], \
                "Leaderboard submission timestamp should match original timestamp"
