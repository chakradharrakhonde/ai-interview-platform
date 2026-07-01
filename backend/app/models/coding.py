"""Coding Question Model"""
from sqlalchemy import Column, String, Text, Integer, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID, JSON, ARRAY
from datetime import datetime
import uuid

from app.database import Base


class CodingQuestion(Base):
    __tablename__ = "coding_questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String(20), nullable=False)
    topic = Column(String(100), nullable=False)
    languages = Column(ARRAY(String), default=["python", "javascript", "java"])
    time_limit_minutes = Column(Integer, default=30)
    memory_limit_mb = Column(Integer, default=256)
    test_cases = Column(JSON, nullable=False)
    examples = Column(JSON, nullable=True)
    hints = Column(JSON, nullable=True)
    solution = Column(Text, nullable=True)
    acceptance_rate = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<CodingQuestion {self.title}>"
