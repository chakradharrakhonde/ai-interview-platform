from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, CodingQuestion
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/coding", tags=["Coding Questions"])

def get_current_user(db: Session = Depends(get_db), user_id: str = Depends(lambda: "user_id")):
    """Get current authenticated user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return user

@router.get("/questions")
async def get_coding_questions(
    difficulty: str = "medium",
    topic: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10
):
    """Get recommended coding questions"""
    query = db.query(CodingQuestion).filter(
        CodingQuestion.difficulty == difficulty
    )
    
    if topic:
        query = query.filter(CodingQuestion.topic == topic)
    
    questions = query.offset(skip).limit(limit).all()
    
    return {
        "questions": [
            {
                "id": q.id,
                "title": q.title,
                "difficulty": q.difficulty,
                "topic": q.topic
            }
            for q in questions
        ]
    }

@router.get("/questions/{question_id}")
async def get_coding_question(
    question_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get coding question details"""
    question = db.query(CodingQuestion).filter(
        CodingQuestion.id == question_id
    ).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    return {
        "id": question.id,
        "title": question.title,
        "description": question.description,
        "difficulty": question.difficulty,
        "topic": question.topic,
        "examples": question.examples,
        "constraints": question.constraints,
        "follow_up": question.follow_up
    }

@router.post("/submit")
async def submit_coding_solution(
    submission_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit coding solution"""
    logger.info(f"Coding solution submitted: {current_user.id}")
    
    return {
        "message": "Solution submitted for evaluation",
        "submission_id": "sub_123"
    }
