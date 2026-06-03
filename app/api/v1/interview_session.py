import uuid

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.interview import InterviewSession
from app.models.interview import InterviewAnswer

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

    current_question = QUESTIONS[
        previous_answers_count
    ]

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
class EndInterviewRequest(BaseModel):
    session_id: str


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

    if overall_score >= 80:
        recommendation = "Strong chances"
    elif overall_score >= 65:
        recommendation = "Good Chances"
    elif overall_score >= 50:
        recommendation = "Moderate Chances"
    else:
        recommendation = "Need Improvement "

    session.status = "completed"
    db.commit()

    return {
        "session_id": str(session.id),
        "status": session.status,
        "technical_score": technical_score,
        "communication_score": communication_score,
        "problem_solving_score": problem_solving_score,
        "overall_score": overall_score,
        "recommendation": recommendation,
        "answers_evaluated": len(answers)
    }