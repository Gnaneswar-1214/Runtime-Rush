from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from app.database import get_db
from app.models_sqlite import User, Challenge, UserProgress

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Admin verification (simple check - in production use proper JWT)
def verify_admin(user_id: str, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

@router.get("/users")
async def get_all_users(admin_id: str, db: Session = Depends(get_db)):
    verify_admin(admin_id, db)
    
    users = db.query(User).all()
    result = []
    
    for user in users:
        progress = db.query(UserProgress).filter(UserProgress.user_id == user.id).first()
        result.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "current_level": progress.current_level if progress else 1,
            "level1_completed": progress.level1_completed if progress else False,
            "level2_completed": progress.level2_completed if progress else False,
            "level3_completed": progress.level3_completed if progress else False,
            "level1_score": progress.level1_score if progress else 0,
            "level2_score": progress.level2_score if progress else 0,
            "level3_score": progress.level3_score if progress else 0,
            "level1_time": progress.level1_time_taken if progress else 0,
            "level2_time": progress.level2_time_taken if progress else 0,
            "level3_time": progress.level3_time_taken if progress else 0,
            "level1_submission_order": progress.level1_submission_order if progress else 0,
            "level2_submission_order": progress.level2_submission_order if progress else 0,
            "level3_submission_order": progress.level3_submission_order if progress else 0,
            "total_score": progress.total_score if progress else 0
        })
    
    return result

@router.get("/challenges/by-level/{level}")
async def get_challenges_by_level(level: int, admin_id: str, db: Session = Depends(get_db)):
    verify_admin(admin_id, db)
    
    challenges = db.query(Challenge).filter(Challenge.level == level).all()
    result = []
    
    for challenge in challenges:
        result.append({
            "id": challenge.id,
            "title": challenge.title,
            "description": challenge.description,
            "language": challenge.language,
            "level": challenge.level,
            "fragments_count": len(challenge.fragments),
            "test_cases_count": len(challenge.test_cases),
            "created_at": challenge.created_at.isoformat() if challenge.created_at else None
        })
    
    return result

@router.delete("/challenges/{challenge_id}")
async def delete_challenge(challenge_id: str, admin_id: str, db: Session = Depends(get_db)):
    verify_admin(admin_id, db)
    
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    db.delete(challenge)
    db.commit()
    
    return {"message": "Challenge deleted successfully"}

@router.get("/stats")
async def get_stats(admin_id: str, db: Session = Depends(get_db)):
    verify_admin(admin_id, db)
    
    total_users = db.query(User).filter(User.role == 'participant').count()
    total_challenges = db.query(Challenge).count()
    
    level1_challenges = db.query(Challenge).filter(Challenge.level == 1).count()
    level2_challenges = db.query(Challenge).filter(Challenge.level == 2).count()
    level3_challenges = db.query(Challenge).filter(Challenge.level == 3).count()
    
    users_on_level1 = db.query(UserProgress).filter(UserProgress.current_level == 1).count()
    users_on_level2 = db.query(UserProgress).filter(UserProgress.current_level == 2).count()
    users_on_level3 = db.query(UserProgress).filter(UserProgress.current_level == 3).count()
    
    return {
        "total_users": total_users,
        "total_challenges": total_challenges,
        "challenges_by_level": {
            "level1": level1_challenges,
            "level2": level2_challenges,
            "level3": level3_challenges
        },
        "users_by_level": {
            "level1": users_on_level1,
            "level2": users_on_level2,
            "level3": users_on_level3
        }
    }

@router.delete("/users/{user_id}")
async def terminate_user(user_id: str, admin_id: str, db: Session = Depends(get_db)):
    """Terminate (delete) a user account"""
    verify_admin(admin_id, db)
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.role == 'admin':
        raise HTTPException(status_code=403, detail="Cannot terminate admin users")
    
    # Delete user progress first (foreign key constraint)
    db.query(UserProgress).filter(UserProgress.user_id == user_id).delete()
    
    # Delete user
    db.delete(user)
    db.commit()
    
    return {"message": f"User {user.username} terminated successfully"}

@router.post("/create-admin")
async def create_admin_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    """Create an admin user - use this once to create your first admin"""
    import uuid
    import hashlib
    
    # Check if admin already exists
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user_id = str(uuid.uuid4())
    admin_user = User(
        id=user_id,
        username=username,
        email=email,
        password_hash=hashlib.sha256(password.encode()).hexdigest(),
        role='admin'
    )
    db.add(admin_user)
    db.commit()
    
    return {"message": "Admin created successfully", "id": user_id, "username": username}
