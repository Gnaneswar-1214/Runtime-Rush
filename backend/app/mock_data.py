# Mock data for testing without database
from datetime import datetime, timedelta
import uuid

MOCK_CHALLENGES = []

def create_mock_challenge():
    challenge_id = str(uuid.uuid4())
    challenge = {
        "id": challenge_id,
        "title": "Fix the Hello World Bug",
        "description": "The code below should print 'Hello, World!' but it has a bug. Fix the code and make it work!",
        "language": "python",
        "fragments": [
            {
                "id": str(uuid.uuid4()),
                "content": "def greet():",
                "order": 1
            },
            {
                "id": str(uuid.uuid4()),
                "content": "    print('Hello, World!')",
                "order": 2
            },
            {
                "id": str(uuid.uuid4()),
                "content": "greet()",
                "order": 3
            }
        ],
        "correct_solution": "def greet():\n    print('Hello, World!')\n\ngreet()",
        "test_cases": [
            {
                "id": str(uuid.uuid4()),
                "input": "",
                "expected_output": "Hello, World!",
                "visible": True
            }
        ],
        "start_time": datetime.now().isoformat(),
        "end_time": (datetime.now() + timedelta(hours=2)).isoformat(),
        "created_by": str(uuid.uuid4())
    }
    MOCK_CHALLENGES.append(challenge)
    return challenge

# Create initial mock challenge
create_mock_challenge()
