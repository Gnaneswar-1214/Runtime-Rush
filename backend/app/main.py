from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import challenges_sqlite, auth, admin

# ✅ IMPORT DB
from app.database import Base, engine

app = FastAPI(title="Runtime Rush API", version="1.0.0")

# ✅ CREATE TABLES ON STARTUP (CRITICAL FOR RAILWAY)
Base.metadata.create_all(bind=engine)

# ✅ AUTO-MIGRATE DATABASE SCHEMA (ADD MISSING COLUMNS)
def auto_migrate_database():
    """Automatically add missing columns to existing database"""
    from app.database import SessionLocal
    import sqlite3
    
    db = SessionLocal()
    try:
        # Check if tab_switch_count column exists
        result = db.execute("PRAGMA table_info(user_progress)")
        columns = [row[1] for row in result.fetchall()]
        
        if 'tab_switch_count' not in columns:
            print("⚠️ Missing tab_switch_count column! Adding it now...")
            db.execute("ALTER TABLE user_progress ADD COLUMN tab_switch_count INTEGER DEFAULT 0")
            db.commit()
            print("✅ Added tab_switch_count column successfully!")
        else:
            print("✅ Database schema is up to date")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        db.rollback()
    finally:
        db.close()

# Run migration before initialization
auto_migrate_database()

# ✅ AUTO-INITIALIZE DATABASE IF EMPTY (FOR RAILWAY EPHEMERAL STORAGE)
def auto_initialize_database():
    """Automatically initialize database with challenges if empty"""
    from app.database import SessionLocal
    from app.models_sqlite import Challenge
    
    db = SessionLocal()
    try:
        challenge_count = db.query(Challenge).count()
        if challenge_count == 0:
            print("⚠️ Database is empty! Auto-initializing...")
            # Import and run initialization
            from app.models_sqlite import User, CodeFragment
            import uuid
            import hashlib
            from datetime import datetime, timedelta
            
            def hash_password(password: str) -> str:
                return hashlib.sha256(password.encode()).hexdigest()
            
            # Create admin
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
            
            # Create challenges
            challenges_data = [
                # Level 1: Armstrong Number - 4 languages
                {
                    "title": "Armstrong Number - Python",
                    "description": "Check if a number is an Armstrong number (sum of cubes of digits equals the number). Arrange the code fragments in the correct order.",
                    "language": "python",
                    "level": 1,
                    "fragments": [
                        "def is_armstrong(n):\n    digits = str(n)\n    power = len(digits)",
                        "    total = 0\n    for digit in digits:",
                        "        total += int(digit) ** power",
                        "    return total == n"
                    ]
                },
                {
                    "title": "Armstrong Number - C",
                    "description": "Check if a number is an Armstrong number (sum of cubes of digits equals the number). Arrange the code fragments in the correct order.",
                    "language": "c",
                    "level": 1,
                    "fragments": [
                        "int is_armstrong(int n) {\n    int original = n, sum = 0, digits = 0;",
                        "    int temp = n;\n    while(temp != 0) { digits++; temp /= 10; }",
                        "    temp = n;\n    while(temp != 0) { int digit = temp % 10; sum += pow(digit, digits); temp /= 10; }",
                        "    return sum == original;\n}"
                    ]
                },
                {
                    "title": "Armstrong Number - Java",
                    "description": "Check if a number is an Armstrong number (sum of cubes of digits equals the number). Arrange the code fragments in the correct order.",
                    "language": "java",
                    "level": 1,
                    "fragments": [
                        "public static boolean isArmstrong(int n) {\n    String digits = String.valueOf(n);\n    int power = digits.length();",
                        "    int total = 0;\n    for (char digit : digits.toCharArray()) {",
                        "        total += Math.pow(Character.getNumericValue(digit), power);",
                        "    }\n    return total == n;\n}"
                    ]
                },
                {
                    "title": "Armstrong Number - C++",
                    "description": "Check if a number is an Armstrong number (sum of cubes of digits equals the number). Arrange the code fragments in the correct order.",
                    "language": "cpp",
                    "level": 1,
                    "fragments": [
                        "bool isArmstrong(int n) {\n    int original = n, sum = 0, digits = 0;",
                        "    int temp = n;\n    while(temp != 0) { digits++; temp /= 10; }",
                        "    temp = n;\n    while(temp != 0) { int digit = temp % 10; sum += pow(digit, digits); temp /= 10; }",
                        "    return sum == original;\n}"
                    ]
                },
                # Level 2: Merge Sort - 4 languages
                {
                    "title": "Merge Sort - Python",
                    "description": "Implement the merge sort algorithm to sort an array. Arrange the code fragments in the correct order.",
                    "language": "python",
                    "level": 2,
                    "fragments": [
                        "def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr",
                        "    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])",
                        "    return merge(left, right)\n\ndef merge(left, right):\n    result = []",
                        "    i = j = 0\n    while i < len(left) and j < len(right):",
                        "        if left[i] <= right[j]:\n            result.append(left[i])\n            i += 1\n        else:\n            result.append(right[j])\n            j += 1\n    result.extend(left[i:])\n    result.extend(right[j:])\n    return result"
                    ]
                },
                {
                    "title": "Merge Sort - C",
                    "description": "Implement the merge sort algorithm to sort an array. Arrange the code fragments in the correct order.",
                    "language": "c",
                    "level": 2,
                    "fragments": [
                        "void merge(int arr[], int l, int m, int r) {\n    int n1 = m - l + 1, n2 = r - m;\n    int L[n1], R[n2];",
                        "    for(int i = 0; i < n1; i++) L[i] = arr[l + i];\n    for(int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];",
                        "    int i = 0, j = 0, k = l;\n    while(i < n1 && j < n2) { arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++]; }",
                        "    while(i < n1) arr[k++] = L[i++];\n    while(j < n2) arr[k++] = R[j++];\n}",
                        "void mergeSort(int arr[], int l, int r) {\n    if(l < r) { int m = l + (r - l) / 2; mergeSort(arr, l, m); mergeSort(arr, m + 1, r); merge(arr, l, m, r); }\n}"
                    ]
                },
                {
                    "title": "Merge Sort - Java",
                    "description": "Implement the merge sort algorithm to sort an array. Arrange the code fragments in the correct order.",
                    "language": "java",
                    "level": 2,
                    "fragments": [
                        "public static void mergeSort(int[] arr, int l, int r) {\n    if (l < r) {",
                        "        int m = l + (r - l) / 2;\n        mergeSort(arr, l, m);\n        mergeSort(arr, m + 1, r);",
                        "        merge(arr, l, m, r);\n    }\n}",
                        "private static void merge(int[] arr, int l, int m, int r) {\n    int n1 = m - l + 1, n2 = r - m;\n    int[] L = new int[n1], R = new int[n2];",
                        "    for(int i = 0; i < n1; i++) L[i] = arr[l + i];\n    for(int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];\n    int i = 0, j = 0, k = l;\n    while(i < n1 && j < n2) arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++];\n    while(i < n1) arr[k++] = L[i++];\n    while(j < n2) arr[k++] = R[j++];\n}"
                    ]
                },
                {
                    "title": "Merge Sort - C++",
                    "description": "Implement the merge sort algorithm to sort an array. Arrange the code fragments in the correct order.",
                    "language": "cpp",
                    "level": 2,
                    "fragments": [
                        "void merge(vector<int>& arr, int l, int m, int r) {\n    vector<int> L(arr.begin() + l, arr.begin() + m + 1);\n    vector<int> R(arr.begin() + m + 1, arr.begin() + r + 1);",
                        "    int i = 0, j = 0, k = l;\n    while(i < L.size() && j < R.size()) {",
                        "        arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++];",
                        "    }\n    while(i < L.size()) arr[k++] = L[i++];\n    while(j < R.size()) arr[k++] = R[j++];\n}",
                        "void mergeSort(vector<int>& arr, int l, int r) {\n    if(l < r) { int m = l + (r - l) / 2; mergeSort(arr, l, m); mergeSort(arr, m + 1, r); merge(arr, l, m, r); }\n}"
                    ]
                },
                # Level 3: Reversing Array - 4 languages (5 fragments each)
                {
                    "title": "Reversing Array - Python",
                    "description": "Implement a function to reverse an array in-place. Arrange the code fragments in the correct order.",
                    "language": "python",
                    "level": 3,
                    "fragments": [
                        "def reverse_array(arr):\n    left = 0\n    right = len(arr) - 1",
                        "    while left < right:",
                        "        arr[left], arr[right] = arr[right], arr[left]",
                        "        left += 1\n        right -= 1",
                        "    return arr"
                    ]
                },
                {
                    "title": "Reversing Array - C",
                    "description": "Implement a function to reverse an array in-place. Arrange the code fragments in the correct order.",
                    "language": "c",
                    "level": 3,
                    "fragments": [
                        "void reverse_array(int arr[], int n) {\n    int left = 0, right = n - 1;",
                        "    while(left < right) {",
                        "        int temp = arr[left];",
                        "        arr[left] = arr[right];\n        arr[right] = temp;",
                        "        left++;\n        right--;\n    }\n}"
                    ]
                },
                {
                    "title": "Reversing Array - Java",
                    "description": "Implement a function to reverse an array in-place. Arrange the code fragments in the correct order.",
                    "language": "java",
                    "level": 3,
                    "fragments": [
                        "public static void reverseArray(int[] arr) {\n    int left = 0, right = arr.length - 1;",
                        "    while(left < right) {",
                        "        int temp = arr[left];",
                        "        arr[left] = arr[right];\n        arr[right] = temp;",
                        "        left++;\n        right--;\n    }\n}"
                    ]
                },
                {
                    "title": "Reversing Array - C++",
                    "description": "Implement a function to reverse an array in-place. Arrange the code fragments in the correct order.",
                    "language": "cpp",
                    "level": 3,
                    "fragments": [
                        "void reverseArray(vector<int>& arr) {\n    int left = 0, right = arr.size() - 1;",
                        "    while(left < right) {",
                        "        swap(arr[left], arr[right]);",
                        "        left++;\n        right--;",
                        "    }\n}"
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
            
            print("✅ Database auto-initialized with 12 challenges!")
        else:
            print(f"✅ Database already has {challenge_count} challenges")
    except Exception as e:
        print(f"❌ Auto-initialization failed: {e}")
        db.rollback()
    finally:
        db.close()

# Run auto-initialization
auto_initialize_database()

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


@app.get("/initialize-db")
@app.post("/initialize-db")
async def initialize_database():
    """
    Initialize database with admin user and challenges
    Call this endpoint ONCE after deployment to set up the database
    Can be accessed via GET (browser) or POST (API)
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
                # Level 1: Armstrong Number - 4 languages
                {
                    "title": "Armstrong Number - Python",
                    "description": "Check if a number is an Armstrong number (sum of cubes of digits equals the number). Arrange the code fragments in the correct order.",
                    "language": "python",
                    "level": 1,
                    "fragments": [
                        "def is_armstrong(n):\n    digits = str(n)\n    power = len(digits)",
                        "    total = 0\n    for digit in digits:",
                        "        total += int(digit) ** power",
                        "    return total == n"
                    ]
                },
                {
                    "title": "Armstrong Number - C",
                    "description": "Check if a number is an Armstrong number (sum of cubes of digits equals the number). Arrange the code fragments in the correct order.",
                    "language": "c",
                    "level": 1,
                    "fragments": [
                        "int is_armstrong(int n) {\n    int original = n, sum = 0, digits = 0;",
                        "    int temp = n;\n    while(temp != 0) { digits++; temp /= 10; }",
                        "    temp = n;\n    while(temp != 0) { int digit = temp % 10; sum += pow(digit, digits); temp /= 10; }",
                        "    return sum == original;\n}"
                    ]
                },
                {
                    "title": "Armstrong Number - Java",
                    "description": "Check if a number is an Armstrong number (sum of cubes of digits equals the number). Arrange the code fragments in the correct order.",
                    "language": "java",
                    "level": 1,
                    "fragments": [
                        "public static boolean isArmstrong(int n) {\n    String digits = String.valueOf(n);\n    int power = digits.length();",
                        "    int total = 0;\n    for (char digit : digits.toCharArray()) {",
                        "        total += Math.pow(Character.getNumericValue(digit), power);",
                        "    }\n    return total == n;\n}"
                    ]
                },
                {
                    "title": "Armstrong Number - C++",
                    "description": "Check if a number is an Armstrong number (sum of cubes of digits equals the number). Arrange the code fragments in the correct order.",
                    "language": "cpp",
                    "level": 1,
                    "fragments": [
                        "bool isArmstrong(int n) {\n    int original = n, sum = 0, digits = 0;",
                        "    int temp = n;\n    while(temp != 0) { digits++; temp /= 10; }",
                        "    temp = n;\n    while(temp != 0) { int digit = temp % 10; sum += pow(digit, digits); temp /= 10; }",
                        "    return sum == original;\n}"
                    ]
                },
                # Level 2: Merge Sort - 4 languages
                {
                    "title": "Merge Sort - Python",
                    "description": "Implement the merge sort algorithm to sort an array. Arrange the code fragments in the correct order.",
                    "language": "python",
                    "level": 2,
                    "fragments": [
                        "def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr",
                        "    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])",
                        "    return merge(left, right)\n\ndef merge(left, right):\n    result = []",
                        "    i = j = 0\n    while i < len(left) and j < len(right):",
                        "        if left[i] <= right[j]:\n            result.append(left[i])\n            i += 1\n        else:\n            result.append(right[j])\n            j += 1\n    result.extend(left[i:])\n    result.extend(right[j:])\n    return result"
                    ]
                },
                {
                    "title": "Merge Sort - C",
                    "description": "Implement the merge sort algorithm to sort an array. Arrange the code fragments in the correct order.",
                    "language": "c",
                    "level": 2,
                    "fragments": [
                        "void merge(int arr[], int l, int m, int r) {\n    int n1 = m - l + 1, n2 = r - m;\n    int L[n1], R[n2];",
                        "    for(int i = 0; i < n1; i++) L[i] = arr[l + i];\n    for(int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];",
                        "    int i = 0, j = 0, k = l;\n    while(i < n1 && j < n2) { arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++]; }",
                        "    while(i < n1) arr[k++] = L[i++];\n    while(j < n2) arr[k++] = R[j++];\n}",
                        "void mergeSort(int arr[], int l, int r) {\n    if(l < r) { int m = l + (r - l) / 2; mergeSort(arr, l, m); mergeSort(arr, m + 1, r); merge(arr, l, m, r); }\n}"
                    ]
                },
                {
                    "title": "Merge Sort - Java",
                    "description": "Implement the merge sort algorithm to sort an array. Arrange the code fragments in the correct order.",
                    "language": "java",
                    "level": 2,
                    "fragments": [
                        "public static void mergeSort(int[] arr, int l, int r) {\n    if (l < r) {",
                        "        int m = l + (r - l) / 2;\n        mergeSort(arr, l, m);\n        mergeSort(arr, m + 1, r);",
                        "        merge(arr, l, m, r);\n    }\n}",
                        "private static void merge(int[] arr, int l, int m, int r) {\n    int n1 = m - l + 1, n2 = r - m;\n    int[] L = new int[n1], R = new int[n2];",
                        "    for(int i = 0; i < n1; i++) L[i] = arr[l + i];\n    for(int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];\n    int i = 0, j = 0, k = l;\n    while(i < n1 && j < n2) arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++];\n    while(i < n1) arr[k++] = L[i++];\n    while(j < n2) arr[k++] = R[j++];\n}"
                    ]
                },
                {
                    "title": "Merge Sort - C++",
                    "description": "Implement the merge sort algorithm to sort an array. Arrange the code fragments in the correct order.",
                    "language": "cpp",
                    "level": 2,
                    "fragments": [
                        "void merge(vector<int>& arr, int l, int m, int r) {\n    vector<int> L(arr.begin() + l, arr.begin() + m + 1);\n    vector<int> R(arr.begin() + m + 1, arr.begin() + r + 1);",
                        "    int i = 0, j = 0, k = l;\n    while(i < L.size() && j < R.size()) {",
                        "        arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++];",
                        "    }\n    while(i < L.size()) arr[k++] = L[i++];\n    while(j < R.size()) arr[k++] = R[j++];\n}",
                        "void mergeSort(vector<int>& arr, int l, int r) {\n    if(l < r) { int m = l + (r - l) / 2; mergeSort(arr, l, m); mergeSort(arr, m + 1, r); merge(arr, l, m, r); }\n}"
                    ]
                },
                # Level 3: Reversing Array - 4 languages (5 fragments each)
                {
                    "title": "Reversing Array - Python",
                    "description": "Implement a function to reverse an array in-place. Arrange the code fragments in the correct order.",
                    "language": "python",
                    "level": 3,
                    "fragments": [
                        "def reverse_array(arr):\n    left = 0\n    right = len(arr) - 1",
                        "    while left < right:",
                        "        arr[left], arr[right] = arr[right], arr[left]",
                        "        left += 1\n        right -= 1",
                        "    return arr"
                    ]
                },
                {
                    "title": "Reversing Array - C",
                    "description": "Implement a function to reverse an array in-place. Arrange the code fragments in the correct order.",
                    "language": "c",
                    "level": 3,
                    "fragments": [
                        "void reverse_array(int arr[], int n) {\n    int left = 0, right = n - 1;",
                        "    while(left < right) {",
                        "        int temp = arr[left];",
                        "        arr[left] = arr[right];\n        arr[right] = temp;",
                        "        left++;\n        right--;\n    }\n}"
                    ]
                },
                {
                    "title": "Reversing Array - Java",
                    "description": "Implement a function to reverse an array in-place. Arrange the code fragments in the correct order.",
                    "language": "java",
                    "level": 3,
                    "fragments": [
                        "public static void reverseArray(int[] arr) {\n    int left = 0, right = arr.length - 1;",
                        "    while(left < right) {",
                        "        int temp = arr[left];",
                        "        arr[left] = arr[right];\n        arr[right] = temp;",
                        "        left++;\n        right--;\n    }\n}"
                    ]
                },
                {
                    "title": "Reversing Array - C++",
                    "description": "Implement a function to reverse an array in-place. Arrange the code fragments in the correct order.",
                    "language": "cpp",
                    "level": 3,
                    "fragments": [
                        "void reverseArray(vector<int>& arr) {\n    int left = 0, right = arr.size() - 1;",
                        "    while(left < right) {",
                        "        swap(arr[left], arr[right]);",
                        "        left++;\n        right--;",
                        "    }\n}"
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
