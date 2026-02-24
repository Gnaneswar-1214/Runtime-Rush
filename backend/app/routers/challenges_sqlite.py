from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
import uuid

from app.database import get_db
from app.models_sqlite import Challenge, CodeFragment, TestCase, User

router = APIRouter(prefix="/api/challenges", tags=["challenges"])

# Pydantic schemas
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
    level: int = 1
    fragments: List[CodeFragmentSchema]
    correct_solution: str
    test_cases: List[TestCaseSchema]
    start_time: datetime
    end_time: datetime
    created_by: str

class ChallengeResponse(BaseModel):
    id: str
    title: str
    description: str
    language: str
    level: int = 1
    fragments: List[dict]
    correct_solution: str
    test_cases: List[dict]
    start_time: datetime
    end_time: datetime
    created_by: str

    class Config:
        from_attributes = True

@router.post("", response_model=ChallengeResponse)
async def create_challenge(challenge_data: ChallengeCreateSchema, db: Session = Depends(get_db)):
    import hashlib
    
    # Create or get user
    user = db.query(User).filter(User.id == challenge_data.created_by).first()
    if not user:
        user = User(
            id=challenge_data.created_by,
            username=f"user_{challenge_data.created_by[:8]}",
            email=f"user_{challenge_data.created_by[:8]}@example.com",
            password_hash=hashlib.sha256(b"default123").hexdigest(),
            role="organizer"
        )
        db.add(user)
    
    # Create challenge
    challenge = Challenge(
        id=str(uuid.uuid4()),
        title=challenge_data.title,
        description=challenge_data.description,
        language=challenge_data.language,
        level=challenge_data.level,
        correct_solution=challenge_data.correct_solution,
        start_time=challenge_data.start_time,
        end_time=challenge_data.end_time,
        created_by=challenge_data.created_by
    )
    db.add(challenge)
    
    # Add fragments
    for frag in challenge_data.fragments:
        fragment = CodeFragment(
            id=str(uuid.uuid4()),
            challenge_id=challenge.id,
            content=frag.content,
            original_order=frag.original_order
        )
        db.add(fragment)
    
    # Add test cases
    for tc in challenge_data.test_cases:
        test_case = TestCase(
            id=str(uuid.uuid4()),
            challenge_id=challenge.id,
            input=tc.input,
            expected_output=tc.expected_output,
            visible=tc.visible
        )
        db.add(test_case)
    
    db.commit()
    db.refresh(challenge)
    
    # Build response
    return {
        "id": challenge.id,
        "title": challenge.title,
        "description": challenge.description,
        "language": challenge.language,
        "level": challenge.level,
        "fragments": [{"id": f.id, "content": f.content, "order": f.original_order} for f in challenge.fragments],
        "correct_solution": challenge.correct_solution,
        "test_cases": [{"id": t.id, "input": t.input, "expected_output": t.expected_output, "visible": t.visible} for t in challenge.test_cases],
        "start_time": challenge.start_time,
        "end_time": challenge.end_time,
        "created_by": challenge.created_by
    }

@router.get("", response_model=List[ChallengeResponse])
async def get_challenges(db: Session = Depends(get_db)):
    challenges = db.query(Challenge).all()
    result = []
    for challenge in challenges:
        result.append({
            "id": challenge.id,
            "title": challenge.title,
            "description": challenge.description,
            "language": challenge.language,
            "level": challenge.level,
            "fragments": [{"id": f.id, "content": f.content, "order": f.original_order} for f in challenge.fragments],
            "correct_solution": challenge.correct_solution,
            "test_cases": [{"id": t.id, "input": t.input, "expected_output": t.expected_output, "visible": t.visible} for t in challenge.test_cases],
            "start_time": challenge.start_time,
            "end_time": challenge.end_time,
            "created_by": challenge.created_by
        })
    return result

@router.get("/{challenge_id}", response_model=ChallengeResponse)
async def get_challenge(challenge_id: str, db: Session = Depends(get_db)):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    return {
        "id": challenge.id,
        "title": challenge.title,
        "description": challenge.description,
        "language": challenge.language,
        "level": challenge.level,
        "fragments": [{"id": f.id, "content": f.content, "order": f.original_order} for f in challenge.fragments],
        "correct_solution": challenge.correct_solution,
        "test_cases": [{"id": t.id, "input": t.input, "expected_output": t.expected_output, "visible": t.visible} for t in challenge.test_cases],
        "start_time": challenge.start_time,
        "end_time": challenge.end_time,
        "created_by": challenge.created_by
    }
