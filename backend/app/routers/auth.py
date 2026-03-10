from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid
import hashlib

from app.database import get_db
from app.models_sqlite import User, UserProgress

router = APIRouter(prefix="/api/auth", tags=["authentication"])

# Pydantic schemas
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: str
    current_level: int
    
    class Config:
        from_attributes = True

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Create new user
    user_id = str(uuid.uuid4())
    new_user = User(
        id=user_id,
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role='participant'
    )
    db.add(new_user)
    
    # Create user progress
    progress = UserProgress(
        id=str(uuid.uuid4()),
        user_id=user_id,
        current_level=1
    )
    db.add(progress)
    
    db.commit()
    db.refresh(new_user)
    db.refresh(progress)
    
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "role": new_user.role,
        "current_level": progress.current_level
    }

@router.post("/login", response_model=UserResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user or user.password_hash != hash_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Update last login
    user.last_login = datetime.now()
    db.commit()
    
    # Get user progress
    progress = db.query(UserProgress).filter(UserProgress.user_id == user.id).first()
    if not progress:
        progress = UserProgress(
            id=str(uuid.uuid4()),
            user_id=user.id,
            current_level=1
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "current_level": progress.current_level
    }

@router.get("/users/{user_id}/progress")
async def get_user_progress(user_id: str, db: Session = Depends(get_db)):
    progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    
    return {
        "user_id": progress.user_id,
        "current_level": progress.current_level,
        "level1_completed": progress.level1_completed,
        "level2_completed": progress.level2_completed,
        "level3_completed": progress.level3_completed,
        "level1_language": progress.level1_language,
        "level2_language": progress.level2_language,
        "level3_language": progress.level3_language,
        "total_score": progress.total_score
    }

@router.post("/users/{user_id}/select-language/{level}")
async def select_language(user_id: str, level: int, language: str, db: Session = Depends(get_db)):
    """Select language for a specific level. Can only be done once per level."""
    progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    
    # Validate language
    valid_languages = ["python", "c", "java", "cpp"]
    if language not in valid_languages:
        raise HTTPException(status_code=400, detail=f"Invalid language. Must be one of: {', '.join(valid_languages)}")
    
    # Check if language already selected for this level
    if level == 1:
        if progress.level1_language:
            raise HTTPException(status_code=400, detail="Language already selected for Level 1")
        progress.level1_language = language
    elif level == 2:
        if progress.level2_language:
            raise HTTPException(status_code=400, detail="Language already selected for Level 2")
        if not progress.level1_completed:
            raise HTTPException(status_code=400, detail="Must complete Level 1 first")
        progress.level2_language = language
    elif level == 3:
        if progress.level3_language:
            raise HTTPException(status_code=400, detail="Language already selected for Level 3")
        if not progress.level2_completed:
            raise HTTPException(status_code=400, detail="Must complete Level 2 first")
        progress.level3_language = language
    else:
        raise HTTPException(status_code=400, detail="Invalid level")
    
    db.commit()
    
    return {
        "message": f"Language {language} selected for Level {level}",
        "level": level,
        "language": language
    }

@router.post("/users/{user_id}/complete-level/{level}")
async def complete_level(user_id: str, level: int, time_taken: int = 180, db: Session = Depends(get_db)):
    progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    
    # Check if level already completed
    if level == 1 and progress.level1_completed:
        raise HTTPException(status_code=400, detail="Level 1 already completed")
    elif level == 2 and progress.level2_completed:
        raise HTTPException(status_code=400, detail="Level 2 already completed")
    elif level == 3 and progress.level3_completed:
        raise HTTPException(status_code=400, detail="Level 3 already completed")
    
    # Calculate score based on time taken
    # Each level: 100 marks, 180 seconds
    # Score = 100 - (time_taken × 0.5556)
    # Minimum score: 0
    marks_per_second = 100.0 / 180.0  # 0.5556
    score = max(0, 100 - (time_taken * marks_per_second))
    score = round(score, 2)  # Round to 2 decimal places
    
    # Count submission order
    if level == 1:
        submission_order = db.query(UserProgress).filter(UserProgress.level1_completed == True).count() + 1
        progress.level1_completed = True
        progress.level1_score = score
        progress.level1_time_taken = time_taken
        progress.level1_submission_order = submission_order
        progress.current_level = 2
    elif level == 2:
        if not progress.level1_completed:
            raise HTTPException(status_code=400, detail="Must complete Level 1 first")
        submission_order = db.query(UserProgress).filter(UserProgress.level2_completed == True).count() + 1
        progress.level2_completed = True
        progress.level2_score = score
        progress.level2_time_taken = time_taken
        progress.level2_submission_order = submission_order
        progress.current_level = 3
    elif level == 3:
        if not progress.level2_completed:
            raise HTTPException(status_code=400, detail="Must complete Level 2 first")
        submission_order = db.query(UserProgress).filter(UserProgress.level3_completed == True).count() + 1
        progress.level3_completed = True
        progress.level3_score = score
        progress.level3_time_taken = time_taken
        progress.level3_submission_order = submission_order
    
    # Update total score
    progress.total_score = progress.level1_score + progress.level2_score + progress.level3_score
    db.commit()
    
    return {
        "message": f"Level {level} completed!",
        "current_level": progress.current_level,
        "score": score,
        "time_taken": time_taken,
        "submission_order": submission_order,
        "total_score": progress.total_score
    }

@router.get("/leaderboard")
async def get_leaderboard(db: Session = Depends(get_db)):
    # Get all users who completed all 3 levels
    completed_users = db.query(UserProgress, User).join(
        User, UserProgress.user_id == User.id
    ).filter(
        UserProgress.level1_completed == True,
        UserProgress.level2_completed == True,
        UserProgress.level3_completed == True
    ).order_by(
        UserProgress.total_score.desc(),
        UserProgress.level3_submission_order.asc()
    ).all()
    
    leaderboard = []
    for rank, (progress, user) in enumerate(completed_users, start=1):
        total_time = (progress.level1_time_taken or 0) + (progress.level2_time_taken or 0) + (progress.level3_time_taken or 0)
        leaderboard.append({
            "rank": rank,
            "username": user.username,
            "total_score": round(progress.total_score, 2),
            "level1_score": round(progress.level1_score, 2),
            "level2_score": round(progress.level2_score, 2),
            "level3_score": round(progress.level3_score, 2),
            "total_time": total_time,
            "level1_time": progress.level1_time_taken,
            "level2_time": progress.level2_time_taken,
            "level3_time": progress.level3_time_taken,
            "tab_switch_count": progress.tab_switch_count or 0
        })
    
    return {"leaderboard": leaderboard}


@router.post("/users/{user_id}/tab-switch")
async def record_tab_switch(user_id: str, db: Session = Depends(get_db)):
    """Record a tab switch violation for a user"""
    progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    
    # Increment tab switch count
    progress.tab_switch_count += 1
    db.commit()
    
    return {
        "tab_switch_count": progress.tab_switch_count,
        "message": f"Tab switch recorded. Total violations: {progress.tab_switch_count}"
    }

@router.get("/users/{user_id}/tab-switches")
async def get_tab_switches(user_id: str, db: Session = Depends(get_db)):
    """Get tab switch count for a user"""
    progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    
    return {
        "tab_switch_count": progress.tab_switch_count
    }
