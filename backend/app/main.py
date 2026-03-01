from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import challenges_sqlite, auth, admin

# ✅ IMPORT DB
from app.database import Base, engine

app = FastAPI(title="Runtime Rush API", version="1.0.0")

# ✅ CREATE TABLES ON STARTUP (CRITICAL FOR RAILWAY)
Base.metadata.create_all(bind=engine)

# ✅ Allowed origins - Allow all origins for deployment flexibility
# In production, you should restrict this to your specific domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(challenges_sqlite.router)
app.include_router(auth.router)
app.include_router(admin.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/initialize-db")
async def initialize_database():
    """
    Initialize database with admin user and challenges
    Call this endpoint ONCE after deployment to set up the database
    """
    from app.database import SessionLocal
    from app.models_sqlite import User, Challenge, CodeFragment
    import uuid
    import hashlib
    from datetime import datetime, timedelta
    
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    db = SessionLocal()
    results = {"admin_created": False, "challenges_created": 0, "errors": []}
    
    try:
        # Create admin if doesn't exist
        existing_admin = db.query(User).filter(User.username == "mouniadmin").first()
        if not existing_admin:
            admin_id = str(uuid.uuid4())
            admin_user = User(
                id=admin_id,
                username="mouniadmin",
                email="mouniadmin@runtimerush.com",
                password_hash=hash_password("1214@"),
                role='admin'
            )
            db.add(admin_user)
            db.commit()
            results["admin_created"] = True
        else:
            admin_id = existing_admin.id
        
        # Create challenges if don't exist
        existing_count = db.query(Challenge).count()
        if existing_count == 0:
            challenges_data = [
                {
                    "title": "Binary Search Algorithm",
                    "description": "Implement a binary search algorithm to find an element in a sorted array. Arrange the code fragments in the correct order.",
                    "language": "python",
                    "level": 1,
                    "fragments": [
                        "def binary_search(arr, target):\n    left, right = 0, len(arr) - 1",
                        "    while left <= right:\n        mid = (left + right) // 2",
                        "        if arr[mid] == target:\n            return mid",
                        "        elif arr[mid] < target:\n            left = mid + 1",
                        "        else:\n            right = mid - 1\n    return -1"
                    ]
                },
                {
                    "title": "Quick Sort Algorithm",
                    "description": "Implement the quick sort algorithm to sort an array. Arrange the code fragments in the correct order.",
                    "language": "python",
                    "level": 2,
                    "fragments": [
                        "def quick_sort(arr):\n    if len(arr) <= 1:\n        return arr",
                        "    pivot = arr[len(arr) // 2]",
                        "    left = [x for x in arr if x < pivot]",
                        "    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]",
                        "    return quick_sort(left) + middle + quick_sort(right)"
                    ]
                },
                {
                    "title": "Merge Sort Algorithm",
                    "description": "Implement the merge sort algorithm to sort an array. Arrange the code fragments in the correct order.",
                    "language": "python",
                    "level": 3,
                    "fragments": [
                        "def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr",
                        "    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])",
                        "    return merge(left, right)\n\ndef merge(left, right):\n    result = []",
                        "    i = j = 0\n    while i < len(left) and j < len(right):",
                        "        if left[i] <= right[j]:\n            result.append(left[i])\n            i += 1\n        else:\n            result.append(right[j])\n            j += 1\n    result.extend(left[i:])\n    result.extend(right[j:])\n    return result"
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
                    created_by=admin_id
                )
                db.add(challenge)
                
                for idx, fragment_content in enumerate(challenge_data["fragments"]):
                    fragment = CodeFragment(
                        id=str(uuid.uuid4()),
                        challenge_id=challenge_id,
                        content=fragment_content,
                        original_order=idx + 1
                    )
                    db.add(fragment)
                
                db.commit()
                results["challenges_created"] += 1
        
        return {
            "success": True,
            "message": "Database initialized successfully",
            "details": results
        }
        
    except Exception as e:
        results["errors"].append(str(e))
        db.rollback()
        return {
            "success": False,
            "message": "Database initialization failed",
            "details": results
        }
    finally:
        db.close()
