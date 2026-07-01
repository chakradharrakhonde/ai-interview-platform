"""Learning Roadmap Model"""
from sqlalchemy import Column, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON, ARRAY
from datetime import datetime
import uuid

from app.database import Base


class LearningRoadmap(Base):
    __tablename__ = "learning_roadmaps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    goal = Column(String(255), nullable=True)
    target_role = Column(String(100), nullable=True)
    difficulty_level = Column(String(20), default="intermediate")
    topics = Column(ARRAY(String), nullable=True)
    progress_percentage = Column(Float, default=0.0)
    completed_topics = Column(ARRAY(String), default=[])
    recommendations = Column(JSON, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<LearningRoadmap {self.title}>"
