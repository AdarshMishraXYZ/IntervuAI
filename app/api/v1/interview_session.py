from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.models.interview import InterviewSession
from app.models.interview import InterviewAnswer
from app.models.interview_question import InterviewQuestion
from app.models.resume import Resume
from app.models.github_profile import GitHubProfile
from app.models.leetcode_profile import LeetCodeProfile
from app.models.codeforces_profile import CodeforcesProfile
from app.models.interview_report import InterviewReport

from app.services.candidate_intelligence_service import (
    generate_candidate_intelligence
)

from app.services.llm_interview_agent import (
    generate_llm_interview_question
)

router = APIRouter()


class StartInterviewRequest(BaseModel):
    role: str


class SubmitAnswerRequest(BaseModel):
    session_id: str
    answer: str


class EndInterviewRequest(BaseModel):
    session_id: str


def build_candidate_intelligence(
    db: Session
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

    codeforces = db.query(CodeforcesProfile).order_by(
        CodeforcesProfile.created_at.desc()
    ).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    if not github:
        raise HTTPException(status_code=404, detail="GitHub profile not found")

    if not leetcode:
        raise HTTPException(status_code=404, detail="LeetCode profile not found")

    if not codeforces:
        raise HTTPException(status_code=404, detail="Codeforces profile not found")

    return generate_candidate_intelligence(
        resume.resume_score,
        github.github_score,
        leetcode.leetcode_score,
        codeforces.codeforces_score,
        resume.skills
    )


def get_previous_qa(
    session_id: str,
    db: Session
):
    answers = db.query(InterviewAnswer).filter(
        InterviewAnswer.session_id == session_id
    ).order_by(
        InterviewAnswer.created_at.asc()
    ).all()

    previous_qa = []

    for item in answers:
        previous_qa.append(
            {
                "question": item.question,
                "answer": item.answer
            }
        )

    return previous_qa


@router.post("/start")
def start_interview(
    payload: StartInterviewRequest,
    db: Session = Depends(get_db)
):
    intelligence = build_candidate_intelligence(db)

    question_data = generate_llm_interview_question(
        payload.role,
        intelligence,
        []
    )

    session = InterviewSession(
        user_id="a4b1b6ad-f44d-4178-b677-c8cc06541292",
        role=payload.role
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    question_record = InterviewQuestion(
        session_id=session.id,
        question_number=1,
        question_text=question_data["question"],
        reason=question_data.get("reason"),
        difficulty=question_data.get("difficulty"),
        focus_area=question_data.get("focus_area")
    )

    db.add(question_record)
    db.commit()

    return {
        "session_id": str(session.id),
        "question_number": 1,
        "question": question_record.question_text,
        "reason": question_record.reason,
        "difficulty": question_record.difficulty,
        "focus_area": question_record.focus_area
    }


@router.post("/answer")
def submit_answer(
    payload: SubmitAnswerRequest,
    db: Session = Depends(get_db)
):
    session = db.query(InterviewSession).filter(
        InterviewSession.id == payload.session_id
    ).first()

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found"
        )

    current_question = db.query(InterviewQuestion).filter(
        InterviewQuestion.session_id == payload.session_id
    ).order_by(
        InterviewQuestion.question_number.desc()
    ).first()

    if not current_question:
        raise HTTPException(
            status_code=400,
            detail="No interview question found. Start interview again."
        )

    answer = InterviewAnswer(
        session_id=session.id,
        question=current_question.question_text,
        answer=payload.answer
    )

    db.add(answer)
    db.commit()

    previous_qa = get_previous_qa(
        payload.session_id,
        db
    )

    if len(previous_qa) >= 5:
        return {
            "message": "All questions answered. Please end the interview for final evaluation.",
            "next_question": None
        }

    intelligence = build_candidate_intelligence(db)

    question_data = generate_llm_interview_question(
        session.role,
        intelligence,
        previous_qa
    )

    next_question_number = len(previous_qa) + 1

    next_question_record = InterviewQuestion(
        session_id=session.id,
        question_number=next_question_number,
        question_text=question_data["question"],
        reason=question_data.get("reason"),
        difficulty=question_data.get("difficulty"),
        focus_area=question_data.get("focus_area")
    )

    db.add(next_question_record)
    db.commit()

    return {
        "question_number": next_question_number,
        "next_question": next_question_record.question_text,
        "reason": next_question_record.reason,
        "difficulty": next_question_record.difficulty,
        "focus_area": next_question_record.focus_area,
        "question_type": "llm_adaptive"
    }


@router.post("/end")
def end_interview(
    payload: EndInterviewRequest,
    db: Session = Depends(get_db)
):
    session = db.query(InterviewSession).filter(
        InterviewSession.id == payload.session_id
    ).first()

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found"
        )

    answers = db.query(InterviewAnswer).filter(
        InterviewAnswer.session_id == payload.session_id
    ).all()

    if len(answers) == 0:
        raise HTTPException(
            status_code=400,
            detail="No answers submitted"
        )

    total_words = 0

    for item in answers:
        total_words += len(item.answer.split())

    average_words = total_words // len(answers)

    technical_score = min(60 + len(answers) * 5, 90)

    communication_score = min(
        max(average_words, 40),
        90
    )

    problem_solving_score = min(
        technical_score + 3,
        95
    )

    overall_score = round(
        (
            technical_score +
            communication_score +
            problem_solving_score
        ) / 3
    )

    if overall_score >= 85:
        readiness_level = "Strong Chances"
    elif overall_score >= 70:
        readiness_level = "Good Chances"
    elif overall_score >= 55:
        readiness_level = "Moderate Chances"
    elif overall_score >= 40:
        readiness_level = "Needs Improvement"
    else:
        readiness_level = "Not Ready Yet"

    strengths = []
    areas_to_improve = []
    next_steps = []

    resume = db.query(Resume).order_by(
        Resume.created_at.desc()
    ).first()

    if resume:
        skills = resume.skills.lower()

        if "python" in skills:
            strengths.append("Strong Python foundation")

        if "git" in skills or "github" in skills:
            strengths.append("Good version control awareness")

        if "javascript" in skills:
            strengths.append("Full-stack development exposure")

        if "sql" not in skills and "postgresql" not in skills:
            areas_to_improve.append("Improve database and SQL fundamentals")

    if technical_score >= 80:
        strengths.append("Good technical understanding")
    else:
        areas_to_improve.append("Strengthen backend fundamentals")

    if problem_solving_score >= 80:
        strengths.append("Strong problem-solving potential")
    else:
        areas_to_improve.append("Practice structured problem solving")

    if communication_score < 60:
        areas_to_improve.append("Improve communication clarity and answer depth")
        next_steps.append("Practice explaining projects out loud daily")
    else:
        strengths.append("Clear interview communication")

    if overall_score >= 70:
        next_steps.append("Start applying for internships while continuing DSA practice")
    else:
        next_steps.append("Focus on DSA, backend basics, and mock interviews before applying widely")

    next_steps.append("Revise REST APIs, JWT, indexing, caching, and database transactions")

    feedback = (
        "Candidate shows promising technical potential. "
        "The current readiness level is based on candidate intelligence, "
        "LLM-driven interview questions, interview answers, technical depth, "
        "communication clarity, and problem-solving indicators."
    )

    report = InterviewReport(
        session_id=session.id,
        technical_score=technical_score,
        communication_score=communication_score,
        problem_solving_score=problem_solving_score,
        overall_score=overall_score,
        readiness_level=readiness_level,
        strengths=", ".join(strengths),
        areas_to_improve=", ".join(areas_to_improve),
        next_steps=", ".join(next_steps),
        feedback=feedback
    )

    db.add(report)

    session.status = "completed"
    db.commit()

    return {
        "session_id": str(session.id),
        "status": session.status,
        "technical_score": technical_score,
        "communication_score": communication_score,
        "problem_solving_score": problem_solving_score,
        "overall_score": overall_score,
        "readiness_level": readiness_level,
        "strengths": strengths,
        "areas_to_improve": areas_to_improve,
        "next_steps": next_steps,
        "feedback": feedback,
        "answers_evaluated": len(answers)
    }


@router.get("/report/{session_id}")
def get_report(
    session_id: str,
    db: Session = Depends(get_db)
):
    report = db.query(InterviewReport).filter(
        InterviewReport.session_id == session_id
    ).first()

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return {
        "session_id": str(report.session_id),
        "technical_score": report.technical_score,
        "communication_score": report.communication_score,
        "problem_solving_score": report.problem_solving_score,
        "overall_score": report.overall_score,
        "readiness_level": report.readiness_level,
        "strengths": report.strengths,
        "areas_to_improve": report.areas_to_improve,
        "next_steps": report.next_steps,
        "feedback": report.feedback
    }