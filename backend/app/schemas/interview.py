"""Interview Schemas"""
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from enum import Enum


class InterviewTypeEnum(str, Enum):
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    CODING = "coding"


class InterviewStart(BaseModel):
    type: InterviewTypeEnum
    title: Optional[str] = None
    duration_minutes: Optional[int] = 30


class AnswerSubmit(BaseModel):
    question_number: int
    question_text: str
    text_response: Optional[str] = None
    audio_url: Optional[str] = None


class InterviewResponse(BaseModel):
    id: UUID
    type: str
    status: str
    score: Optional[int]
    feedback: Optional[str]
    created_at: str

    class Config:
        from_attributes = True
