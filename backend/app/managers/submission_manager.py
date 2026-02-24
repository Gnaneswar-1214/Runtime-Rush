from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import Submission, Challenge
from uuid import UUID


class SubmissionError(Exception):
    """Raised when submission operation fails"""
    pass


class MockValidationManager:
    """
    Placeholder ValidationManager that returns mock validation results.
    This will be replaced with the actual ValidationManager once Docker sandbox is implemented.
    """
    
    @staticmethod
    def validate_submission(code: str, challenge: Challenge) -> dict:
        """
        Mock validation that returns a simple validation result.
        
        Args:
            code: The submitted code
            challenge: The challenge being validated against
            
        Returns:
            Mock validation result dictionary
        """
        # For now, return a mock validation result
        # In the real implementation, this would execute code in sandbox and run test cases
        return {
            "isValid": True,
            "syntaxErrors": [],
            "testResults": [
                {
                    "testCaseId": str(tc.id),
                    "passed": True,
                    "actualOutput": "mock output",
                    "expectedOutput": tc.expected_output,
                    "executionTime": 0.1,
                }
                for tc in challenge.test_cases
            ],
            "allTestsPassed": True,
        }


class SubmissionManager:
    """Manages code submission operations and validation"""
    
    def __init__(self, db: Session):
        self.db = db
        self.validation_manager = MockValidationManager()
    
    def submit_code(
        self, 
        challenge_id: UUID, 
        participant_id: UUID, 
        code: str
    ) -> Submission:
        """
        Submit code for a challenge with automatic validation.
        
        Args:
            challenge_id: UUID of the challenge
            participant_id: UUID of the participant
            code: The submitted code
            
        Returns:
            Created Submission object with validation results
            
        Raises:
            SubmissionError: If submission is rejected (challenge ended, not found, etc.)
        """
        # Get the challenge
        challenge = self.db.query(Challenge).filter(Challenge.id == challenge_id).first()
        if not challenge:
            raise SubmissionError(f"Challenge {challenge_id} not found")
        
        # Check if challenge has ended
        current_time = datetime.now(timezone.utc)
        if challenge.end_time and current_time > challenge.end_time:
            raise SubmissionError("Challenge has ended")
        
        try:
            # Validate the submission using the validation manager
            validation_result = self.validation_manager.validate_submission(code, challenge)
            
            # Determine if submission is correct
            is_correct = validation_result.get("allTestsPassed", False)
            
            # Create submission with server-side timestamp
            submission = Submission(
                challenge_id=challenge_id,
                participant_id=participant_id,
                code=code,
                is_correct=is_correct,
                validation_result=validation_result,
                # timestamp is set automatically by server_default=func.now()
            )
            
            self.db.add(submission)
            self.db.commit()
            self.db.refresh(submission)
            
            return submission
            
        except IntegrityError as e:
            self.db.rollback()
            raise SubmissionError(f"Database integrity error: {str(e)}")
        except Exception as e:
            self.db.rollback()
            raise
    
    def get_submission(self, submission_id: UUID) -> Optional[Submission]:
        """
        Retrieve a submission by ID.
        
        Args:
            submission_id: UUID of the submission
            
        Returns:
            Submission object or None if not found
        """
        return self.db.query(Submission).filter(Submission.id == submission_id).first()
    
    def get_submissions_by_participant(
        self, 
        participant_id: UUID, 
        challenge_id: UUID
    ) -> List[Submission]:
        """
        Retrieve all submissions by a participant for a specific challenge.
        
        Args:
            participant_id: UUID of the participant
            challenge_id: UUID of the challenge
            
        Returns:
            List of Submission objects ordered by timestamp (newest first)
        """
        return (
            self.db.query(Submission)
            .filter(
                Submission.participant_id == participant_id,
                Submission.challenge_id == challenge_id
            )
            .order_by(Submission.timestamp.desc())
            .all()
        )
    
    def get_submissions_by_challenge(self, challenge_id: UUID) -> List[Submission]:
        """
        Retrieve all submissions for a specific challenge.
        
        Args:
            challenge_id: UUID of the challenge
            
        Returns:
            List of Submission objects ordered by timestamp (oldest first)
        """
        return (
            self.db.query(Submission)
            .filter(Submission.challenge_id == challenge_id)
            .order_by(Submission.timestamp.asc())
            .all()
        )
