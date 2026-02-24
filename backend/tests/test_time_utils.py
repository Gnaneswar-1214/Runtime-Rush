"""
Tests for time calculation utility functions.

This module contains both unit tests and property-based tests for
the time calculation utilities used in challenge management.
"""

import pytest
from datetime import datetime, timezone, timedelta
from hypothesis import given, strategies as st
from app.utils.time_utils import (
    calculate_remaining_time,
    calculate_time_until_start,
    is_challenge_active,
    mark_challenge_as_ended,
)
from app.models.challenge import Challenge


# Helper function to create a challenge with specific times
def create_test_challenge(start_time: datetime, end_time: datetime) -> Challenge:
    """Create a minimal challenge object for testing."""
    challenge = Challenge()
    challenge.start_time = start_time
    challenge.end_time = end_time
    return challenge


# Strategy for generating timezone-aware datetimes
# Hypothesis requires naive datetimes for min/max, then we add timezone
datetime_strategy = st.datetimes(
    min_value=datetime(2020, 1, 1),
    max_value=datetime(2030, 12, 31),
).map(lambda dt: dt.replace(tzinfo=timezone.utc))


class TestCalculateRemainingTime:
    """Unit tests for calculate_remaining_time function."""
    
    def test_active_challenge_returns_positive_time(self):
        """Test that an active challenge returns positive remaining time."""
        start_time = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        current_time = datetime(2024, 1, 1, 11, 0, 0, tzinfo=timezone.utc)
        
        challenge = create_test_challenge(start_time, end_time)
        remaining = calculate_remaining_time(challenge, current_time)
        
        assert remaining == timedelta(hours=1)
        assert remaining.total_seconds() > 0
    
    def test_ended_challenge_returns_zero(self):
        """Test that an ended challenge returns zero remaining time."""
        start_time = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        current_time = datetime(2024, 1, 1, 13, 0, 0, tzinfo=timezone.utc)
        
        challenge = create_test_challenge(start_time, end_time)
        remaining = calculate_remaining_time(challenge, current_time)
        
        assert remaining == timedelta(0)
    
    def test_challenge_at_exact_end_time_returns_zero(self):
        """Test that a challenge at exact end time returns zero."""
        start_time = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        current_time = end_time
        
        challenge = create_test_challenge(start_time, end_time)
        remaining = calculate_remaining_time(challenge, current_time)
        
        assert remaining == timedelta(0)
    
    def test_challenge_one_second_before_end(self):
        """Test remaining time calculation one second before end."""
        start_time = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        current_time = datetime(2024, 1, 1, 11, 59, 59, tzinfo=timezone.utc)
        
        challenge = create_test_challenge(start_time, end_time)
        remaining = calculate_remaining_time(challenge, current_time)
        
        assert remaining == timedelta(seconds=1)
    
    def test_uses_current_time_if_not_provided(self):
        """Test that function uses current time when not provided."""
        # Create a challenge that ends in the future
        start_time = datetime.now(timezone.utc) - timedelta(hours=1)
        end_time = datetime.now(timezone.utc) + timedelta(hours=1)
        
        challenge = create_test_challenge(start_time, end_time)
        remaining = calculate_remaining_time(challenge)
        
        # Should be approximately 1 hour (with some tolerance for execution time)
        assert timedelta(minutes=59) < remaining <= timedelta(hours=1)


class TestCalculateTimeUntilStart:
    """Unit tests for calculate_time_until_start function."""
    
    def test_future_challenge_returns_positive_time(self):
        """Test that a future challenge returns positive time until start."""
        start_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(2024, 1, 1, 14, 0, 0, tzinfo=timezone.utc)
        current_time = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        
        challenge = create_test_challenge(start_time, end_time)
        time_until_start = calculate_time_until_start(challenge, current_time)
        
        assert time_until_start == timedelta(hours=2)
        assert time_until_start.total_seconds() > 0
    
    def test_started_challenge_returns_zero(self):
        """Test that a started challenge returns zero time until start."""
        start_time = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        current_time = datetime(2024, 1, 1, 11, 0, 0, tzinfo=timezone.utc)
        
        challenge = create_test_challenge(start_time, end_time)
        time_until_start = calculate_time_until_start(challenge, current_time)
        
        assert time_until_start == timedelta(0)
    
    def test_challenge_at_exact_start_time_returns_zero(self):
        """Test that a challenge at exact start time returns zero."""
        start_time = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        current_time = start_time
        
        challenge = create_test_challenge(start_time, end_time)
        time_until_start = calculate_time_until_start(challenge, current_time)
        
        assert time_until_start == timedelta(0)
    
    def test_challenge_one_second_before_start(self):
        """Test time until start calculation one second before start."""
        start_time = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        current_time = datetime(2024, 1, 1, 9, 59, 59, tzinfo=timezone.utc)
        
        challenge = create_test_challenge(start_time, end_time)
        time_until_start = calculate_time_until_start(challenge, current_time)
        
        assert time_until_start == timedelta(seconds=1)


class TestIsChallengeActive:
    """Unit tests for is_challenge_active function."""
    
    def test_active_challenge_returns_true(self):
        """Test that an active challenge returns True."""
        start_time = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        current_time = datetime(2024, 1, 1, 11, 0, 0, tzinfo=timezone.utc)
        
        challenge = create_test_challenge(start_time, end_time)
        
        assert is_challenge_active(challenge, current_time) is True
    
    def test_not_started_challenge_returns_false(self):
        """Test that a not-yet-started challenge returns False."""
        start_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(2024, 1, 1, 14, 0, 0, tzinfo=timezone.utc)
        current_time = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        
        challenge = create_test_challenge(start_time, end_time)
        
        assert is_challenge_active(challenge, current_time) is False
    
    def test_ended_challenge_returns_false(self):
        """Test that an ended challenge returns False."""
        start_time = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        current_time = datetime(2024, 1, 1, 13, 0, 0, tzinfo=timezone.utc)
        
        challenge = create_test_challenge(start_time, end_time)
        
        assert is_challenge_active(challenge, current_time) is False
    
    def test_challenge_at_start_time_is_active(self):
        """Test that a challenge at exact start time is active."""
        start_time = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        current_time = start_time
        
        challenge = create_test_challenge(start_time, end_time)
        
        assert is_challenge_active(challenge, current_time) is True
    
    def test_challenge_at_end_time_is_not_active(self):
        """Test that a challenge at exact end time is not active."""
        start_time = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        current_time = end_time
        
        challenge = create_test_challenge(start_time, end_time)
        
        assert is_challenge_active(challenge, current_time) is False


class TestMarkChallengeAsEnded:
    """Unit tests for mark_challenge_as_ended function."""
    
    def test_ended_challenge_returns_true(self):
        """Test that an ended challenge returns True."""
        start_time = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        current_time = datetime(2024, 1, 1, 13, 0, 0, tzinfo=timezone.utc)
        
        challenge = create_test_challenge(start_time, end_time)
        
        assert mark_challenge_as_ended(challenge, current_time) is True
    
    def test_active_challenge_returns_false(self):
        """Test that an active challenge returns False."""
        start_time = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        current_time = datetime(2024, 1, 1, 11, 0, 0, tzinfo=timezone.utc)
        
        challenge = create_test_challenge(start_time, end_time)
        
        assert mark_challenge_as_ended(challenge, current_time) is False
    
    def test_not_started_challenge_returns_false(self):
        """Test that a not-yet-started challenge returns False."""
        start_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(2024, 1, 1, 14, 0, 0, tzinfo=timezone.utc)
        current_time = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        
        challenge = create_test_challenge(start_time, end_time)
        
        assert mark_challenge_as_ended(challenge, current_time) is False
    
    def test_challenge_at_exact_end_time_returns_true(self):
        """Test that a challenge at exact end time returns True."""
        start_time = datetime(2024, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        current_time = end_time
        
        challenge = create_test_challenge(start_time, end_time)
        
        assert mark_challenge_as_ended(challenge, current_time) is True


# Property-Based Tests

@given(
    start_time=datetime_strategy,
    duration=st.timedeltas(min_value=timedelta(minutes=1), max_value=timedelta(days=7)),
    time_offset=st.timedeltas(min_value=timedelta(0), max_value=timedelta(days=1)),
)
def test_property_remaining_time_calculation(start_time, duration, time_offset):
    """
    Property 21: Remaining Time Calculation
    
    For any active challenge (start_time < current_time < end_time),
    calculating remaining time should return end_time minus current_time.
    
    **Validates: Requirements 8.1**
    """
    end_time = start_time + duration
    current_time = start_time + time_offset
    
    # Only test when challenge is active
    if current_time >= end_time:
        return
    
    challenge = create_test_challenge(start_time, end_time)
    remaining = calculate_remaining_time(challenge, current_time)
    expected_remaining = end_time - current_time
    
    assert remaining == expected_remaining
    assert remaining.total_seconds() > 0


@given(
    start_time=datetime_strategy,
    duration=st.timedeltas(min_value=timedelta(minutes=1), max_value=timedelta(days=7)),
    time_before_start=st.timedeltas(min_value=timedelta(0), max_value=timedelta(days=1)),
)
def test_property_time_until_start_calculation(start_time, duration, time_before_start):
    """
    Property 23: Time Until Start Calculation
    
    For any challenge that has not started (current_time < start_time),
    calculating time until start should return start_time minus current_time.
    
    **Validates: Requirements 8.5**
    """
    end_time = start_time + duration
    current_time = start_time - time_before_start
    
    challenge = create_test_challenge(start_time, end_time)
    time_until_start = calculate_time_until_start(challenge, current_time)
    expected_time = start_time - current_time
    
    assert time_until_start == expected_time
    assert time_until_start.total_seconds() >= 0


@given(
    start_time=datetime_strategy,
    duration=st.timedeltas(min_value=timedelta(minutes=1), max_value=timedelta(days=7)),
    current_time=datetime_strategy,
)
def test_property_challenge_status_transition(start_time, duration, current_time):
    """
    Property 22: Challenge Status Transition at End Time
    
    For any challenge where current_time >= end_time,
    the challenge status should be marked as ended.
    
    **Validates: Requirements 8.3**
    """
    end_time = start_time + duration
    challenge = create_test_challenge(start_time, end_time)
    
    should_be_ended = mark_challenge_as_ended(challenge, current_time)
    
    if current_time >= end_time:
        assert should_be_ended is True
    else:
        assert should_be_ended is False


@given(
    start_time=datetime_strategy,
    duration=st.timedeltas(min_value=timedelta(minutes=1), max_value=timedelta(days=7)),
    current_time=datetime_strategy,
)
def test_property_challenge_active_status(start_time, duration, current_time):
    """
    Property: Challenge Active Status
    
    A challenge is active if and only if start_time <= current_time < end_time.
    
    **Validates: Requirements 8.4**
    """
    end_time = start_time + duration
    challenge = create_test_challenge(start_time, end_time)
    
    is_active = is_challenge_active(challenge, current_time)
    expected_active = start_time <= current_time < end_time
    
    assert is_active == expected_active


@given(
    start_time=datetime_strategy,
    duration=st.timedeltas(min_value=timedelta(minutes=1), max_value=timedelta(days=7)),
)
def test_property_remaining_time_never_negative(start_time, duration):
    """
    Property: Remaining time should never be negative.
    
    For any challenge and any current time, calculate_remaining_time
    should return a non-negative timedelta.
    """
    end_time = start_time + duration
    # Test with time after end
    current_time = end_time + timedelta(hours=1)
    
    challenge = create_test_challenge(start_time, end_time)
    remaining = calculate_remaining_time(challenge, current_time)
    
    assert remaining.total_seconds() >= 0


@given(
    start_time=datetime_strategy,
    duration=st.timedeltas(min_value=timedelta(minutes=1), max_value=timedelta(days=7)),
)
def test_property_time_until_start_never_negative(start_time, duration):
    """
    Property: Time until start should never be negative.
    
    For any challenge and any current time, calculate_time_until_start
    should return a non-negative timedelta.
    """
    end_time = start_time + duration
    # Test with time after start
    current_time = start_time + timedelta(hours=1)
    
    challenge = create_test_challenge(start_time, end_time)
    time_until_start = calculate_time_until_start(challenge, current_time)
    
    assert time_until_start.total_seconds() >= 0
