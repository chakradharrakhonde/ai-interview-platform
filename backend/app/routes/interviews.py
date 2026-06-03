from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Interview, InterviewAnswer
from app.schemas import InterviewStart, InterviewFeedback, InterviewResponse
from app.services.llm import LLMService
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/interviews", tags=["Interviews"])

def get_current_user(db: Session = Depends(get_db), user_id: str = Depends(lambda: "user_id")):
    """Get current authenticated user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return user

@router.post("/start", response_model=dict)
async def start_interview(
    interview_config: InterviewStart,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start mock interview"""
    # Create interview record
    db_interview = Interview(
        user_id=current_user.id,
        interview_type=interview_config.interview_type,
        role=interview_config.role,
        difficulty=interview_config.difficulty,
        status="in_progress"
    )
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    
    # Generate questions
    questions = await LLMService.generate_interview_questions(
        interview_type=interview_config.interview_type,
        role=interview_config.role or "Software Engineer",
        difficulty=interview_config.difficulty,
        num_questions=5
    )
    
    logger.info(f"Interview started: {db_interview.id} - Type: {interview_config.interview_type}")
    
    return {
        "interview_id": db_interview.id,
        "questions": questions,
        "message": "Interview started successfully"
    }

@router.post("/{interview_id}/answer")
async def submit_answer(
    interview_id: str,
    answer_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit interview answer"""
    interview = db.query(Interview).filter(
        Interview.id == interview_id,
        Interview.user_id == current_user.id
    ).first()
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    # Evaluate answer
    evaluation = await LLMService.evaluate_interview_response(
        question=answer_data.get("question", ""),
        answer=answer_data.get("text_response", ""),
        interview_type=interview.interview_type
    )
    
    # Store answer
    db_answer = InterviewAnswer(
        interview_id=interview_id,
        question_number=answer_data.get("question_number", 0),
        question_text=answer_data.get("question", ""),
        text_response=answer_data.get("text_response"),
        audio_url=answer_data.get("audio_url"),
        feedback=evaluation.get("feedback", ""),
        score=evaluation.get("score", 0),
        sentiment=evaluation.get("sentiment")
    )
    db.add(db_answer)
    db.commit()
    
    logger.info(f"Answer submitted: {interview_id}")
    
    return {
        "answer_id": db_answer.id,
        "score": evaluation.get("score"),
        "feedback": evaluation.get("feedback"),
        "message": "Answer evaluated"
    }

@router.get("/{interview_id}/feedback")
async def get_interview_feedback(
    interview_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get interview feedback"""
    interview = db.query(Interview).filter(
        Interview.id == interview_id,
        Interview.user_id == current_user.id
    ).first()
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    answers = db.query(InterviewAnswer).filter(
        InterviewAnswer.interview_id == interview_id
    ).all()
    
    # Calculate overall score
    scores = [a.score for a in answers if a.score is not None]
    overall_score = sum(scores) / len(scores) if scores else 0
    
    interview.overall_score = overall_score
    interview.status = "completed"
    interview.completed_at = datetime.utcnow()
    db.commit()
    
    return {
        "interview_id": interview_id,
        "overall_score": overall_score,
        "answers": [
            {
                "question_number": a.question_number,
                "score": a.score,
                "feedback": a.feedback,
                "sentiment": a.sentiment
            }
            for a in answers
        ]
    }

@router.get("/history")
async def get_interview_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10
):
    """Get interview history"""
    interviews = db.query(Interview).filter(
        Interview.user_id == current_user.id
    ).order_by(Interview.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "interviews": [
            {
                "id": i.id,
                "type": i.interview_type,
                "status": i.status,
                "overall_score": i.overall_score,
                "completed_at": i.completed_at,
                "created_at": i.created_at
            }
            for i in interviews
        ]
    }
