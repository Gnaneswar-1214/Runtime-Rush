from fastapi import APIRouter
from app.mock_data import MOCK_CHALLENGES

router = APIRouter(prefix="/api/challenges", tags=["challenges"])

@router.get("")
async def get_challenges():
    return MOCK_CHALLENGES

@router.get("/{challenge_id}")
async def get_challenge(challenge_id: str):
    for challenge in MOCK_CHALLENGES:
        if challenge["id"] == challenge_id:
            return challenge
    return {"detail": "Challenge not found"}
