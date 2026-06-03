from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Resume
from app.schemas import ResumeUploadResponse, ResumeScoreResponse, ResumeAnalysis
from app.services.resume import ResumeParser
from app.services.llm import LLMService
from app.config import settings
from pathlib import Path
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/resumes", tags=["Resumes"])

def get_current_user(db: Session = Depends(get_db), user_id: str = Depends(lambda: "user_id")):
    """Get current authenticated user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return user

@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload resume file"""
    # Validate file type
    file_ext = Path(file.filename).suffix.lower()
    if file_ext.lstrip('.') not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Check file size
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed: {settings.MAX_UPLOAD_SIZE / 1024 / 1024:.1f}MB"
        )
    
    # Create upload directory
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Save file
    file_path = os.path.join(settings.UPLOAD_DIR, f"{current_user.id}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Parse resume
    resume_text = ResumeParser.parse_resume(file_path)
    metadata = ResumeParser.extract_metadata(resume_text)
    
    # Create database record
    db_resume = Resume(
        user_id=current_user.id,
        file_path=file_path,
        file_name=file.filename,
        parsed_data=metadata
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    
    logger.info(f"Resume uploaded: {current_user.id} - {file.filename}")
    
    return db_resume

@router.get("/{resume_id}", response_model=ResumeAnalysis)
async def get_resume(
    resume_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get resume details"""
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    return resume

@router.post("/{resume_id}/score", response_model=ResumeScoreResponse)
async def score_resume(
    resume_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get ATS score for resume"""
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Parse resume text
    resume_text = ResumeParser.parse_resume(resume.file_path)
    
    # Get analysis from LLM
    analysis = await LLMService.analyze_resume(resume_text)
    
    # Update database
    resume.ats_score = analysis.get("ats_score", 0)
    resume.analysis = analysis.get("overall_feedback", "")
    db.commit()
    
    logger.info(f"Resume scored: {resume_id} - Score: {resume.ats_score}")
    
    return ResumeScoreResponse(
        resume_id=resume_id,
        ats_score=resume.ats_score,
        analysis=resume.analysis,
        suggestions=analysis.get("improvements", [])
    )

@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete resume"""
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Delete file
    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)
    
    # Delete from database
    db.delete(resume)
    db.commit()
    
    logger.info(f"Resume deleted: {resume_id}")
