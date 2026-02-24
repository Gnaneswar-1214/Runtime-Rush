from app.database import SessionLocal
from app.models_sqlite import Challenge, User, UserProgress
from datetime import datetime

db = SessionLocal()

try:
    # Check challenges
    challenges = db.query(Challenge).all()
    print(f"📊 Found {len(challenges)} challenges in database:")
    for challenge in challenges:
        print(f"  - {challenge.title} (Level {challenge.level})")
        print(f"    Start: {challenge.start_time}")
        print(f"    End: {challenge.end_time}")
        print(f"    Status: {'Active' if challenge.start_time <= datetime.now() <= challenge.end_time else 'Inactive'}")
        print()
    
    # Check users
    users = db.query(User).all()
    print(f"👥 Found {len(users)} users in database:")
    for user in users:
        progress = db.query(UserProgress).filter(UserProgress.user_id == user.id).first()
        current_level = progress.current_level if progress else 1
        print(f"  - {user.username} (Level {current_level}, Role: {user.role})")
    
finally:
    db.close()