import requests
import json

# Test login
login_data = {
    "username": "testuser",
    "password": "password123"
}

try:
    response = requests.post("http://127.0.0.1:8000/api/auth/login", json=login_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print("User data:")
        print(json.dumps(user_data, indent=2))
    else:
        print("Error:", response.text)
except Exception as e:
    print(f"Error: {e}")

# Test getting challenges
try:
    response = requests.get("http://127.0.0.1:8000/api/challenges")
    print(f"\nChallenges Status: {response.status_code}")
    if response.status_code == 200:
        challenges = response.json()
        print(f"Found {len(challenges)} challenges:")
        for challenge in challenges:
            print(f"  - {challenge['title']} (Level {challenge.get('level', 'N/A')})")
    else:
        print("Error:", response.text)
except Exception as e:
    print(f"Error: {e}")