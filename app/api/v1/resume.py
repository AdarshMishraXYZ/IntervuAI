from fastapi import HTTPException
from fastapi import status

from app.services.resume_service import analyze_resume_text
import os
import uuid

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.resume import Resume
from app.services.resume_service import extract_text_from_pdf

router = APIRouter()

UPLOAD_DIR = "uploads/resumes"


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_extension = file.filename.split(".")[-1]

    unique_filename = (
        str(uuid.uuid4())
        + "."
        + file_extension
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    content = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    extracted_text = extract_text_from_pdf(
        file_path
    )

    resume = Resume(
        user_id="a4b1b6ad-f44d-4178-b677-c8cc06541292",
        file_name=file.filename,
        file_path=file_path,
        raw_text=extracted_text
    )

    db.add(resume)

    db.commit()

    db.refresh(resume)

    return {
        "resume_id": str(resume.id),
        "file_name": resume.file_name
    }
@router.get("/{resume_id}/analysis")
def get_resume_analysis(
    resume_id: str,
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    analysis = analyze_resume_text(
        resume.raw_text
    )

    resume.skills = ", ".join(
        analysis["skills"]
    )

    resume.resume_score = analysis["resume_score"]

    db.commit()
    db.refresh(resume)

    return {
        "resume_id": str(resume.id),
        "file_name": resume.file_name,
        "skills": analysis["skills"],
        "resume_score": analysis["resume_score"],
        "text_preview": analysis["text_preview"]
    }
@router.get("/list")
def list_resumes(
    db: Session = Depends(get_db)
):
    resumes = db.query(Resume).all()

    return {
        "count": len(resumes),
        "resumes": [
            {
                "id": str(resume.id),
                "file_name": resume.file_name,
                "skills": resume.skills,
                "resume_score": resume.resume_score
            }
            for resume in resumes
        ]
    }


@router.get("/{resume_id}")
def get_resume(
    resume_id: str,
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(
        Resume.id == resume_id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )

    return {
        "id": str(resume.id),
        "user_id": str(resume.user_id),
        "file_name": resume.file_name,
        "file_path": resume.file_path,
        "skills": resume.skills,
        "resume_score": resume.resume_score,
        "created_at": resume.created_at
    }