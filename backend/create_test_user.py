from app.database import SessionLocal
from app.models_sqlite import User, UserProgress
import uuid
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

db = SessionLocal()

try:
    # Check if test user already exists
    existing_user = db.query(User).filter(User.username == 'testuser').first()
    if existing_user:
        print("Test user already exists!")
        # Check progress
        progress = db.query(UserProgress).filter(UserProgress.user_id == existing_user.id).first()
        if progress:
            print(f"Current level: {progress.current_level}")
        else:
            print("No progress found, creating...")
            progress = UserProgress(
                id=str(uuid.uuid4()),
                user_id=existing_user.id,
                current_level=1
            )
            db.add(progress)
            db.commit()
            print("Progress created!")
    else:
        # Create test user
        user_id = str(uuid.uuid4())
        test_user = User(
            id=user_id,
            username='testuser',
            email='test@example.com',
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
        print("✅ Test user created!")
        print("Username: testuser")
        print("Password: password123")
        print("Level: 1")

finally:
    db.close()