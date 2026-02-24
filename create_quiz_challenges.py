import requests
from datetime import datetime, timedelta
import uuid

API_URL = "http://127.0.0.1:8000/api/challenges"

# Progressive quiz challenges - Easy to Hard
quiz_challenges = [
    # LEVEL 1 - EASY (5 minutes each)
    {
        "title": "Level 1: Print Your Name",
        "description": "Write a program that prints 'Hello, [Your Name]!' - Replace [Your Name] with any name.",
        "language": "python",
        "level": 1,
        "fragments": [
            {"content": "name = 'Student'", "original_order": 1},
            {"content": "print(f'Hello, {name}!')", "original_order": 2}
        ],
        "correct_solution": "name = 'Student'\nprint(f'Hello, {name}!')",
        "test_cases": [
            {"input": "", "expected_output": "Hello, Student!", "visible": True}
        ],
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(minutes=5)).isoformat(),
        "created_by": str(uuid.uuid4())
    },
    
    # LEVEL 2 - EASY (5 minutes)
    {
        "title": "Level 2: Add Two Numbers",
        "description": "Create a function that adds two numbers and returns the result.",
        "language": "python",
        "level": 1,
        "fragments": [
            {"content": "def add(a, b):", "original_order": 1},
            {"content": "    return a + b", "original_order": 2},
            {"content": "print(add(5, 3))", "original_order": 3}
        ],
        "correct_solution": "def add(a, b):\n    return a + b\n\nprint(add(5, 3))",
        "test_cases": [
            {"input": "", "expected_output": "8", "visible": True}
        ],
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(minutes=5)).isoformat(),
        "created_by": str(uuid.uuid4())
    },
    
    # LEVEL 3 - MEDIUM (7 minutes)
    {
        "title": "Level 3: Find Maximum",
        "description": "Write a function that finds the maximum number in a list.",
        "language": "python",
        "level": 2,
        "fragments": [
            {"content": "def find_max(numbers):", "original_order": 1},
            {"content": "    return max(numbers)", "original_order": 2},
            {"content": "print(find_max([3, 7, 2, 9, 1]))", "original_order": 3}
        ],
        "correct_solution": "def find_max(numbers):\n    return max(numbers)\n\nprint(find_max([3, 7, 2, 9, 1]))",
        "test_cases": [
            {"input": "", "expected_output": "9", "visible": True}
        ],
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(minutes=7)).isoformat(),
        "created_by": str(uuid.uuid4())
    },
    
    # LEVEL 4 - MEDIUM (7 minutes)
    {
        "title": "Level 4: Reverse a String",
        "description": "Create a function that reverses a string.",
        "language": "python",
        "level": 2,
        "fragments": [
            {"content": "def reverse_string(text):", "original_order": 1},
            {"content": "    return text[::-1]", "original_order": 2},
            {"content": "print(reverse_string('hello'))", "original_order": 3}
        ],
        "correct_solution": "def reverse_string(text):\n    return text[::-1]\n\nprint(reverse_string('hello'))",
        "test_cases": [
            {"input": "", "expected_output": "olleh", "visible": True}
        ],
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(minutes=7)).isoformat(),
        "created_by": str(uuid.uuid4())
    },
    
    # LEVEL 5 - HARD (10 minutes)
    {
        "title": "Level 5: Count Vowels",
        "description": "Write a function that counts the number of vowels (a, e, i, o, u) in a string.",
        "language": "python",
        "level": 3,
        "fragments": [
            {"content": "def count_vowels(text):", "original_order": 1},
            {"content": "    vowels = 'aeiouAEIOU'", "original_order": 2},
            {"content": "    return sum(1 for char in text if char in vowels)", "original_order": 3},
            {"content": "print(count_vowels('Hello World'))", "original_order": 4}
        ],
        "correct_solution": "def count_vowels(text):\n    vowels = 'aeiouAEIOU'\n    return sum(1 for char in text if char in vowels)\n\nprint(count_vowels('Hello World'))",
        "test_cases": [
            {"input": "", "expected_output": "3", "visible": True}
        ],
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(minutes=10)).isoformat(),
        "created_by": str(uuid.uuid4())
    },
    
    # LEVEL 6 - HARD (10 minutes)
    {
        "title": "Level 6: Fibonacci Sequence",
        "description": "Generate the first 10 numbers of the Fibonacci sequence.",
        "language": "python",
        "level": 3,
        "fragments": [
            {"content": "def fibonacci(n):", "original_order": 1},
            {"content": "    fib = [0, 1]", "original_order": 2},
            {"content": "    for i in range(2, n):", "original_order": 3},
            {"content": "        fib.append(fib[i-1] + fib[i-2])", "original_order": 4},
            {"content": "    return fib", "original_order": 5},
            {"content": "print(fibonacci(10))", "original_order": 6}
        ],
        "correct_solution": "def fibonacci(n):\n    fib = [0, 1]\n    for i in range(2, n):\n        fib.append(fib[i-1] + fib[i-2])\n    return fib\n\nprint(fibonacci(10))",
        "test_cases": [
            {"input": "", "expected_output": "[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]", "visible": True}
        ],
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(minutes=10)).isoformat(),
        "created_by": str(uuid.uuid4())
    }
]

print("🎮 Creating Progressive Quiz Challenges...\n")
print("=" * 50)

for i, challenge in enumerate(quiz_challenges, 1):
    try:
        response = requests.post(API_URL, json=challenge, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            duration = challenge['title'].split('(')[0] if '(' in challenge['title'] else ''
            print(f"✅ Level {i}: {challenge['title']}")
            print(f"   ⏱️  Time: {(datetime.fromisoformat(challenge['end_time']) - datetime.fromisoformat(challenge['start_time'])).seconds // 60} minutes")
        else:
            print(f"❌ Failed: {challenge['title']}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

print("=" * 50)
print("\n🎉 Quiz challenges created!")
print("📊 6 levels: Easy → Medium → Hard")
print("⏰ Individual timers for each level")
print("🚀 Visit http://localhost:3000 to start!")
