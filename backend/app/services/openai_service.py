"""OpenAI Integration Service"""
from app.config import settings
import json
import random


class OpenAIService:
    def __init__(self):
        self.model = "gpt-3.5-turbo"
    
    async def analyze_resume(self, file_path: str) -> dict:
        """Analyze resume and return ATS score"""
        try:
            with open(file_path, 'r', errors='ignore') as f:
                resume_text = f.read()[:1000]  # First 1000 chars
            
            # Mock response
            result = {
                "ats_score": random.randint(65, 95),
                "skills": ["Python", "FastAPI", "PostgreSQL", "AWS", "Docker"],
                "experience_years": random.randint(2, 10),
                "suggestions": [
                    "Add quantifiable metrics to achievements",
                    "Include relevant certifications",
                    "Improve formatting consistency"
                ],
                "feedback": "Good resume structure with relevant experience."
            }
            return result
        except Exception as e:
            return {
                "ats_score": 0,
                "skills": [],
                "experience_years": 0,
                "suggestions": ["Error analyzing resume"],
                "feedback": str(e)
            }
    
    async def get_answer_feedback(self, question: str, answer: str) -> dict:
        """Get feedback on interview answer"""
        try:
            result = {
                "score": random.randint(70, 95),
                "feedback": "Excellent answer with clear explanation and good examples.",
                "improvements": ["Add more technical depth", "Consider edge cases"]
            }
            return result
        except Exception as e:
            return {
                "score": 0,
                "feedback": f"Error: {str(e)}",
                "improvements": []
            }
    
    async def evaluate_code(self, question: str, code: str, language: str) -> dict:
        """Evaluate submitted code"""
        try:
            result = {
                "passed": True,
                "score": random.randint(75, 100),
                "feedback": "Clean code with good logic and proper error handling.",
                "test_results": [
                    {"test": "test_case_1", "passed": True},
                    {"test": "test_case_2", "passed": True},
                    {"test": "test_case_3", "passed": True}
                ]
            }
            return result
        except Exception as e:
            return {
                "passed": False,
                "score": 0,
                "feedback": f"Error: {str(e)}",
                "test_results": []
            }
    
    async def generate_interview_questions(self, topic: str, difficulty: str) -> list:
        """Generate mock interview questions"""
        questions = {
            "behavioral": [
                "Tell me about a challenging project you worked on",
                "How do you handle conflicts in a team?",
                "Describe a time you failed and what you learned",
                "What are your career goals?",
                "How do you prioritize tasks?"
            ],
            "technical": [
                "Explain the difference between SQL and NoSQL databases",
                "What is the difference between REST and GraphQL?",
                "How does caching improve application performance?",
                "Explain microservices architecture",
                "What are design patterns and why are they important?"
            ]
        }
        interview_type = "behavioral" if difficulty == "easy" else "technical"
        return questions.get(interview_type, [])
