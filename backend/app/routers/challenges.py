from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime

from app.database import get_db
from app.managers.challenge_manager import ChallengeManager, ValidationError
from app.models import Challenge

router = APIRouter(prefix="/api/challenges", tags=["challenges"])


# Pydantic schemas for request/response
class CodeFragmentSchema(BaseModel):
    content: str
    original_order: int


class TestCaseSchema(BaseModel):
    input: str
    expected_output: str
    visible: bool = True


class ChallengeCreateSchema(BaseModel):
    title: str
    description: str
    language: str
    correct_solution: str = ""
    start_time: datetime
    end_time: datetime
    created_by: UUID | None = None
    fragments: List[CodeFragmentSchema] = []
    test_cases: List[TestCaseSchema]


class ChallengeUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    language: str | None = None
    correct_solution: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    fragments: List[CodeFragmentSchema] | None = None
    test_cases: List[TestCaseSchema] | None = None


class CodeFragmentResponse(BaseModel):
    id: UUID
    content: str
    original_order: int
    
    class Config:
        from_attributes = True


class TestCaseResponse(BaseModel):
    id: UUID
    input: str
    expected_output: str
    visible: bool
    
    class Config:
        from_attributes = True


class ChallengeResponse(BaseModel):
    id: UUID
    title: str
    description: str
    language: str
    correct_solution: str
    start_time: datetime
    end_time: datetime
    created_by: UUID | None
    created_at: datetime
    fragments: List[CodeFragmentResponse]
    test_cases: List[TestCaseResponse]
    
    class Config:
        from_attributes = True


@router.post("", response_model=ChallengeResponse, status_code=status.HTTP_201_CREATED)
async def create_challenge(
    challenge_data: ChallengeCreateSchema,
    db: Session = Depends(get_db)
):
    """Create a new challenge"""
    manager = ChallengeManager(db)
    
    try:
        # Convert Pydantic model to dict
        challenge_dict = challenge_data.model_dump()
        
        # Convert nested models to dicts
        challenge_dict["fragments"] = [f.model_dump() for f in challenge_data.fragments]
        challenge_dict["test_cases"] = [tc.model_dump() for tc in challenge_data.test_cases]
        
        challenge = manager.create_challenge(challenge_dict)
        return challenge
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{challenge_id}", response_model=ChallengeResponse)
async def get_challenge(
    challenge_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a challenge by ID"""
    manager = ChallengeManager(db)
    
    challenge = manager.get_challenge(challenge_id)
    if not challenge:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found")
    
    return challenge


@router.get("", response_model=List[ChallengeResponse])
async def list_challenges(
    db: Session = Depends(get_db)
):
    """List all challenges"""
    manager = ChallengeManager(db)
    challenges = manager.list_challenges()
    return challenges


@router.put("/{challenge_id}", response_model=ChallengeResponse)
async def update_challenge(
    challenge_id: UUID,
    updates: ChallengeUpdateSchema,
    db: Session = Depends(get_db)
):
    """Update a challenge"""
    manager = ChallengeManager(db)
    
    try:
        # Convert Pydantic model to dict, excluding None values
        updates_dict = updates.model_dump(exclude_none=True)
        
        # Convert nested models to dicts if present
        if "fragments" in updates_dict and updates.fragments is not None:
            updates_dict["fragments"] = [f.model_dump() for f in updates.fragments]
        if "test_cases" in updates_dict and updates.test_cases is not None:
            updates_dict["test_cases"] = [tc.model_dump() for tc in updates.test_cases]
        
        challenge = manager.update_challenge(challenge_id, updates_dict)
        if not challenge:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found")
        
        return challenge
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{challenge_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_challenge(
    challenge_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete a challenge"""
    manager = ChallengeManager(db)
    
    deleted = manager.delete_challenge(challenge_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge not found")
    
    return None
