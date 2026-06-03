import os
import logging
from typing import Optional
import openai
from app.config import settings

logger = logging.getLogger(__name__)

openai.api_key = settings.OPENAI_API_KEY

class LLMService:
    """Service for LLM operations"""
    
    @staticmethod
    async def generate_interview_questions(
        interview_type: str,
        role: str,
        difficulty: str,
        num_questions: int = 5
    ) -> list:
        """Generate interview questions using GPT"""
        try:
            prompt = f"""Generate {num_questions} {interview_type} interview questions for a {role} position at {difficulty} difficulty level.
            
Format as JSON array with objects containing:
- question: the interview question
- difficulty: difficulty level
- follow_up: optional follow-up question

Return only valid JSON."""
            
            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert interview coach."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            import json
            questions = json.loads(response.choices[0].message.content)
            return questions
        except Exception as e:
            logger.error(f"Error generating questions: {e}")
            return []
    
    @staticmethod
    async def evaluate_interview_response(
        question: str,
        answer: str,
        interview_type: str
    ) -> dict:
        """Evaluate interview response using GPT"""
        try:
            prompt = f"""Evaluate this {interview_type} interview answer.
            
Question: {question}
Answer: {answer}

Provide feedback in JSON format with:
- score: 1-10
- strengths: list of strengths
- improvements: list of improvements
- sentiment: positive/neutral/negative
- feedback: detailed feedback paragraph

Return only valid JSON."""
            
            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert interview evaluator. Be constructive and fair."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1000
            )
            
            import json
            evaluation = json.loads(response.choices[0].message.content)
            return evaluation
        except Exception as e:
            logger.error(f"Error evaluating response: {e}")
            return {
                "score": 0,
                "feedback": "Unable to evaluate at this time",
                "strengths": [],
                "improvements": []
            }
    
    @staticmethod
    async def analyze_resume(resume_text: str) -> dict:
        """Analyze resume using GPT"""
        try:
            prompt = f"""Analyze this resume and provide an ATS score (0-100) and analysis.

Resume:
{resume_text}

Provide in JSON format:
- ats_score: 0-100
- strengths: list of resume strengths
- improvements: list of improvements needed
- keywords_present: list of strong keywords found
- keywords_missing: list of recommended keywords
- overall_feedback: brief overall assessment

Return only valid JSON."""
            
            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an ATS expert and resume coach."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            import json
            analysis = json.loads(response.choices[0].message.content)
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing resume: {e}")
            return {
                "ats_score": 0,
                "analysis": "Unable to analyze at this time",
                "strengths": [],
                "improvements": []
            }
    
    @staticmethod
    async def generate_learning_roadmap(
        role: str,
        level: str,
        weak_areas: Optional[list] = None
    ) -> dict:
        """Generate personalized learning roadmap"""
        try:
            weak_areas_str = ", ".join(weak_areas) if weak_areas else "None identified"
            
            prompt = f"""Create a personalized learning roadmap for a {level} level candidate applying for {role} role.
Weak areas identified: {weak_areas_str}

Provide in JSON format with:
- topics: array of topics with name, status, resources (links to learning materials)
- timeline: estimated weeks to complete
- priorities: array of high priority items
- recommendations: personalized recommendations

Return only valid JSON."""
            
            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a career coach and learning path expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            import json
            roadmap = json.loads(response.choices[0].message.content)
            return roadmap
        except Exception as e:
            logger.error(f"Error generating roadmap: {e}")
            return {
                "topics": [],
                "recommendations": [],
                "error": "Unable to generate roadmap at this time"
            }
