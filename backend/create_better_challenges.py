from app.database import SessionLocal
from app.models_sqlite import Challenge, CodeFragment, TestCase, User
from datetime import datetime, timedelta
import uuid

db = SessionLocal()

try:
    # Delete all existing challenges
    db.query(TestCase).delete()
    db.query(CodeFragment).delete()
    db.query(Challenge).delete()
    
    print("🗑️ Deleted all existing challenges")
    
    # Get admin user
    admin_user = db.query(User).filter(User.role == 'admin').first()
    if not admin_user:
        print("❌ No admin user found")
        exit()
    
    now = datetime.now()
    end_time = now + timedelta(hours=24)
    
    # Create 3 new challenges with 4-5 fragments each
    challenges_data = [
        {
            "level": 1,
            "title": "Level 1: Binary Search",
            "description": "Implement a binary search algorithm to find a target value in a sorted array.",
            "language": "python",
            "fragments": [
                "def binary_search(arr, target):\n    left, right = 0, len(arr) - 1",
                "    while left <= right:\n        mid = (left + right) // 2",
                "        if arr[mid] == target:\n            return mid",
                "        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1",
                "    return -1"
            ],
            "test_cases": [
                {"input": "[1,2,3,4,5], 3", "expected_output": "2", "visible": True},
                {"input": "[1,2,3,4,5], 6", "expected_output": "-1", "visible": True}
            ]
        },
        {
            "level": 2,
            "title": "Level 2: Quick Sort",
            "description": "Implement the quicksort algorithm to sort an array in ascending order.",
            "language": "python",
            "fragments": [
                "def quicksort(arr):\n    if len(arr) <= 1:\n        return arr",
                "    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]",
                "    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]",
                "    return quicksort(left) + middle + quicksort(right)"
            ],
            "test_cases": [
                {"input": "[3,1,4,1,5,9,2,6]", "expected_output": "[1, 1, 2, 3, 4, 5, 6, 9]", "visible": True},
                {"input": "[5,2,8,1,9]", "expected_output": "[1, 2, 5, 8, 9]", "visible": True}
            ]
        },
        {
            "level": 3,
            "title": "Level 3: Merge Sort",
            "description": "Implement the merge sort algorithm with proper divide and conquer approach.",
            "language": "python",
            "fragments": [
                "def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2",
                "    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)",
                "def merge(left, right):\n    result = []\n    i = j = 0",
                "    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            result.append(left[i])\n            i += 1\n        else:\n            result.append(right[j])\n            j += 1",
                "    result.extend(left[i:])\n    result.extend(right[j:])\n    return result"
            ],
            "test_cases": [
                {"input": "[38,27,43,3,9,82,10]", "expected_output": "[3, 9, 10, 27, 38, 43, 82]", "visible": True},
                {"input": "[5,2,4,6,1,3]", "expected_output": "[1, 2, 3, 4, 5, 6]", "visible": True}
            ]
        }
    ]
    
    for challenge_data in challenges_data:
        # Create challenge
        challenge_id = str(uuid.uuid4())
        challenge = Challenge(
            id=challenge_id,
            title=challenge_data["title"],
            description=challenge_data["description"],
            language=challenge_data["language"],
            level=challenge_data["level"],
            correct_solution="\n".join(challenge_data["fragments"]),
            start_time=now,
            end_time=end_time,
            created_by=admin_user.id
        )
        db.add(challenge)
        
        # Add fragments
        for i, fragment_content in enumerate(challenge_data["fragments"]):
            fragment = CodeFragment(
                id=str(uuid.uuid4()),
                challenge_id=challenge_id,
                content=fragment_content,
                original_order=i + 1
            )
            db.add(fragment)
        
        # Add test cases
        for test_data in challenge_data["test_cases"]:
            test_case = TestCase(
                id=str(uuid.uuid4()),
                challenge_id=challenge_id,
                input=test_data["input"],
                expected_output=test_data["expected_output"],
                visible=test_data["visible"]
            )
            db.add(test_case)
        
        print(f"✅ Created {challenge_data['title']} with {len(challenge_data['fragments'])} fragments")
    
    db.commit()
    print("\n🎉 Successfully created 3 new challenges!")
    print("📊 Level 1: 5 fragments, Level 2: 4 fragments, Level 3: 5 fragments")
    print("⏰ All challenges active for 24 hours")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
