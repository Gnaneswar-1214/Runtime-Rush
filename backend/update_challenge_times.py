from app.database import SessionLocal
from app.models_sqlite import Challenge
from datetime import datetime, timedelta

db = SessionLocal()

try:
    # Get all challenges
    challenges = db.query(Challenge).all()
    
    print(f"Found {len(challenges)} challenges")
    
    # Update times to make them active
    now = datetime.now()
    
    for challenge in challenges:
        # Set start time to now
        challenge.start_time = now
        # Set end time to 2 hours from now
        challenge.end_time = now + timedelta(hours=2)
        
        print(f"Updated '{challenge.title}' - Active until {challenge.end_time.strftime('%H:%M:%S')}")
    
    db.commit()
    print("\n✅ All challenge times updated successfully!")
    print("🎮 All challenges are now ACTIVE for 2 hours!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()