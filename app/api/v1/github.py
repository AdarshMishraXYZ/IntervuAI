from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.github_profile import GitHubProfile
from app.services.github_service import fetch_github_profile
from app.services.github_service import calculate_github_score

router = APIRouter()


class GitHubAnalyzeRequest(BaseModel):
    username: str


@router.post("/analyze")
def analyze_github(
    payload: GitHubAnalyzeRequest,
    db: Session = Depends(get_db)
):
    profile_data = fetch_github_profile(payload.username)

    if not profile_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="GitHub profile not found"
        )

    public_repos = profile_data.get("public_repos", 0)
    followers = profile_data.get("followers", 0)

    github_score = calculate_github_score(
        public_repos,
        followers
    )

    github_profile = GitHubProfile(
        user_id="a4b1b6ad-f44d-4178-b677-c8cc06541292",
        username=payload.username,
        public_repos=public_repos,
        followers=followers,
        languages="",
        github_score=github_score
    )

    db.add(github_profile)
    db.commit()
    db.refresh(github_profile)

    return {
        "id": str(github_profile.id),
        "username": github_profile.username,
        "public_repos": github_profile.public_repos,
        "followers": github_profile.followers,
        "github_score": github_profile.github_score
    }