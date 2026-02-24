import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from app.managers.challenge_manager import ChallengeManager, ValidationError
from app.models import Challenge, CodeFragment, TestCase


class TestChallengeManager:
    """Unit tests for ChallengeManager CRUD operations"""
    
    def test_create_challenge_success(self, db_session):
        """Test creating a valid challenge"""
        manager = ChallengeManager(db_session)
        
        challenge_data = {
            "title": "Test Challenge",
            "description": "A test challenge description",
            "language": "python",
            "correct_solution": "print('Hello, World!')",
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=1),
            "fragments": [
                {"content": "print('Hello", "original_order": 0},
                {"content": ", World!')", "original_order": 1}
            ],
            "test_cases": [
                {"input": "", "expected_output": "Hello, World!", "visible": True}
            ]
        }
        
        challenge = manager.create_challenge(challenge_data)
        
        assert challenge.id is not None
        assert challenge.title == "Test Challenge"
        assert challenge.description == "A test challenge description"
        assert challenge.language == "python"
        assert len(challenge.fragments) == 2
        assert len(challenge.test_cases) == 1
    
    def test_create_challenge_missing_title(self, db_session):
        """Test that creating a challenge without a title fails"""
        manager = ChallengeManager(db_session)
        
        challenge_data = {
            "description": "A test challenge",
            "language": "python",
            "test_cases": [{"input": "", "expected_output": "test", "visible": True}]
        }
        
        with pytest.raises(ValidationError) as exc_info:
            manager.create_challenge(challenge_data)
        
        assert "title" in str(exc_info.value).lower()
    
    def test_create_challenge_empty_title(self, db_session):
        """Test that creating a challenge with empty title fails"""
        manager = ChallengeManager(db_session)
        
        challenge_data = {
            "title": "   ",
            "description": "A test challenge",
            "language": "python",
            "test_cases": [{"input": "", "expected_output": "test", "visible": True}]
        }
        
        with pytest.raises(ValidationError) as exc_info:
            manager.create_challenge(challenge_data)
        
        assert "title" in str(exc_info.value).lower()
    
    def test_create_challenge_missing_description(self, db_session):
        """Test that creating a challenge without a description fails"""
        manager = ChallengeManager(db_session)
        
        challenge_data = {
            "title": "Test Challenge",
            "language": "python",
            "test_cases": [{"input": "", "expected_output": "test", "visible": True}]
        }
        
        with pytest.raises(ValidationError) as exc_info:
            manager.create_challenge(challenge_data)
        
        assert "description" in str(exc_info.value).lower()
    
    def test_create_challenge_missing_language(self, db_session):
        """Test that creating a challenge without a language fails"""
        manager = ChallengeManager(db_session)
        
        challenge_data = {
            "title": "Test Challenge",
            "description": "A test challenge",
            "test_cases": [{"input": "", "expected_output": "test", "visible": True}]
        }
        
        with pytest.raises(ValidationError) as exc_info:
            manager.create_challenge(challenge_data)
        
        assert "language" in str(exc_info.value).lower()
    
    def test_create_challenge_missing_test_cases(self, db_session):
        """Test that creating a challenge without test cases fails"""
        manager = ChallengeManager(db_session)
        
        challenge_data = {
            "title": "Test Challenge",
            "description": "A test challenge",
            "language": "python"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            manager.create_challenge(challenge_data)
        
        assert "test case" in str(exc_info.value).lower()
    
    def test_create_challenge_empty_test_cases(self, db_session):
        """Test that creating a challenge with empty test cases list fails"""
        manager = ChallengeManager(db_session)
        
        challenge_data = {
            "title": "Test Challenge",
            "description": "A test challenge",
            "language": "python",
            "test_cases": []
        }
        
        with pytest.raises(ValidationError) as exc_info:
            manager.create_challenge(challenge_data)
        
        assert "test case" in str(exc_info.value).lower()
    
    def test_create_challenge_invalid_time_range(self, db_session):
        """Test that creating a challenge with start time >= end time fails"""
        manager = ChallengeManager(db_session)
        
        now = datetime.now()
        challenge_data = {
            "title": "Test Challenge",
            "description": "A test challenge",
            "language": "python",
            "start_time": now,
            "end_time": now - timedelta(hours=1),  # End before start
            "test_cases": [{"input": "", "expected_output": "test", "visible": True}]
        }
        
        with pytest.raises(ValidationError) as exc_info:
            manager.create_challenge(challenge_data)
        
        assert "time" in str(exc_info.value).lower()
    
    def test_get_challenge_success(self, db_session):
        """Test retrieving an existing challenge"""
        manager = ChallengeManager(db_session)
        
        # Create a challenge first
        challenge_data = {
            "title": "Test Challenge",
            "description": "A test challenge",
            "language": "python",
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=1),
            "test_cases": [{"input": "", "expected_output": "test", "visible": True}]
        }
        created = manager.create_challenge(challenge_data)
        
        # Retrieve it
        retrieved = manager.get_challenge(created.id)
        
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.title == "Test Challenge"
    
    def test_get_challenge_not_found(self, db_session):
        """Test retrieving a non-existent challenge returns None"""
        manager = ChallengeManager(db_session)
        
        result = manager.get_challenge(uuid4())
        
        assert result is None
    
    def test_update_challenge_success(self, db_session):
        """Test updating a challenge"""
        manager = ChallengeManager(db_session)
        
        # Create a challenge
        challenge_data = {
            "title": "Original Title",
            "description": "Original description",
            "language": "python",
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=1),
            "test_cases": [{"input": "", "expected_output": "test", "visible": True}]
        }
        created = manager.create_challenge(challenge_data)
        
        # Update it
        updates = {
            "title": "Updated Title",
            "description": "Updated description"
        }
        updated = manager.update_challenge(created.id, updates)
        
        assert updated is not None
        assert updated.title == "Updated Title"
        assert updated.description == "Updated description"
        assert updated.language == "python"  # Unchanged
    
    def test_update_challenge_not_found(self, db_session):
        """Test updating a non-existent challenge returns None"""
        manager = ChallengeManager(db_session)
        
        result = manager.update_challenge(uuid4(), {"title": "New Title"})
        
        assert result is None
    
    def test_update_challenge_invalid_data(self, db_session):
        """Test updating a challenge with invalid data fails"""
        manager = ChallengeManager(db_session)
        
        # Create a challenge
        challenge_data = {
            "title": "Test Challenge",
            "description": "A test challenge",
            "language": "python",
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=1),
            "test_cases": [{"input": "", "expected_output": "test", "visible": True}]
        }
        created = manager.create_challenge(challenge_data)
        
        # Try to update with empty title
        with pytest.raises(ValidationError):
            manager.update_challenge(created.id, {"title": "   "})
    
    def test_delete_challenge_success(self, db_session):
        """Test deleting a challenge"""
        manager = ChallengeManager(db_session)
        
        # Create a challenge
        challenge_data = {
            "title": "Test Challenge",
            "description": "A test challenge",
            "language": "python",
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=1),
            "test_cases": [{"input": "", "expected_output": "test", "visible": True}]
        }
        created = manager.create_challenge(challenge_data)
        
        # Delete it
        result = manager.delete_challenge(created.id)
        
        assert result is True
        
        # Verify it's gone
        retrieved = manager.get_challenge(created.id)
        assert retrieved is None
    
    def test_delete_challenge_not_found(self, db_session):
        """Test deleting a non-existent challenge returns False"""
        manager = ChallengeManager(db_session)
        
        result = manager.delete_challenge(uuid4())
        
        assert result is False
    
    def test_delete_challenge_cascades_to_fragments(self, db_session):
        """Test that deleting a challenge also deletes its fragments"""
        manager = ChallengeManager(db_session)
        
        # Create a challenge with fragments
        challenge_data = {
            "title": "Test Challenge",
            "description": "A test challenge",
            "language": "python",
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=1),
            "fragments": [
                {"content": "fragment 1", "original_order": 0},
                {"content": "fragment 2", "original_order": 1}
            ],
            "test_cases": [{"input": "", "expected_output": "test", "visible": True}]
        }
        created = manager.create_challenge(challenge_data)
        challenge_id = created.id
        
        # Verify fragments exist
        fragments = db_session.query(CodeFragment).filter(
            CodeFragment.challenge_id == challenge_id
        ).all()
        assert len(fragments) == 2
        
        # Delete challenge
        manager.delete_challenge(challenge_id)
        
        # Verify fragments are gone
        fragments = db_session.query(CodeFragment).filter(
            CodeFragment.challenge_id == challenge_id
        ).all()
        assert len(fragments) == 0
    
    def test_delete_challenge_cascades_to_test_cases(self, db_session):
        """Test that deleting a challenge also deletes its test cases"""
        manager = ChallengeManager(db_session)
        
        # Create a challenge with test cases
        challenge_data = {
            "title": "Test Challenge",
            "description": "A test challenge",
            "language": "python",
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=1),
            "test_cases": [
                {"input": "1", "expected_output": "1", "visible": True},
                {"input": "2", "expected_output": "2", "visible": False}
            ]
        }
        created = manager.create_challenge(challenge_data)
        challenge_id = created.id
        
        # Verify test cases exist
        test_cases = db_session.query(TestCase).filter(
            TestCase.challenge_id == challenge_id
        ).all()
        assert len(test_cases) == 2
        
        # Delete challenge
        manager.delete_challenge(challenge_id)
        
        # Verify test cases are gone
        test_cases = db_session.query(TestCase).filter(
            TestCase.challenge_id == challenge_id
        ).all()
        assert len(test_cases) == 0
    
    def test_list_challenges_empty(self, db_session):
        """Test listing challenges when none exist"""
        manager = ChallengeManager(db_session)
        
        challenges = manager.list_challenges()
        
        assert challenges == []
    
    def test_list_challenges_multiple(self, db_session):
        """Test listing multiple challenges"""
        manager = ChallengeManager(db_session)
        
        # Create multiple challenges
        for i in range(3):
            challenge_data = {
                "title": f"Challenge {i}",
                "description": f"Description {i}",
                "language": "python",
                "start_time": datetime.now(),
                "end_time": datetime.now() + timedelta(hours=1),
                "test_cases": [{"input": "", "expected_output": "test", "visible": True}]
            }
            manager.create_challenge(challenge_data)
        
        challenges = manager.list_challenges()
        
        assert len(challenges) == 3
    
    def test_get_challenge_without_scrambling(self, db_session):
        """Test retrieving a challenge without fragment scrambling preserves original order"""
        manager = ChallengeManager(db_session)
        
        # Create a challenge with multiple fragments
        challenge_data = {
            "title": "Test Challenge",
            "description": "A test challenge",
            "language": "python",
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=1),
            "fragments": [
                {"content": "fragment 0", "original_order": 0},
                {"content": "fragment 1", "original_order": 1},
                {"content": "fragment 2", "original_order": 2},
                {"content": "fragment 3", "original_order": 3},
            ],
            "test_cases": [{"input": "", "expected_output": "test", "visible": True}]
        }
        created = manager.create_challenge(challenge_data)
        
        # Retrieve without scrambling
        retrieved = manager.get_challenge(created.id, scramble_fragments=False)
        
        assert retrieved is not None
        assert len(retrieved.fragments) == 4
        # Verify original order is preserved
        for i, fragment in enumerate(retrieved.fragments):
            assert fragment.original_order == i
    
    def test_get_challenge_with_scrambling(self, db_session):
        """Test retrieving a challenge with fragment scrambling randomizes order"""
        manager = ChallengeManager(db_session)
        
        # Create a challenge with multiple fragments
        challenge_data = {
            "title": "Test Challenge",
            "description": "A test challenge",
            "language": "python",
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=1),
            "fragments": [
                {"content": "fragment 0", "original_order": 0},
                {"content": "fragment 1", "original_order": 1},
                {"content": "fragment 2", "original_order": 2},
                {"content": "fragment 3", "original_order": 3},
                {"content": "fragment 4", "original_order": 4},
            ],
            "test_cases": [{"input": "", "expected_output": "test", "visible": True}]
        }
        created = manager.create_challenge(challenge_data)
        
        # Retrieve with scrambling multiple times to verify randomization
        # With 5 fragments, the probability of getting the same order twice is very low
        orders_seen = []
        for _ in range(10):
            retrieved = manager.get_challenge(created.id, scramble_fragments=True)
            order = [f.original_order for f in retrieved.fragments]
            orders_seen.append(tuple(order))
        
        # At least one retrieval should have a different order than the original
        original_order = (0, 1, 2, 3, 4)
        assert any(order != original_order for order in orders_seen), \
            "Fragment scrambling should produce at least one different order"
    
    def test_get_challenge_scrambling_preserves_database_order(self, db_session):
        """Test that scrambling doesn't affect the database order"""
        manager = ChallengeManager(db_session)
        
        # Create a challenge with fragments
        challenge_data = {
            "title": "Test Challenge",
            "description": "A test challenge",
            "language": "python",
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=1),
            "fragments": [
                {"content": "fragment 0", "original_order": 0},
                {"content": "fragment 1", "original_order": 1},
                {"content": "fragment 2", "original_order": 2},
            ],
            "test_cases": [{"input": "", "expected_output": "test", "visible": True}]
        }
        created = manager.create_challenge(challenge_data)
        
        # Retrieve with scrambling
        manager.get_challenge(created.id, scramble_fragments=True)
        
        # Retrieve again without scrambling to verify database order is preserved
        retrieved = manager.get_challenge(created.id, scramble_fragments=False)
        
        assert len(retrieved.fragments) == 3
        # Verify original order is still intact in database
        for i, fragment in enumerate(retrieved.fragments):
            assert fragment.original_order == i
    
    def test_get_challenge_without_filtering_shows_all_test_cases(self, db_session):
        """Test retrieving a challenge without filtering shows all test cases with expected outputs"""
        manager = ChallengeManager(db_session)
        
        # Create a challenge with visible and hidden test cases
        challenge_data = {
            "title": "Test Challenge",
            "description": "A test challenge",
            "language": "python",
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=1),
            "test_cases": [
                {"input": "1", "expected_output": "output1", "visible": True},
                {"input": "2", "expected_output": "output2", "visible": True},
                {"input": "3", "expected_output": "output3", "visible": False},
            ]
        }
        created = manager.create_challenge(challenge_data)
        
        # Retrieve without filtering
        retrieved = manager.get_challenge(created.id, filter_test_cases=False)
        
        assert retrieved is not None
        assert len(retrieved.test_cases) == 3
        # Verify all test cases have expected outputs
        for tc in retrieved.test_cases:
            assert tc.expected_output != ""
            assert tc.expected_output.startswith("output")
    
    def test_get_challenge_with_filtering_excludes_hidden_test_cases(self, db_session):
        """Test retrieving a challenge with filtering excludes hidden test cases"""
        manager = ChallengeManager(db_session)
        
        # Create a challenge with visible and hidden test cases
        challenge_data = {
            "title": "Test Challenge",
            "description": "A test challenge",
            "language": "python",
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=1),
            "test_cases": [
                {"input": "1", "expected_output": "output1", "visible": True},
                {"input": "2", "expected_output": "output2", "visible": True},
                {"input": "3", "expected_output": "output3", "visible": False},
                {"input": "4", "expected_output": "output4", "visible": False},
            ]
        }
        created = manager.create_challenge(challenge_data)
        
        # Retrieve with filtering
        retrieved = manager.get_challenge(created.id, filter_test_cases=True)
        
        assert retrieved is not None
        assert len(retrieved.test_cases) == 2  # Only visible test cases
        # Verify all returned test cases are visible
        for tc in retrieved.test_cases:
            assert tc.visible is True
    
    def test_get_challenge_with_filtering_clears_expected_outputs(self, db_session):
        """Test retrieving a challenge with filtering clears expected outputs from visible test cases"""
        manager = ChallengeManager(db_session)
        
        # Create a challenge with visible test cases
        challenge_data = {
            "title": "Test Challenge",
            "description": "A test challenge",
            "language": "python",
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=1),
            "test_cases": [
                {"input": "input1", "expected_output": "output1", "visible": True},
                {"input": "input2", "expected_output": "output2", "visible": True},
            ]
        }
        created = manager.create_challenge(challenge_data)
        
        # Retrieve with filtering
        retrieved = manager.get_challenge(created.id, filter_test_cases=True)
        
        assert retrieved is not None
        assert len(retrieved.test_cases) == 2
        # Verify expected outputs are cleared
        for tc in retrieved.test_cases:
            assert tc.expected_output == ""
            # But inputs should still be present
            assert tc.input != ""
            assert tc.input.startswith("input")
    
    def test_get_challenge_filtering_preserves_database_data(self, db_session):
        """Test that filtering doesn't affect the database data"""
        manager = ChallengeManager(db_session)
        
        # Create a challenge with test cases
        challenge_data = {
            "title": "Test Challenge",
            "description": "A test challenge",
            "language": "python",
            "start_time": datetime.now(),
            "end_time": datetime.now() + timedelta(hours=1),
            "test_cases": [
                {"input": "1", "expected_output": "output1", "visible": True},
                {"input": "2", "expected_output": "output2", "visible": False},
            ]
        }
        created = manager.create_challenge(challenge_data)
        
        # Retrieve with filtering
        manager.get_challenge(created.id, filter_test_cases=True)
        
        # Retrieve again without filtering to verify database data is preserved
        retrieved = manager.get_challenge(created.id, filter_test_cases=False)
        
        assert len(retrieved.test_cases) == 2
        # Verify expected outputs are still intact in database
        for tc in retrieved.test_cases:
            assert tc.expected_output != ""
            assert tc.expected_output.startswith("output")
        # Verify both visible and hidden test cases are present
        visible_count = sum(1 for tc in retrieved.test_cases if tc.visible)
        hidden_count = sum(1 for tc in retrieved.test_cases if not tc.visible)
        assert visible_count == 1
        assert hidden_count == 1


# Property-based tests using Hypothesis
from hypothesis import given, strategies as st, settings, HealthCheck


# Hypothesis strategies for generating incomplete challenge data
@st.composite
def incomplete_challenge_strategy(draw):
    """
    Generate challenge data that is missing at least one required field.
    
    Required fields: title, description, language, test_cases
    """
    # Define all possible fields
    all_fields = {
        'title': draw(st.text(min_size=1, max_size=100)),
        'description': draw(st.text(min_size=1, max_size=500)),
        'language': draw(st.sampled_from(['python'])),
        'test_cases': [{'input': 'test', 'expected_output': 'test', 'visible': True}]
    }
    
    # Choose which required field(s) to omit
    # We need to omit at least one required field
    fields_to_include = draw(st.sets(
        st.sampled_from(['title', 'description', 'language', 'test_cases']),
        min_size=0,
        max_size=3  # At most 3 out of 4, ensuring at least 1 is missing
    ))
    
    # Build incomplete challenge data
    incomplete_data = {}
    for field in fields_to_include:
        incomplete_data[field] = all_fields[field]
    
    # Optionally add non-required fields
    if draw(st.booleans()):
        incomplete_data['correct_solution'] = draw(st.text(max_size=200))
    if draw(st.booleans()):
        from datetime import datetime, timedelta
        start_time = datetime.now()
        incomplete_data['start_time'] = start_time
        incomplete_data['end_time'] = start_time + timedelta(hours=1)
    
    return incomplete_data


@st.composite
def empty_field_challenge_strategy(draw):
    """
    Generate challenge data where required fields are present but empty/whitespace.
    """
    # Choose which field to make empty
    empty_field = draw(st.sampled_from(['title', 'description', 'language']))
    
    challenge_data = {
        'title': 'Valid Title',
        'description': 'Valid Description',
        'language': 'python',
        'test_cases': [{'input': 'test', 'expected_output': 'test', 'visible': True}]
    }
    
    # Make the chosen field empty or whitespace
    if empty_field in ['title', 'description', 'language']:
        challenge_data[empty_field] = draw(st.sampled_from(['', '   ', '\t', '\n', '  \t\n  ']))
    
    return challenge_data


@st.composite
def empty_test_cases_strategy(draw):
    """
    Generate challenge data with empty test cases list.
    """
    challenge_data = {
        'title': draw(st.text(min_size=1, max_size=100)),
        'description': draw(st.text(min_size=1, max_size=500)),
        'language': draw(st.sampled_from(['python'])),
        'test_cases': []  # Empty list
    }
    
    return challenge_data


class TestChallengeValidationProperty:
    """
    Property-based tests for challenge validation.
    
    Feature: runtime-rush-platform
    """
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(incomplete_challenge_strategy())
    def test_challenge_validation_rejects_incomplete_data(self, db_session, challenge_data):
        """
        Property 2: Challenge Validation Rejects Incomplete Data
        
        For any challenge missing required fields (title, description, language, 
        or test cases), attempting to create the challenge should be rejected 
        with a validation error.
        
        **Validates: Requirements 1.6**
        """
        manager = ChallengeManager(db_session)
        
        # Attempting to create a challenge with incomplete data should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            manager.create_challenge(challenge_data)
        
        # Verify that the error message mentions a required field
        error_message = str(exc_info.value).lower()
        required_fields = ['title', 'description', 'language', 'test case']
        
        # At least one required field should be mentioned in the error
        assert any(field in error_message for field in required_fields), \
            f"Error message should mention a required field. Got: {exc_info.value}"
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(empty_field_challenge_strategy())
    def test_challenge_validation_rejects_empty_fields(self, db_session, challenge_data):
        """
        Property 2 (variant): Challenge Validation Rejects Empty Fields
        
        For any challenge where required fields are present but contain only 
        whitespace, attempting to create the challenge should be rejected 
        with a validation error.
        
        **Validates: Requirements 1.6**
        """
        manager = ChallengeManager(db_session)
        
        # Attempting to create a challenge with empty fields should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            manager.create_challenge(challenge_data)
        
        # Verify that the error message is about empty or missing fields
        error_message = str(exc_info.value).lower()
        assert any(word in error_message for word in ['empty', 'required', 'missing']), \
            f"Error message should indicate empty or missing field. Got: {exc_info.value}"
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(empty_test_cases_strategy())
    def test_challenge_validation_rejects_empty_test_cases(self, db_session, challenge_data):
        """
        Property 2 (variant): Challenge Validation Rejects Empty Test Cases
        
        For any challenge with an empty test cases list, attempting to create 
        the challenge should be rejected with a validation error.
        
        **Validates: Requirements 1.6**
        """
        manager = ChallengeManager(db_session)
        
        # Attempting to create a challenge with no test cases should raise ValidationError
        with pytest.raises(ValidationError) as exc_info:
            manager.create_challenge(challenge_data)
        
        # Verify that the error message mentions test cases
        error_message = str(exc_info.value).lower()
        assert 'test case' in error_message, \
            f"Error message should mention test cases. Got: {exc_info.value}"


# Hypothesis strategy for generating challenges with multiple fragments
@st.composite
def challenge_with_fragments_strategy(draw):
    """
    Generate challenge data with multiple code fragments (at least 2).
    """
    from datetime import datetime, timedelta
    
    # Generate at least 2 fragments, up to 10
    num_fragments = draw(st.integers(min_value=2, max_value=10))
    
    # Use text that excludes problematic characters:
    # - NUL characters (\x00) which PostgreSQL doesn't accept
    # - Surrogate characters which can't be encoded in UTF-8
    # Use printable ASCII and common Unicode characters
    safe_text = st.text(
        alphabet=st.characters(
            blacklist_categories=('Cs',),  # Exclude surrogates
            blacklist_characters='\x00'     # Exclude NUL
        ),
        min_size=1,
        max_size=100
    ).filter(lambda s: s.strip() != '')
    
    safe_text_long = st.text(
        alphabet=st.characters(
            blacklist_categories=('Cs',),  # Exclude surrogates
            blacklist_characters='\x00'     # Exclude NUL
        ),
        min_size=1,
        max_size=500
    ).filter(lambda s: s.strip() != '')
    
    fragments = []
    for i in range(num_fragments):
        fragments.append({
            'content': draw(safe_text),
            'original_order': i
        })
    
    challenge_data = {
        'title': draw(safe_text),
        'description': draw(safe_text_long),
        'language': 'python',
        'start_time': datetime.now(),
        'end_time': datetime.now() + timedelta(hours=1),
        'fragments': fragments,
        'test_cases': [{'input': 'test', 'expected_output': 'test', 'visible': True}]
    }
    
    return challenge_data


class TestFragmentScramblingProperty:
    """
    Property-based tests for fragment scrambling.
    
    Feature: runtime-rush-platform
    """
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(challenge_with_fragments_strategy())
    def test_fragment_scrambling_changes_order(self, db_session, challenge_data):
        """
        Property 3: Fragment Scrambling
        
        For any challenge with multiple code fragments, retrieving the challenge 
        for participants should return fragments in an order different from the 
        original order.
        
        **Validates: Requirements 2.2**
        """
        manager = ChallengeManager(db_session)
        
        # Create the challenge
        created = manager.create_challenge(challenge_data)
        
        # Get the original order
        original_order = tuple(f.original_order for f in created.fragments)
        
        # Retrieve with scrambling multiple times
        # With multiple fragments, at least one retrieval should produce a different order
        scrambled_orders = []
        max_attempts = 20  # Try up to 20 times to get a different order
        
        for _ in range(max_attempts):
            retrieved = manager.get_challenge(created.id, scramble_fragments=True)
            scrambled_order = tuple(f.original_order for f in retrieved.fragments)
            scrambled_orders.append(scrambled_order)
            
            # If we found a different order, the property is satisfied
            if scrambled_order != original_order:
                break
        
        # For challenges with 2+ fragments, scrambling should produce at least one different order
        # The probability of getting the same order 20 times in a row is extremely low
        # For 2 fragments: (1/2)^20 ≈ 0.0001%
        # For 3+ fragments: even lower
        assert any(order != original_order for order in scrambled_orders), \
            f"Fragment scrambling should produce at least one different order. " \
            f"Original: {original_order}, Got: {scrambled_orders}"
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(challenge_with_fragments_strategy())
    def test_fragment_scrambling_preserves_all_fragments(self, db_session, challenge_data):
        """
        Property 3 (variant): Fragment Scrambling Preserves All Fragments
        
        For any challenge with multiple code fragments, retrieving the challenge 
        with scrambling should return all fragments (same count and content), 
        just in a different order.
        
        **Validates: Requirements 2.2**
        """
        manager = ChallengeManager(db_session)
        
        # Create the challenge
        created = manager.create_challenge(challenge_data)
        
        # Get original fragments
        original_fragments = sorted(created.fragments, key=lambda f: f.original_order)
        original_count = len(original_fragments)
        original_contents = {f.content for f in original_fragments}
        
        # Retrieve with scrambling
        retrieved = manager.get_challenge(created.id, scramble_fragments=True)
        
        # Verify all fragments are present
        assert len(retrieved.fragments) == original_count, \
            "Scrambling should preserve fragment count"
        
        # Verify all fragment contents are present (order may differ)
        scrambled_contents = {f.content for f in retrieved.fragments}
        assert scrambled_contents == original_contents, \
            "Scrambling should preserve all fragment contents"
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(challenge_with_fragments_strategy())
    def test_fragment_scrambling_does_not_modify_database(self, db_session, challenge_data):
        """
        Property 3 (variant): Fragment Scrambling Does Not Modify Database
        
        For any challenge with multiple code fragments, retrieving the challenge 
        with scrambling should not affect the original order stored in the database.
        
        **Validates: Requirements 2.2**
        """
        manager = ChallengeManager(db_session)
        
        # Create the challenge
        created = manager.create_challenge(challenge_data)
        
        # Get original order
        original_order = tuple(f.original_order for f in created.fragments)
        
        # Retrieve with scrambling multiple times
        for _ in range(5):
            manager.get_challenge(created.id, scramble_fragments=True)
        
        # Retrieve without scrambling to check database order
        retrieved = manager.get_challenge(created.id, scramble_fragments=False)
        database_order = tuple(f.original_order for f in retrieved.fragments)
        
        # Database order should remain unchanged
        assert database_order == original_order, \
            "Scrambling should not modify the database order"



# Hypothesis strategy for generating challenges with test cases
@st.composite
def challenge_with_test_cases_strategy(draw):
    """
    Generate challenge data with multiple test cases (both visible and hidden).
    """
    from datetime import datetime, timedelta
    
    # Generate at least 2 test cases, up to 10
    num_test_cases = draw(st.integers(min_value=2, max_value=10))
    
    # Use safe text that excludes problematic characters
    safe_text = st.text(
        alphabet=st.characters(
            blacklist_categories=('Cs',),  # Exclude surrogates
            blacklist_characters='\x00'     # Exclude NUL
        ),
        min_size=1,
        max_size=100
    ).filter(lambda s: s.strip() != '')
    
    safe_text_long = st.text(
        alphabet=st.characters(
            blacklist_categories=('Cs',),  # Exclude surrogates
            blacklist_characters='\x00'     # Exclude NUL
        ),
        min_size=1,
        max_size=500
    ).filter(lambda s: s.strip() != '')
    
    test_cases = []
    for i in range(num_test_cases):
        test_cases.append({
            'input': draw(safe_text),
            'expected_output': draw(safe_text),
            'visible': draw(st.booleans())  # Randomly visible or hidden
        })
    
    challenge_data = {
        'title': draw(safe_text),
        'description': draw(safe_text_long),
        'language': 'python',
        'start_time': datetime.now(),
        'end_time': datetime.now() + timedelta(hours=1),
        'test_cases': test_cases
    }
    
    return challenge_data


class TestTestCaseVisibilityFilteringProperty:
    """
    Property-based tests for test case visibility filtering.
    
    Feature: runtime-rush-platform
    """
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(challenge_with_test_cases_strategy())
    def test_test_case_input_visibility_filtering(self, db_session, challenge_data):
        """
        Property 4: Test Case Input Visibility Filtering
        
        For any challenge with test cases, retrieving visible test cases should 
        return inputs but not expected outputs, while hidden test cases should 
        not be returned at all.
        
        **Validates: Requirements 2.5**
        """
        manager = ChallengeManager(db_session)
        
        # Create the challenge
        created = manager.create_challenge(challenge_data)
        
        # Count visible and hidden test cases
        visible_count = sum(1 for tc in challenge_data['test_cases'] if tc['visible'])
        hidden_count = sum(1 for tc in challenge_data['test_cases'] if not tc['visible'])
        
        # Retrieve with filtering
        retrieved = manager.get_challenge(created.id, filter_test_cases=True)
        
        # Property 1: Only visible test cases should be returned
        assert len(retrieved.test_cases) == visible_count, \
            f"Should return only {visible_count} visible test cases, got {len(retrieved.test_cases)}"
        
        # Property 2: All returned test cases should be visible
        for tc in retrieved.test_cases:
            assert tc.visible is True, \
                "All returned test cases should be visible"
        
        # Property 3: Expected outputs should be cleared (empty string)
        for tc in retrieved.test_cases:
            assert tc.expected_output == "", \
                f"Expected output should be cleared, got: {tc.expected_output}"
        
        # Property 4: Inputs should still be present (not empty)
        for tc in retrieved.test_cases:
            assert tc.input != "", \
                "Input should still be present"
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(challenge_with_test_cases_strategy())
    def test_test_case_filtering_does_not_modify_database(self, db_session, challenge_data):
        """
        Property 4 (variant): Test Case Filtering Does Not Modify Database
        
        For any challenge with test cases, retrieving the challenge with filtering 
        should not affect the original test case data stored in the database.
        
        **Validates: Requirements 2.5**
        """
        manager = ChallengeManager(db_session)
        
        # Create the challenge
        created = manager.create_challenge(challenge_data)
        
        # Store original test case data as a list of tuples to handle duplicates
        original_test_cases = [
            (tc['input'], tc['expected_output'], tc['visible'])
            for tc in challenge_data['test_cases']
        ]
        original_count = len(challenge_data['test_cases'])
        
        # Retrieve with filtering multiple times
        for _ in range(5):
            manager.get_challenge(created.id, filter_test_cases=True)
        
        # Retrieve without filtering to check database data
        retrieved = manager.get_challenge(created.id, filter_test_cases=False)
        
        # Database should still have all test cases
        assert len(retrieved.test_cases) == original_count, \
            "Filtering should not modify the database test case count"
        
        # All expected outputs should still be intact in database
        retrieved_test_cases = [
            (tc.input, tc.expected_output, tc.visible)
            for tc in retrieved.test_cases
        ]
        
        # Sort both lists to compare them (order might differ)
        assert sorted(retrieved_test_cases) == sorted(original_test_cases), \
            "Expected outputs should still be intact in database"
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.function_scoped_fixture])
    @given(challenge_with_test_cases_strategy())
    def test_unfiltered_retrieval_shows_all_test_cases(self, db_session, challenge_data):
        """
        Property 4 (variant): Unfiltered Retrieval Shows All Test Cases
        
        For any challenge with test cases, retrieving the challenge without 
        filtering should return all test cases (both visible and hidden) with 
        their expected outputs intact.
        
        **Validates: Requirements 2.5**
        """
        manager = ChallengeManager(db_session)
        
        # Create the challenge
        created = manager.create_challenge(challenge_data)
        
        # Store original test case data as a list of tuples to handle duplicates
        original_count = len(challenge_data['test_cases'])
        original_test_cases = [
            (tc['input'], tc['expected_output'], tc['visible'])
            for tc in challenge_data['test_cases']
        ]
        
        # Retrieve without filtering
        retrieved = manager.get_challenge(created.id, filter_test_cases=False)
        
        # Should return all test cases
        assert len(retrieved.test_cases) == original_count, \
            f"Should return all {original_count} test cases"
        
        # All expected outputs should be present
        retrieved_test_cases = [
            (tc.input, tc.expected_output, tc.visible)
            for tc in retrieved.test_cases
        ]
        
        # Sort both lists to compare them (order might differ)
        assert sorted(retrieved_test_cases) == sorted(original_test_cases), \
            "All test cases with expected outputs should match original"
