from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    interviews = relationship("Interview", back_populates="user", cascade="all, delete-orphan")
    roadmaps = relationship("LearningRoadmap", back_populates="user", cascade="all, delete-orphan")

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    ats_score = Column(Float, nullable=True)
    parsed_data = Column(JSON, nullable=True)
    analysis = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="resumes")

class Interview(Base):
    __tablename__ = "interviews"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    interview_type = Column(String(50), nullable=False)  # technical, behavioral, coding
    status = Column(String(50), default="in_progress")  # in_progress, completed, abandoned
    role = Column(String(255), nullable=True)
    difficulty = Column(String(50), default="medium")  # easy, medium, hard
    overall_feedback = Column(Text, nullable=True)
    overall_score = Column(Float, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="interviews")
    answers = relationship("InterviewAnswer", back_populates="interview", cascade="all, delete-orphan")

class InterviewAnswer(Base):
    __tablename__ = "interview_answers"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    interview_id = Column(String(36), ForeignKey("interviews.id"), nullable=False, index=True)
    question_number = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    text_response = Column(Text, nullable=True)
    audio_url = Column(String(500), nullable=True)
    feedback = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    sentiment = Column(String(50), nullable=True)  # positive, neutral, negative
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    interview = relationship("Interview", back_populates="answers")

class CodingQuestion(Base):
    __tablename__ = "coding_questions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String(50), nullable=False)  # easy, medium, hard
    topic = Column(String(100), nullable=False)  # arrays, strings, trees, graphs, etc
    examples = Column(JSON, nullable=True)
    constraints = Column(Text, nullable=True)
    follow_up = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CodingSubmission(Base):
    __tablename__ = "coding_submissions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    question_id = Column(String(36), ForeignKey("coding_questions.id"), nullable=False)
    code = Column(Text, nullable=False)
    language = Column(String(50), nullable=False)
    status = Column(String(50), default="pending")  # pending, passed, failed, error
    test_results = Column(JSON, nullable=True)
    feedback = Column(Text, nullable=True)
    execution_time = Column(Float, nullable=True)
    memory_usage = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class LearningRoadmap(Base):
    __tablename__ = "learning_roadmaps"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    role = Column(String(255), nullable=True)
    level = Column(String(50), default="intermediate")  # beginner, intermediate, advanced
    topics = Column(JSON, nullable=True)  # list of topics to study
    progress = Column(JSON, nullable=True)  # progress per topic
    recommendations = Column(JSON, nullable=True)  # recommended resources
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="roadmaps")
