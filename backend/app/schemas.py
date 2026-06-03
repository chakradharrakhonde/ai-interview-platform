from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)

class UserResponse(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Resume Schemas
class ResumeUploadResponse(BaseModel):
    id: str
    file_name: str
    file_path: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ResumeScoreResponse(BaseModel):
    resume_id: str
    ats_score: float
    analysis: str
    suggestions: List[str]

class ResumeAnalysis(BaseModel):
    id: str
    ats_score: float
    parsed_data: Optional[Dict[str, Any]]
    analysis: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Interview Schemas
class InterviewStart(BaseModel):
    interview_type: str  # technical, behavioral, coding
    role: Optional[str] = None
    difficulty: str = "medium"

class InterviewQuestion(BaseModel):
    question_number: int
    question_text: str
    estimated_time: int

class InterviewAnswer(BaseModel):
    question_number: int
    text_response: Optional[str] = None
    audio_url: Optional[str] = None

class InterviewFeedback(BaseModel):
    question_number: int
    feedback: str
    score: float
    sentiment: Optional[str]

class InterviewResponse(BaseModel):
    id: str
    interview_type: str
    status: str
    role: Optional[str]
    overall_score: Optional[float]
    overall_feedback: Optional[str]
    started_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Coding Question Schemas
class CodingQuestionResponse(BaseModel):
    id: str
    title: str
    description: str
    difficulty: str
    topic: str
    examples: Optional[List[Dict[str, Any]]]
    constraints: Optional[str]
    
    class Config:
        from_attributes = True

class CodeSubmission(BaseModel):
    code: str
    language: str

class CodeSubmissionResponse(BaseModel):
    id: str
    status: str
    test_results: Optional[Dict[str, Any]]
    feedback: Optional[str]
    execution_time: Optional[float]
    
    class Config:
        from_attributes = True

# Learning Roadmap Schemas
class RoadmapTopic(BaseModel):
    name: str
    status: str  # not_started, in_progress, completed
    progress: float  # 0-100

class LearningRoadmapResponse(BaseModel):
    id: str
    role: Optional[str]
    level: str
    topics: List[RoadmapTopic]
    recommendations: Optional[List[Dict[str, str]]]
    last_updated: datetime
    
    class Config:
        from_attributes = True

# Auth Schemas
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRequest(BaseModel):
    email: EmailStr
    password: str

# Health Check
class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
