"""
Initialize database with admin user and challenges for Railway deployment
Run this ONCE after deploying to Railway
"""
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models_sqlite import User, Challenge, CodeFragment, UserProgress
import uuid
import hashlib
from datetime import datetime, timedelta

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def init_database():
    print("🚀 Initializing database...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created")
    
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("⚠️ Admin user already exists")
        else:
            # Create admin user
            admin_id = str(uuid.uuid4())
            admin_user = User(
                id=admin_id,
                username="admin",
                email="admin@runtimerush.com",
                password_hash=hash_password("admin123"),
                role='admin'
            )
            db.add(admin_user)
            db.commit()
            print("✅ Admin user created (username: admin, password: admin123)")
        
        # Check if challenges already exist
        existing_challenges = db.query(Challenge).count()
        if existing_challenges > 0:
            print(f"⚠️ {existing_challenges} challenges already exist")
        else:
            # Create challenges for each level
            challenges_data = [
                {
                    "title": "Binary Search Algorithm",
                    "description": "Implement a binary search algorithm to find an element in a sorted array. Arrange the code fragments in the correct order.",
                    "language": "python",
                    "level": 1,
                    "fragments": [
                        "def binary_search(arr, target):",
                        "    left, right = 0, len(arr) - 1",
                        "    while left <= right:",
                        "        mid = (left + right) // 2",
                        "        if arr[mid] == target:",
                        "            return mid",
                        "        elif arr[mid] < target:",
                        "            left = mid + 1",
                        "        else:",
                        "            right = mid - 1",
                        "    return -1"
                    ]
                },
                {
                    "title": "Quick Sort Algorithm",
                    "description": "Implement the quick sort algorithm to sort an array. Arrange the code fragments in the correct order.",
                    "language": "python",
                    "level": 2,
                    "fragments": [
                        "def quick_sort(arr):",
                        "    if len(arr) <= 1:",
                        "        return arr",
                        "    pivot = arr[len(arr) // 2]",
                        "    left = [x for x in arr if x < pivot]",
                        "    middle = [x for x in arr if x == pivot]",
                        "    right = [x for x in arr if x > pivot]",
                        "    return quick_sort(left) + middle + quick_sort(right)"
                    ]
                },
                {
                    "title": "Merge Sort Algorithm",
                    "description": "Implement the merge sort algorithm to sort an array. Arrange the code fragments in the correct order.",
                    "language": "python",
                    "level": 3,
                    "fragments": [
                        "def merge_sort(arr):",
                        "    if len(arr) <= 1:",
                        "        return arr",
                        "    mid = len(arr) // 2",
                        "    left = merge_sort(arr[:mid])",
                        "    right = merge_sort(arr[mid:])",
                        "    return merge(left, right)",
                        "",
                        "def merge(left, right):",
                        "    result = []",
                        "    i = j = 0",
                        "    while i < len(left) and j < len(right):",
                        "        if left[i] <= right[j]:",
                        "            result.append(left[i])",
                        "            i += 1",
                        "        else:",
                        "            result.append(right[j])",
                        "            j += 1",
                        "    result.extend(left[i:])",
                        "    result.extend(right[j:])",
                        "    return result"
                    ]
                }
            ]
            
            for challenge_data in challenges_data:
                challenge_id = str(uuid.uuid4())
                challenge = Challenge(
                    id=challenge_id,
                    title=challenge_data["title"],
                    description=challenge_data["description"],
                    language=challenge_data["language"],
                    level=challenge_data["level"],
                    correct_solution="\n".join(challenge_data["fragments"]),
                    start_time=datetime.now(),
                    end_time=datetime.now() + timedelta(days=365),
                    created_by=admin_id if 'admin_id' in locals() else str(uuid.uuid4())
                )
                db.add(challenge)
                
                # Add fragments
                for idx, fragment_content in enumerate(challenge_data["fragments"]):
                    fragment = CodeFragment(
                        id=str(uuid.uuid4()),
                        challenge_id=challenge_id,
                        content=fragment_content,
                        original_order=idx + 1
                    )
                    db.add(fragment)
                
                db.commit()
                print(f"✅ Created challenge: {challenge_data['title']} (Level {challenge_data['level']})")
        
        print("\n🎉 Database initialization complete!")
        print("\n📝 Admin credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
