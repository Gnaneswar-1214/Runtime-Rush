from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.models import Winner, Submission
from uuid import UUID


class WinnerError(Exception):
    """Raised when winner operation fails"""
    pass


class WinnerManager:
    """Manages winner declaration and leaderboard operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def declare_winner(self, challenge_id: UUID, submission_id: UUID) -> Winner:
        """
        Declare a winner for a challenge atomically using database transaction.
        Uses SELECT FOR UPDATE to prevent race conditions when multiple correct
        submissions arrive simultaneously.
        
        Args:
            challenge_id: UUID of the challenge
            submission_id: UUID of the winning submission
            
        Returns:
            Winner object
            
        Raises:
            WinnerError: If winner already exists, submission not found, or not correct
        """
        try:
            # Start a transaction with SELECT FOR UPDATE to lock the winner row
            # This prevents race conditions when multiple submissions try to declare winner
            existing_winner = (
                self.db.query(Winner)
                .filter(Winner.challenge_id == challenge_id)
                .with_for_update()
                .first()
            )
            
            # If winner already exists, raise error (winner immutability)
            if existing_winner:
                raise WinnerError(
                    f"Winner already declared for challenge {challenge_id}"
                )
            
            # Get the submission
            submission = (
                self.db.query(Submission)
                .filter(Submission.id == submission_id)
                .first()
            )
            
            if not submission:
                raise WinnerError(f"Submission {submission_id} not found")
            
            # Verify submission is correct
            if not submission.is_correct:
                raise WinnerError(
                    f"Submission {submission_id} is not correct and cannot be declared winner"
                )
            
            # Verify submission belongs to the challenge
            if submission.challenge_id != challenge_id:
                raise WinnerError(
                    f"Submission {submission_id} does not belong to challenge {challenge_id}"
                )
            
            # Create winner record
            winner = Winner(
                challenge_id=challenge_id,
                participant_id=submission.participant_id,
                submission_id=submission_id,
                timestamp=submission.timestamp
            )
            
            self.db.add(winner)
            self.db.commit()
            self.db.refresh(winner)
            
            return winner
            
        except IntegrityError as e:
            self.db.rollback()
            # Primary key constraint violation means winner already exists
            raise WinnerError(
                f"Winner already declared for challenge {challenge_id}"
            )
        except WinnerError:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            raise
    
    def get_winner(self, challenge_id: UUID) -> Optional[Winner]:
        """
        Retrieve the winner for a challenge.
        
        Args:
            challenge_id: UUID of the challenge
            
        Returns:
            Winner object or None if no winner declared yet
        """
        return (
            self.db.query(Winner)
            .filter(Winner.challenge_id == challenge_id)
            .first()
        )
    
    def get_leaderboard(self, challenge_id: UUID) -> List[Submission]:
        """
        Get all correct submissions for a challenge ordered chronologically.
        The first submission in the list is the winner (earliest timestamp).
        
        Args:
            challenge_id: UUID of the challenge
            
        Returns:
            List of correct Submission objects ordered by timestamp (earliest first)
        """
        return (
            self.db.query(Submission)
            .filter(
                Submission.challenge_id == challenge_id,
                Submission.is_correct == True
            )
            .order_by(Submission.timestamp.asc())
            .all()
        )
