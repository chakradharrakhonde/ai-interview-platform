"""Interview Routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.models import Interview, InterviewAnswer
from app.schemas.interview import InterviewStart, InterviewResponse, AnswerSubmit

router = APIRouter()


@router.post("/start", response_model=InterviewResponse)
async def start_interview(
    interview_data: InterviewStart,
    db: Session = Depends(get_db),
    user_id: str = "550e8400-e29b-41d4-a716-446655440000",
):
    """Start a new mock interview"""
    interview = Interview(
        user_id=UUID(user_id),
        type=interview_data.type,
        title=interview_data.title,
        duration_minutes=interview_data.duration_minutes,
    )
    db.add(interview)
    db.commit()
    db.refresh(interview)
    
    return interview


@router.post("/{interview_id}/answer")
async def submit_answer(
    interview_id: UUID,
    answer: AnswerSubmit,
    db: Session = Depends(get_db),
):
    """Submit an answer to an interview question"""
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    interview_answer = InterviewAnswer(
        interview_id=interview_id,
        question_number=answer.question_number,
        question_text=answer.question_text,
        text_response=answer.text_response,
        audio_url=answer.audio_url,
        feedback="Great answer! Well structured and clear.",
        score=85,
    )
    db.add(interview_answer)
    db.commit()
    db.refresh(interview_answer)
    
    return {
        "answer_id": str(interview_answer.id),
        "feedback": interview_answer.feedback,
        "score": interview_answer.score,
    }


@router.get("/{interview_id}/feedback")
async def get_interview_feedback(
    interview_id: UUID,
    db: Session = Depends(get_db),
):
    """Get interview feedback"""
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    answers = db.query(InterviewAnswer).filter(
        InterviewAnswer.interview_id == interview_id
    ).all()
    
    return {
        "interview_id": str(interview.id),
        "overall_feedback": interview.feedback or "No feedback yet",
        "answers": [
            {
                "question_number": a.question_number,
                "feedback": a.feedback,
                "score": a.score,
            }
            for a in answers
        ],
    }


@router.get("/history")
async def get_interview_history(
    db: Session = Depends(get_db),
    user_id: str = "550e8400-e29b-41d4-a716-446655440000",
):
    """Get interview history"""
    interviews = db.query(Interview).filter(
        Interview.user_id == UUID(user_id)
    ).all()
    
    return {
        "interviews": [
            {
                "id": str(i.id),
                "type": i.type,
                "status": i.status,
                "score": i.score,
                "created_at": i.created_at.isoformat(),
            }
            for i in interviews
        ]
    }
