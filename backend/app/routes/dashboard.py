"""Dashboard Routes"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.models import Interview, Resume

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    user_id: str = "550e8400-e29b-41d4-a716-446655440000",
):
    """Get user dashboard statistics"""
    user_uuid = UUID(user_id)
    
    total_interviews = db.query(Interview).filter(
        Interview.user_id == user_uuid
    ).count()
    
    avg_score = 0
    interviews = db.query(Interview).filter(
        Interview.user_id == user_uuid,
        Interview.score != None
    ).all()
    
    if interviews:
        avg_score = sum(i.score for i in interviews) / len(interviews)
    
    resumes = db.query(Resume).filter(
        Resume.user_id == user_uuid
    ).all()
    
    latest_resume = resumes[-1] if resumes else None
    
    return {
        "total_interviews": total_interviews,
        "average_score": avg_score,
        "total_resumes": len(resumes),
        "latest_resume_score": latest_resume.ats_score if latest_resume else None,
    }
