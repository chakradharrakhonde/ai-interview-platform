"""Coding Question Schemas"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import UUID


class CodingQuestionResponse(BaseModel):
    id: UUID
    title: str
    description: str
    difficulty: str
    topic: str
    time_limit_minutes: int
    examples: Optional[List[Dict[str, Any]]]
    hints: Optional[List[str]]

    class Config:
        from_attributes = True


class CodeSubmit(BaseModel):
    code: str
    language: str
    question_id: UUID
