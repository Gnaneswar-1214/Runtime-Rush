from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import Challenge, CodeFragment, TestCase
from uuid import UUID
import random


class ValidationError(Exception):
    """Raised when challenge validation fails"""
    pass


class ChallengeManager:
    """Manages challenge CRUD operations and validation"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def validate_challenge(self, challenge_data: dict) -> None:
        """
        Validate challenge data for required fields and constraints.
        
        Args:
            challenge_data: Dictionary containing challenge fields
            
        Raises:
            ValidationError: If validation fails
        """
        # Check required fields
        required_fields = ["title", "description", "language"]
        missing_fields = [field for field in required_fields if not challenge_data.get(field)]
        
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Validate title is not empty
        if not challenge_data.get("title", "").strip():
            raise ValidationError("Title cannot be empty")
        
        # Validate description is not empty
        if not challenge_data.get("description", "").strip():
            raise ValidationError("Description cannot be empty")
        
        # Validate language is not empty
        if not challenge_data.get("language", "").strip():
            raise ValidationError("Language cannot be empty")
        
        # Validate test cases exist
        test_cases = challenge_data.get("test_cases", [])
        if not test_cases or len(test_cases) == 0:
            raise ValidationError("At least one test case is required")
        
        # Validate time range if both times are provided
        start_time = challenge_data.get("start_time")
        end_time = challenge_data.get("end_time")
        if start_time and end_time:
            if isinstance(start_time, str):
                start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            if isinstance(end_time, str):
                end_time = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            
            if start_time >= end_time:
                raise ValidationError("Start time must be before end time")
    
    def create_challenge(self, challenge_data: dict) -> Challenge:
        """
        Create a new challenge with fragments and test cases.
        
        Args:
            challenge_data: Dictionary containing challenge fields including:
                - title: str
                - description: str
                - language: str
                - correct_solution: str
                - start_time: datetime
                - end_time: datetime
                - created_by: UUID (optional)
                - fragments: List[dict] with 'content' and 'original_order'
                - test_cases: List[dict] with 'input', 'expected_output', 'visible'
        
        Returns:
            Created Challenge object
            
        Raises:
            ValidationError: If validation fails
        """
        # Validate challenge data
        self.validate_challenge(challenge_data)
        
        try:
            # Create challenge
            challenge = Challenge(
                title=challenge_data["title"],
                description=challenge_data["description"],
                language=challenge_data["language"],
                correct_solution=challenge_data.get("correct_solution", ""),
                start_time=challenge_data.get("start_time"),
                end_time=challenge_data.get("end_time"),
                created_by=challenge_data.get("created_by")
            )
            
            self.db.add(challenge)
            self.db.flush()  # Get the challenge ID
            
            # Create fragments
            fragments_data = challenge_data.get("fragments", [])
            for fragment_data in fragments_data:
                fragment = CodeFragment(
                    challenge_id=challenge.id,
                    content=fragment_data["content"],
                    original_order=fragment_data["original_order"]
                )
                self.db.add(fragment)
            
            # Create test cases
            test_cases_data = challenge_data.get("test_cases", [])
            for test_case_data in test_cases_data:
                test_case = TestCase(
                    challenge_id=challenge.id,
                    input=test_case_data["input"],
                    expected_output=test_case_data["expected_output"],
                    visible=test_case_data.get("visible", True)
                )
                self.db.add(test_case)
            
            self.db.commit()
            self.db.refresh(challenge)
            
            return challenge
            
        except IntegrityError as e:
            self.db.rollback()
            raise ValidationError(f"Database integrity error: {str(e)}")
        except Exception as e:
            self.db.rollback()
            raise
    
    def get_challenge(self, challenge_id: UUID, scramble_fragments: bool = False, 
                     filter_test_cases: bool = False) -> Optional[Challenge]:
        """
        Retrieve a challenge by ID.
        
        Args:
            challenge_id: UUID of the challenge
            scramble_fragments: If True, randomize the order of fragments for participants
            filter_test_cases: If True, filter test cases for participant view:
                - Only return visible test cases
                - Clear expected_output from visible test cases
            
        Returns:
            Challenge object or None if not found
        """
        # Always do a fresh query to avoid session caching issues
        challenge = self.db.query(Challenge).filter(Challenge.id == challenge_id).first()
        
        if not challenge:
            return None
            
        if scramble_fragments and challenge.fragments:
            # Load fragments into memory
            fragments_list = list(challenge.fragments)
            # Create a shuffled copy
            shuffled = fragments_list.copy()
            random.shuffle(shuffled)
            # Replace the relationship with the shuffled list
            # This only affects this instance, not the database
            challenge.fragments = shuffled
            # Mark the challenge as detached so subsequent queries get fresh data
            self.db.expunge(challenge)
        
        if filter_test_cases and challenge.test_cases:
            # Load test cases into memory
            test_cases_list = list(challenge.test_cases)
            # Filter to only visible test cases
            visible_test_cases = [tc for tc in test_cases_list if tc.visible]
            # Clear expected outputs from visible test cases
            for tc in visible_test_cases:
                tc.expected_output = ""
            # Replace the relationship with filtered test cases
            challenge.test_cases = visible_test_cases
            # Mark the challenge as detached so subsequent queries get fresh data
            self.db.expunge(challenge)
        
        return challenge
    
    def update_challenge(self, challenge_id: UUID, updates: dict) -> Optional[Challenge]:
        """
        Update an existing challenge.
        
        Args:
            challenge_id: UUID of the challenge to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated Challenge object or None if not found
            
        Raises:
            ValidationError: If validation fails
        """
        challenge = self.get_challenge(challenge_id)
        if not challenge:
            return None
        
        # Merge existing data with updates for validation
        challenge_data = {
            "title": updates.get("title", challenge.title),
            "description": updates.get("description", challenge.description),
            "language": updates.get("language", challenge.language),
            "start_time": updates.get("start_time", challenge.start_time),
            "end_time": updates.get("end_time", challenge.end_time),
            "test_cases": updates.get("test_cases", challenge.test_cases)
        }
        
        # Validate the updated data
        self.validate_challenge(challenge_data)
        
        try:
            # Update basic fields
            if "title" in updates:
                challenge.title = updates["title"]
            if "description" in updates:
                challenge.description = updates["description"]
            if "language" in updates:
                challenge.language = updates["language"]
            if "correct_solution" in updates:
                challenge.correct_solution = updates["correct_solution"]
            if "start_time" in updates:
                challenge.start_time = updates["start_time"]
            if "end_time" in updates:
                challenge.end_time = updates["end_time"]
            
            # Update fragments if provided
            if "fragments" in updates:
                # Delete existing fragments
                self.db.query(CodeFragment).filter(
                    CodeFragment.challenge_id == challenge_id
                ).delete()
                
                # Add new fragments
                for fragment_data in updates["fragments"]:
                    fragment = CodeFragment(
                        challenge_id=challenge_id,
                        content=fragment_data["content"],
                        original_order=fragment_data["original_order"]
                    )
                    self.db.add(fragment)
            
            # Update test cases if provided
            if "test_cases" in updates:
                # Delete existing test cases
                self.db.query(TestCase).filter(
                    TestCase.challenge_id == challenge_id
                ).delete()
                
                # Add new test cases
                for test_case_data in updates["test_cases"]:
                    test_case = TestCase(
                        challenge_id=challenge_id,
                        input=test_case_data["input"],
                        expected_output=test_case_data["expected_output"],
                        visible=test_case_data.get("visible", True)
                    )
                    self.db.add(test_case)
            
            self.db.commit()
            self.db.refresh(challenge)
            
            return challenge
            
        except IntegrityError as e:
            self.db.rollback()
            raise ValidationError(f"Database integrity error: {str(e)}")
        except Exception as e:
            self.db.rollback()
            raise
    
    def delete_challenge(self, challenge_id: UUID) -> bool:
        """
        Delete a challenge by ID.
        
        Args:
            challenge_id: UUID of the challenge to delete
            
        Returns:
            True if deleted, False if not found
        """
        challenge = self.get_challenge(challenge_id)
        if not challenge:
            return False
        
        try:
            self.db.delete(challenge)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise
    
    def list_challenges(self) -> List[Challenge]:
        """
        List all challenges.
        
        Returns:
            List of Challenge objects
        """
        return self.db.query(Challenge).all()
