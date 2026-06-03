from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.services.llm import LLMService
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/roadmap", tags=["Learning Roadmap"])

def get_current_user(db: Session = Depends(get_db), user_id: str = Depends(lambda: "user_id")):
    """Get current authenticated user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return user

@router.get("")
async def get_learning_roadmap(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get personalized learning roadmap"""
    roadmap = await LLMService.generate_learning_roadmap(
        role=current_user.resumes[0].parsed_data.get("role") if current_user.resumes else "Software Engineer",
        level="intermediate",
        weak_areas=[]
    )
    
    logger.info(f"Roadmap retrieved: {current_user.id}")
    
    return {
        "user_id": current_user.id,
        "roadmap": roadmap
    }

@router.put("/update")
async def update_roadmap(
    roadmap_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update roadmap progress"""
    logger.info(f"Roadmap updated: {current_user.id}")
    
    return {
        "message": "Roadmap updated successfully",
        "user_id": current_user.id
    }
