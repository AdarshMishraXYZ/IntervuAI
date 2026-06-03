from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.resume import Resume
from app.models.github_profile import GitHubProfile
from app.models.leetcode_profile import LeetCodeProfile
from app.services.candidate_service import calculate_overall_score
from app.services.candidate_service import get_candidate_level
from app.services.interview_service import generate_ai_interview_questions

router = APIRouter()


class InterviewGenerateRequest(BaseModel):
    role: str


@router.post("/generate")
def generate_interview(
    payload: InterviewGenerateRequest,
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).order_by(
        Resume.created_at.desc()
    ).first()

    github = db.query(GitHubProfile).order_by(
        GitHubProfile.created_at.desc()
    ).first()

    leetcode = db.query(LeetCodeProfile).order_by(
        LeetCodeProfile.created_at.desc()
    ).first()

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

    overall_score = calculate_overall_score(
        resume.resume_score,
        github.github_score,
        leetcode.leetcode_score
    )

    candidate_level = get_candidate_level(
        overall_score
    )

    try:
        questions = generate_ai_interview_questions(
            payload.role,
            candidate_level,
            resume.skills,
            github.github_score,
            leetcode.leetcode_score,
            overall_score
        )
    except Exception:
        questions = [
            {
                "question": "Explain how you would design a scalable REST API.",
                "category": "Backend",
                "difficulty": "Medium"
            },
            {
                "question": "Pick one project from your resume and explain the technical architecture.",
                "category": "Resume",
                "difficulty": "Medium"
            },
            {
                "question": "Pick one GitHub project and explain the main design decisions.",
                "category": "GitHub",
                "difficulty": "Medium"
            }
        ]

    return {
        "role": payload.role,
        "candidate_level": candidate_level,
        "overall_score": overall_score,
        "questions": questions
    }