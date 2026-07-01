"""Resume Schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID


class ResumeUpload(BaseModel):
    file_name: str
    file_size: int


class ResumeFeedback(BaseModel):
    ats_score: float = Field(..., ge=0, le=100)
    feedback: str
    skills: List[str]
    experience_years: int
    suggestions: List[str]


class ResumeResponse(BaseModel):
    id: UUID
    file_name: str
    ats_score: Optional[float]
    feedback: Optional[str]
    skills: Optional[List[str]]
    created_at: str

    class Config:
        from_attributes = True
