import requests
from datetime import datetime, timedelta
import json

API_URL = "http://127.0.0.1:8000/api/challenges"

# Same challenge in different languages
challenges = [
    {
        "title": "Fix the Hello World Bug - Python",
        "description": "The code below should print 'Hello, World!' but it has a bug. Fix the code and make it work!",
        "language": "python",
        "fragments": [
            {"content": "def greet():", "original_order": 1},
            {"content": "    print('Hello, World!')", "original_order": 2},
            {"content": "greet()", "original_order": 3}
        ],
        "correct_solution": "def greet():\n    print('Hello, World!')\n\ngreet()",
        "test_cases": [{"input": "", "expected_output": "Hello, World!", "visible": True}],
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(hours=2)).isoformat(),
        "created_by": "00000000-0000-0000-0000-000000000001"
    },
    {
        "title": "Fix the Hello World Bug - JavaScript",
        "description": "The code below should print 'Hello, World!' but it has a bug. Fix the code and make it work!",
        "language": "javascript",
        "fragments": [
            {"content": "function greet() {", "original_order": 1},
            {"content": "    console.log('Hello, World!');", "original_order": 2},
            {"content": "}", "original_order": 3},
            {"content": "greet();", "original_order": 4}
        ],
        "correct_solution": "function greet() {\n    console.log('Hello, World!');\n}\n\ngreet();",
        "test_cases": [{"input": "", "expected_output": "Hello, World!", "visible": True}],
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(hours=2)).isoformat(),
        "created_by": "00000000-0000-0000-0000-000000000001"
    },
    {
        "title": "Fix the Hello World Bug - Java",
        "description": "The code below should print 'Hello, World!' but it has a bug. Fix the code and make it work!",
        "language": "java",
        "fragments": [
            {"content": "public class Main {", "original_order": 1},
            {"content": "    public static void main(String[] args) {", "original_order": 2},
            {"content": "        System.out.println(\"Hello, World!\");", "original_order": 3},
            {"content": "    }", "original_order": 4},
            {"content": "}", "original_order": 5}
        ],
        "correct_solution": "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}",
        "test_cases": [{"input": "", "expected_output": "Hello, World!", "visible": True}],
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(hours=2)).isoformat(),
        "created_by": "00000000-0000-0000-0000-000000000001"
    },
    {
        "title": "Fix the Hello World Bug - C++",
        "description": "The code below should print 'Hello, World!' but it has a bug. Fix the code and make it work!",
        "language": "cpp",
        "fragments": [
            {"content": "#include <iostream>", "original_order": 1},
            {"content": "using namespace std;", "original_order": 2},
            {"content": "int main() {", "original_order": 3},
            {"content": "    cout << \"Hello, World!\" << endl;", "original_order": 4},
            {"content": "    return 0;", "original_order": 5},
            {"content": "}", "original_order": 6}
        ],
        "correct_solution": "#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << \"Hello, World!\" << endl;\n    return 0;\n}",
        "test_cases": [{"input": "", "expected_output": "Hello, World!", "visible": True}],
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(hours=2)).isoformat(),
        "created_by": "00000000-0000-0000-0000-000000000001"
    },
    {
        "title": "Fix the Hello World Bug - C",
        "description": "The code below should print 'Hello, World!' but it has a bug. Fix the code and make it work!",
        "language": "c",
        "fragments": [
            {"content": "#include <stdio.h>", "original_order": 1},
            {"content": "int main() {", "original_order": 2},
            {"content": "    printf(\"Hello, World!\\n\");", "original_order": 3},
            {"content": "    return 0;", "original_order": 4},
            {"content": "}", "original_order": 5}
        ],
        "correct_solution": "#include <stdio.h>\n\nint main() {\n    printf(\"Hello, World!\\n\");\n    return 0;\n}",
        "test_cases": [{"input": "", "expected_output": "Hello, World!", "visible": True}],
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(hours=2)).isoformat(),
        "created_by": "00000000-0000-0000-0000-000000000001"
    }
]

print("Creating multi-language challenges...\n")

for challenge in challenges:
    try:
        response = requests.post(API_URL, json=challenge, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            print(f"✅ Created: {challenge['title']}")
        else:
            print(f"❌ Failed: {challenge['title']} - {response.status_code}")
    except Exception as e:
        print(f"❌ Error creating {challenge['title']}: {e}")

print("\n🎉 All challenges created! Participants can choose their preferred language.")
print("Visit http://localhost:3000 to see all challenges!")
