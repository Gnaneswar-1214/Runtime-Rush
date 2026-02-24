from app.database import SessionLocal
from app.models_sqlite import Challenge

db = SessionLocal()

try:
    # Get all challenges
    challenges = db.query(Challenge).all()
    
    print(f"Found {len(challenges)} challenges")
    
    # Update levels based on title
    for challenge in challenges:
        if "Level 1" in challenge.title or "Print Your Name" in challenge.title or "Add Two Numbers" in challenge.title:
            challenge.level = 1
            print(f"Updated '{challenge.title}' to Level 1")
        elif "Level 2" in challenge.title or "Level 3" in challenge.title or "Find Maximum" in challenge.title or "Reverse a String" in challenge.title:
            challenge.level = 2
            print(f"Updated '{challenge.title}' to Level 2")
        elif "Level 4" in challenge.title or "Level 5" in challenge.title or "Level 6" in challenge.title or "Count Vowels" in challenge.title or "Fibonacci" in challenge.title:
            challenge.level = 3
            print(f"Updated '{challenge.title}' to Level 3")
        else:
            challenge.level = 1
            print(f"Updated '{challenge.title}' to Level 1 (default)")
    
    db.commit()
    print("\n✅ All challenges updated successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
