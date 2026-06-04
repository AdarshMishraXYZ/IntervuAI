from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.models.resume import Resume
from app.models.github_profile import GitHubProfile
from app.models.leetcode_profile import LeetCodeProfile
from app.models.codeforces_profile import CodeforcesProfile

from app.services.candidate_service import (
    calculate_overall_score,
    get_candidate_level
)

router = APIRouter()


@router.get("/summary")
def candidate_summary(
    db: Session = Depends(get_db)
):
    resume = (
        db.query(Resume)
        .order_by(Resume.created_at.desc())
        .first()
    )

    github = (
        db.query(GitHubProfile)
        .order_by(GitHubProfile.created_at.desc())
        .first()
    )

    leetcode = (
        db.query(LeetCodeProfile)
        .order_by(LeetCodeProfile.created_at.desc())
        .first()
    )

    codeforces = (
        db.query(CodeforcesProfile)
        .order_by(CodeforcesProfile.created_at.desc())
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    if not github:
        raise HTTPException(
            status_code=404,
            detail="GitHub profile not found"
        )

    if not leetcode:
        raise HTTPException(
            status_code=404,
            detail="LeetCode profile not found"
        )

    if not codeforces:
        raise HTTPException(
            status_code=404,
            detail="Codeforces profile not found"
        )

    overall_score = calculate_overall_score(
        resume.resume_score,
        github.github_score,
        leetcode.leetcode_score,
        codeforces.codeforces_score
    )

    return {
        "resume_score": resume.resume_score,
        "github_score": github.github_score,
        "leetcode_score": leetcode.leetcode_score,
        "codeforces_score": codeforces.codeforces_score,
        "overall_score": overall_score,
        "candidate_level": get_candidate_level(
            overall_score
        ),
        "weightage": {
            "resume": 70,
            "github": 10,
            "leetcode": 10,
            "codeforces": 10
        }
    }