import requests
from datetime import datetime

# Get challenges and check their times
try:
    response = requests.get("http://127.0.0.1:8000/api/challenges")
    if response.status_code == 200:
        challenges = response.json()
        now = datetime.now()
        print(f"Current time: {now}")
        print(f"Current time ISO: {now.isoformat()}")
        
        for challenge in challenges:
            print(f"\nChallenge: {challenge['title']}")
            print(f"Start: {challenge['start_time']}")
            print(f"End: {challenge['end_time']}")
            
            # Parse times
            start_time = datetime.fromisoformat(challenge['start_time'].replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(challenge['end_time'].replace('Z', '+00:00'))
            
            print(f"Start parsed: {start_time}")
            print(f"End parsed: {end_time}")
            
            if now < start_time:
                status = 'upcoming'
            elif now > end_time:
                status = 'ended'
            else:
                status = 'active'
            
            print(f"Status: {status}")
    else:
        print("Error:", response.text)
except Exception as e:
    print(f"Error: {e}")