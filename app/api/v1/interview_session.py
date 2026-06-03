from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.interview import InterviewSession
from app.models.interview import InterviewAnswer
from app.models.resume import Resume
from app.models.interview_report import InterviewReport

router = APIRouter()


QUESTIONS = [
    "Explain JWT authentication.",
    "How would you design a scalable REST API?",
    "What is database indexing?",
    "How do transactions work in PostgreSQL?",
    "Describe a challenging project you built."
]


class StartInterviewRequest(BaseModel):
    role: str


class SubmitAnswerRequest(BaseModel):
    session_id: str
    answer: str


class EndInterviewRequest(BaseModel):
    session_id: str


@router.post("/start")
def start_interview(
    payload: StartInterviewRequest,
    db: Session = Depends(get_db)
):
    session = InterviewSession(
        user_id="a4b1b6ad-f44d-4178-b677-c8cc06541292",
        role=payload.role
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "session_id": str(session.id),
        "question_number": 1,
        "question": QUESTIONS[0]
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

    previous_answers_count = db.query(InterviewAnswer).filter(
        InterviewAnswer.session_id == payload.session_id
    ).count()

    if previous_answers_count >= len(QUESTIONS):
        return {
            "message": "Interview already completed. Please end the interview for final evaluation."
        }

    current_question = QUESTIONS[previous_answers_count]

    answer = InterviewAnswer(
        session_id=session.id,
        question=current_question,
        answer=payload.answer
    )

    db.add(answer)
    db.commit()

    next_question_index = previous_answers_count + 1

    if next_question_index >= len(QUESTIONS):
        return {
            "message": "All questions answered. Please end the interview for final evaluation.",
            "next_question": None
        }

    return {
        "question_number": next_question_index + 1,
        "next_question": QUESTIONS[next_question_index]
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
        "The current readiness level is based on resume signals, interview answers, "
        "technical depth, communication clarity, and problem-solving indicators."
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
@router.post("/demo-complete")
def demo_complete_interview(
    db: Session = Depends(get_db)
):
    session = InterviewSession(
        user_id="a4b1b6ad-f44d-4178-b677-c8cc06541292",
        role="Backend Developer"
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    demo_answers = [
        "JWT is used for authentication using signed tokens.",
        "A scalable REST API uses proper routing, database design, caching, and load balancing.",
        "Database indexing improves query speed by allowing faster lookup.",
        "Transactions ensure consistency using commit and rollback.",
        "I built IntervuAI using FastAPI, PostgreSQL, resume analysis, GitHub analysis, and interview evaluation."
    ]

    for index, answer_text in enumerate(demo_answers):
        answer = InterviewAnswer(
            session_id=session.id,
            question=QUESTIONS[index],
            answer=answer_text
        )

        db.add(answer)

    db.commit()

    return {
        "message": "Demo interview completed",
        "session_id": str(session.id),
        "next_step": "Call /api/v1/interview-session/end with this session_id"
    }