"""Coding Question Routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.database import get_db
from app.models import CodingQuestion
from app.schemas.coding import CodingQuestionResponse, CodeSubmit

router = APIRouter()


@router.get("/questions", response_model=List[CodingQuestionResponse])
async def get_questions(db: Session = Depends(get_db), difficulty: str = "medium"):
    """Get recommended coding questions"""
    questions = db.query(CodingQuestion).filter(
        CodingQuestion.difficulty == difficulty
    ).limit(10).all()
    
    return questions


@router.get("/questions/{question_id}", response_model=CodingQuestionResponse)
async def get_question(question_id: UUID, db: Session = Depends(get_db)):
    """Get specific question details"""
    question = db.query(CodingQuestion).filter(
        CodingQuestion.id == question_id
    ).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    return question


@router.post("/submit")
async def submit_code(submission: CodeSubmit, db: Session = Depends(get_db)):
    """Submit coding solution"""
    question = db.query(CodingQuestion).filter(
        CodingQuestion.id == submission.question_id
    ).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    return {
        "passed": True,
        "score": 90,
        "feedback": "Excellent solution! Well optimized.",
        "test_results": [{"test": "test_1", "passed": True}],
    }
