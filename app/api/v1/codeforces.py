from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.codeforces_profile import CodeforcesProfile
from app.services.codeforces_service import (
    fetch_codeforces_profile,
    calculate_codeforces_score
)

router = APIRouter()


class CodeforcesAnalyzeRequest(BaseModel):
    username: str


@router.post("/analyze")
def analyze_codeforces(
    payload: CodeforcesAnalyzeRequest,
    db: Session = Depends(get_db)
):
    profile_data = fetch_codeforces_profile(payload.username)

    if not profile_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Codeforces profile not found"
        )

    codeforces_score = calculate_codeforces_score(
        profile_data["rating"],
        profile_data["max_rating"],
        profile_data["contribution"],
        profile_data["friend_count"]
    )

    profile = CodeforcesProfile(
        user_id="a4b1b6ad-f44d-4178-b677-c8cc06541292",
        username=profile_data["username"],
        rating=profile_data["rating"],
        max_rating=profile_data["max_rating"],
        rank=profile_data["rank"],
        max_rank=profile_data["max_rank"],
        contribution=profile_data["contribution"],
        friend_count=profile_data["friend_count"],
        codeforces_score=codeforces_score
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return {
        "id": str(profile.id),
        "username": profile.username,
        "rating": profile.rating,
        "max_rating": profile.max_rating,
        "rank": profile.rank,
        "max_rank": profile.max_rank,
        "contribution": profile.contribution,
        "friend_count": profile.friend_count,
        "codeforces_score": profile.codeforces_score
    }