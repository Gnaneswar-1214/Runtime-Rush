from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from app.database import get_db
from app.managers.submission_manager import SubmissionManager, SubmissionError

router = APIRouter(prefix="/api", tags=["submissions"])


# Pydantic schemas for request/response
class SubmissionCreateSchema(BaseModel):
    code: str
    participant_id: UUID


class ValidationResultSchema(BaseModel):
    isValid: bool
    syntaxErrors: List[dict]
    testResults: List[dict]
    allTestsPassed: bool


class SubmissionResponse(BaseModel):
    id: UUID
    challenge_id: UUID
    participant_id: UUID
    code: str
    timestamp: datetime
    is_correct: bool
    validation_result: dict
    
    class Config:
        from_attributes = True


@router.post(
    "/challenges/{challenge_id}/submit",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED
)
async def submit_code(
    challenge_id: UUID,
    submission_data: SubmissionCreateSchema,
    db: Session = Depends(get_db)
):
    """
    Submit code for a challenge.
    
    Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6
    """
    manager = SubmissionManager(db)
    
    try:
        submission = manager.submit_code(
            challenge_id=challenge_id,
            participant_id=submission_data.participant_id,
            code=submission_data.code
        )
        return submission
    except SubmissionError as e:
        error_msg = str(e)
        if "not found" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_msg
            )
        elif "has ended" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=error_msg
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/submissions/{submission_id}",
    response_model=SubmissionResponse
)
async def get_submission(
    submission_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get a submission by ID.
    
    Requirements: 6.1, 6.2, 6.3, 6.4
    """
    manager = SubmissionManager(db)
    
    submission = manager.get_submission(submission_id)
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    
    return submission


@router.get(
    "/challenges/{challenge_id}/submissions",
    response_model=List[SubmissionResponse]
)
async def get_challenge_submissions(
    challenge_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get all submissions for a challenge.
    
    Requirements: 6.1, 6.2, 6.3, 6.4, 6.5
    """
    manager = SubmissionManager(db)
    
    submissions = manager.get_submissions_by_challenge(challenge_id)
    return submissions


@router.get(
    "/participants/{participant_id}/submissions",
    response_model=List[SubmissionResponse]
)
async def get_participant_submissions(
    participant_id: UUID,
    challenge_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get all submissions by a participant for a specific challenge.
    
    Requirements: 6.1, 6.2, 6.3, 6.4, 6.5
    """
    manager = SubmissionManager(db)
    
    submissions = manager.get_submissions_by_participant(
        participant_id=participant_id,
        challenge_id=challenge_id
    )
    return submissions
