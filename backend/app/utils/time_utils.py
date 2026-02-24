"""
Time calculation utilities for challenge management.

This module provides functions for calculating time-related information
for challenges, including remaining time, time until start, and challenge
status determination.
"""

from datetime import datetime, timezone, timedelta
from typing import Optional
from app.models.challenge import Challenge


def calculate_remaining_time(challenge: Challenge, current_time: Optional[datetime] = None) -> timedelta:
    """
    Calculate the remaining time for an active challenge.
    
    For any active challenge (start_time < current_time < end_time),
    returns end_time minus current_time.
    
    Args:
        challenge: The challenge to calculate remaining time for
        current_time: The current time (defaults to now if not provided)
    
    Returns:
        timedelta representing the remaining time
        Returns timedelta(0) if the challenge has ended
        Returns negative timedelta if current_time is before start_time
    
    Validates: Requirements 8.1
    """
    if current_time is None:
        current_time = datetime.now(timezone.utc)
    
    # Ensure current_time is timezone-aware
    if current_time.tzinfo is None:
        current_time = current_time.replace(tzinfo=timezone.utc)
    
    remaining = challenge.end_time - current_time
    
    # If challenge has ended, return zero
    if remaining.total_seconds() < 0:
        return timedelta(0)
    
    return remaining


def calculate_time_until_start(challenge: Challenge, current_time: Optional[datetime] = None) -> timedelta:
    """
    Calculate the time until a challenge starts.
    
    For any challenge that has not started (current_time < start_time),
    returns start_time minus current_time.
    
    Args:
        challenge: The challenge to calculate time until start for
        current_time: The current time (defaults to now if not provided)
    
    Returns:
        timedelta representing the time until start
        Returns timedelta(0) if the challenge has already started
    
    Validates: Requirements 8.5
    """
    if current_time is None:
        current_time = datetime.now(timezone.utc)
    
    # Ensure current_time is timezone-aware
    if current_time.tzinfo is None:
        current_time = current_time.replace(tzinfo=timezone.utc)
    
    time_until_start = challenge.start_time - current_time
    
    # If challenge has already started, return zero
    if time_until_start.total_seconds() < 0:
        return timedelta(0)
    
    return time_until_start


def is_challenge_active(challenge: Challenge, current_time: Optional[datetime] = None) -> bool:
    """
    Determine if a challenge is currently active.
    
    A challenge is active when:
    start_time <= current_time < end_time
    
    Args:
        challenge: The challenge to check
        current_time: The current time (defaults to now if not provided)
    
    Returns:
        True if the challenge is active, False otherwise
    
    Validates: Requirements 8.4
    """
    if current_time is None:
        current_time = datetime.now(timezone.utc)
    
    # Ensure current_time is timezone-aware
    if current_time.tzinfo is None:
        current_time = current_time.replace(tzinfo=timezone.utc)
    
    return challenge.start_time <= current_time < challenge.end_time


def mark_challenge_as_ended(challenge: Challenge, current_time: Optional[datetime] = None) -> bool:
    """
    Check if a challenge should be marked as ended.
    
    For any challenge where current_time >= end_time, returns True
    indicating the challenge status should be marked as ended.
    
    Note: This function only checks the condition. The actual status
    update should be handled by the caller (e.g., ChallengeManager).
    
    Args:
        challenge: The challenge to check
        current_time: The current time (defaults to now if not provided)
    
    Returns:
        True if the challenge should be marked as ended, False otherwise
    
    Validates: Requirements 8.3
    """
    if current_time is None:
        current_time = datetime.now(timezone.utc)
    
    # Ensure current_time is timezone-aware
    if current_time.tzinfo is None:
        current_time = current_time.replace(tzinfo=timezone.utc)
    
    return current_time >= challenge.end_time
