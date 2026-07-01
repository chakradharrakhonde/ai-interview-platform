"""Resume Management Routes"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from uuid import UUID
import os

from app.database import get_db
from app.models import Resume
from app.schemas.resume import ResumeResponse, ResumeFeedback
from app.config import settings

router = APIRouter()


@router.post("/upload", response_model=dict)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: str = "550e8400-e29b-41d4-a716-446655440000",
):
    """Upload resume"""
    if not file.content_type.startswith("application/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type"
        )
    
    os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIRECTORY, file.filename)
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    resume = Resume(
        user_id=UUID(user_id),
        file_path=file_path,
        file_name=file.filename,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    
    return {
        "id": str(resume.id),
        "message": "Resume uploaded successfully",
        "file_name": resume.file_name,
    }


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(resume_id: UUID, db: Session = Depends(get_db)):
    """Get resume details"""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    return resume


@router.post("/{resume_id}/score", response_model=ResumeFeedback)
async def score_resume(resume_id: UUID, db: Session = Depends(get_db)):
    """Get ATS score for resume"""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    resume.ats_score = 85.0
    resume.feedback = "Strong resume with good structure"
    resume.skills = ["Python", "FastAPI", "PostgreSQL", "AWS"]
    resume.experience_years = 5
    db.commit()
    db.refresh(resume)
    
    return ResumeFeedback(
        ats_score=resume.ats_score,
        feedback=resume.feedback,
        skills=resume.skills or [],
        experience_years=resume.experience_years or 0,
        suggestions=["Add more quantifiable metrics", "Include certifications"],
    )


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(resume_id: UUID, db: Session = Depends(get_db)):
    """Delete resume"""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)
    
    db.delete(resume)
    db.commit()
