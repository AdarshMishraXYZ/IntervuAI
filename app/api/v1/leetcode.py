from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.leetcode_profile import LeetCodeProfile
from app.services.leetcode_service import fetch_leetcode_profile
from app.services.leetcode_service import calculate_leetcode_score

router = APIRouter()


class LeetCodeAnalyzeRequest(BaseModel):
    username: str


@router.post("/analyze")
def analyze_leetcode(
    payload: LeetCodeAnalyzeRequest,
    db: Session = Depends(get_db)
):
    profile_data = fetch_leetcode_profile(payload.username)

    if not profile_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LeetCode profile not found"
        )

    leetcode_score = calculate_leetcode_score(
        profile_data["easy_solved"],
        profile_data["medium_solved"],
        profile_data["hard_solved"]
    )

    leetcode_profile = LeetCodeProfile(
        user_id="a4b1b6ad-f44d-4178-b677-c8cc06541292",
        username=profile_data["username"],
        total_solved=profile_data["total_solved"],
        easy_solved=profile_data["easy_solved"],
        medium_solved=profile_data["medium_solved"],
        hard_solved=profile_data["hard_solved"],
        leetcode_score=leetcode_score
    )

    db.add(leetcode_profile)
    db.commit()
    db.refresh(leetcode_profile)

    return {
        "id": str(leetcode_profile.id),
        "username": leetcode_profile.username,
        "total_solved": leetcode_profile.total_solved,
        "easy_solved": leetcode_profile.easy_solved,
        "medium_solved": leetcode_profile.medium_solved,
        "hard_solved": leetcode_profile.hard_solved,
        "leetcode_score": leetcode_profile.leetcode_score
    }