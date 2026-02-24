from app.database import SessionLocal
from app.models_sqlite import User, UserProgress
import uuid
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

db = SessionLocal()

try:
    # Delete old testuser2 if exists
    old_user = db.query(User).filter(User.username == 'testuser2').first()
    if old_user:
        db.query(UserProgress).filter(UserProgress.user_id == old_user.id).delete()
        db.delete(old_user)
        db.commit()
    
    # Create fresh test user
    user_id = str(uuid.uuid4())
    test_user = User(
        id=user_id,
        username='testuser2',
        email='test2@example.com',
        password_hash=hash_password('password123'),
        role='participant'
    )
    db.add(test_user)
    
    # Create progress
    progress = UserProgress(
        id=str(uuid.uuid4()),
        user_id=user_id,
        current_level=1
    )
    db.add(progress)
    
    db.commit()
    print("✅ Fresh test user created!")
    print("Username: testuser2")
    print("Password: password123")
    print("Level: 1")

finally:
    db.close()
