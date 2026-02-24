# Challenge Management API Routes

## Overview

This document describes the FastAPI routes implemented for challenge management in the Runtime Rush platform.

## Implemented Routes

### 1. Create Challenge
- **Endpoint**: `POST /api/challenges`
- **Description**: Create a new challenge with fragments and test cases
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string",
    "language": "string",
    "correct_solution": "string",
    "start_time": "datetime",
    "end_time": "datetime",
    "created_by": "uuid (optional)",
    "fragments": [
      {
        "content": "string",
        "original_order": "integer"
      }
    ],
    "test_cases": [
      {
        "input": "string",
        "expected_output": "string",
        "visible": "boolean (default: true)"
      }
    ]
  }
  ```
- **Response**: 201 Created with challenge object
- **Validation**: 
  - Requires title, description, language
  - Requires at least one test case
  - Validates start_time < end_time
- **Requirements**: 1.1, 1.2, 1.3, 1.5, 1.6, 1.7

### 2. Get Challenge
- **Endpoint**: `GET /api/challenges/{challenge_id}`
- **Description**: Retrieve a challenge by ID
- **Path Parameters**: `challenge_id` (UUID)
- **Response**: 200 OK with challenge object, or 404 Not Found
- **Requirements**: 1.1, 1.2, 1.3, 1.5

### 3. List Challenges
- **Endpoint**: `GET /api/challenges`
- **Description**: List all challenges
- **Response**: 200 OK with array of challenge objects
- **Requirements**: 1.1

### 4. Update Challenge
- **Endpoint**: `PUT /api/challenges/{challenge_id}`
- **Description**: Update an existing challenge
- **Path Parameters**: `challenge_id` (UUID)
- **Request Body**: Partial challenge object (all fields optional)
- **Response**: 200 OK with updated challenge object, or 404 Not Found
- **Validation**: Same as create challenge
- **Requirements**: 1.1, 1.2, 1.3, 1.5, 1.6, 1.7

### 5. Delete Challenge
- **Endpoint**: `DELETE /api/challenges/{challenge_id}`
- **Description**: Delete a challenge
- **Path Parameters**: `challenge_id` (UUID)
- **Response**: 204 No Content, or 404 Not Found
- **Requirements**: 1.7

## Implementation Details

### File Structure
- **Router**: `backend/app/routers/challenges.py`
- **Manager**: `backend/app/managers/challenge_manager.py` (existing)
- **Models**: `backend/app/models/challenge.py` (existing)
- **Tests**: `backend/tests/test_challenge_routes.py`

### Key Features
1. **Pydantic Schemas**: Request/response validation using Pydantic models
2. **Error Handling**: Proper HTTP status codes and error messages
3. **Database Integration**: Uses ChallengeManager for all database operations
4. **Validation**: Leverages existing ChallengeManager validation logic

### Error Responses
- **400 Bad Request**: Validation errors (missing fields, invalid data)
- **404 Not Found**: Challenge not found
- **500 Internal Server Error**: Unexpected errors

## Testing

Run the test suite:
```bash
cd backend
python -m pytest tests/test_challenge_routes.py -v
```

### Test Coverage
- Create challenge with valid data
- Create challenge with missing required fields
- Create challenge with invalid time range
- Get existing challenge
- Get non-existent challenge
- List all challenges
- Update challenge
- Update non-existent challenge
- Delete challenge
- Delete non-existent challenge

## Usage Example

```python
import requests

# Create a challenge
challenge_data = {
    "title": "Debug the Python Code",
    "description": "Fix the bugs in the fragmented code",
    "language": "python",
    "correct_solution": "print('Hello, World!')",
    "start_time": "2024-01-01T10:00:00",
    "end_time": "2024-01-01T12:00:00",
    "fragments": [
        {"content": "print('Hello", "original_order": 0},
        {"content": ", World!')", "original_order": 1}
    ],
    "test_cases": [
        {"input": "", "expected_output": "Hello, World!", "visible": True}
    ]
}

response = requests.post("http://localhost:8000/api/challenges", json=challenge_data)
challenge = response.json()
challenge_id = challenge["id"]

# Get the challenge
response = requests.get(f"http://localhost:8000/api/challenges/{challenge_id}")
print(response.json())

# Update the challenge
update_data = {"title": "Updated Title"}
response = requests.put(f"http://localhost:8000/api/challenges/{challenge_id}", json=update_data)
print(response.json())

# Delete the challenge
response = requests.delete(f"http://localhost:8000/api/challenges/{challenge_id}")
print(response.status_code)  # 204
```

## Integration with Main App

The challenge router is registered in `backend/app/main.py`:

```python
from app.routers import challenges

app.include_router(challenges.router)
```

All routes are prefixed with `/api/challenges` and tagged with `challenges` for API documentation.

## Next Steps

The following routes still need to be implemented (tasks 15.2-15.5):
- Submission routes
- Test execution routes
- Winner and leaderboard routes
- Session management routes
