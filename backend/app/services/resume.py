import os
import logging
import PyPDF2
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from app.config import settings

logger = logging.getLogger(__name__)

class ResumeParser:
    """Service for parsing resumes"""
    
    @staticmethod
    def parse_pdf(file_path: str) -> str:
        """Extract text from PDF"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            logger.error(f"Error parsing PDF: {e}")
            return ""
    
    @staticmethod
    def parse_docx(file_path: str) -> str:
        """Extract text from DOCX"""
        try:
            text = ""
            with zipfile.ZipFile(file_path) as docx:
                xml_content = docx.read('word/document.xml')
                root = ET.fromstring(xml_content)
                
                namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                for paragraph in root.findall('.//w:p', namespace):
                    for text_elem in paragraph.findall('.//w:t', namespace):
                        if text_elem.text:
                            text += text_elem.text
                    text += "\n"
            return text
        except Exception as e:
            logger.error(f"Error parsing DOCX: {e}")
            return ""
    
    @staticmethod
    def parse_doc(file_path: str) -> str:
        """Extract text from DOC (basic)"""
        # Basic implementation - in production use python-docx or similar
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error parsing DOC: {e}")
            return ""
    
    @staticmethod
    def parse_txt(file_path: str) -> str:
        """Extract text from TXT"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error parsing TXT: {e}")
            return ""
    
    @staticmethod
    def parse_resume(file_path: str) -> str:
        """Parse resume based on file type"""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            return ResumeParser.parse_pdf(file_path)
        elif file_ext == '.docx':
            return ResumeParser.parse_docx(file_path)
        elif file_ext == '.doc':
            return ResumeParser.parse_doc(file_path)
        elif file_ext == '.txt':
            return ResumeParser.parse_txt(file_path)
        else:
            logger.warning(f"Unsupported file type: {file_ext}")
            return ""
    
    @staticmethod
    def extract_metadata(resume_text: str) -> dict:
        """Extract basic metadata from resume text"""
        # Simple keyword extraction
        metadata = {
            "skills": [],
            "experience_years": 0,
            "languages": [],
            "certifications": []
        }
        
        # This is a basic implementation
        # In production, use NLP or more sophisticated parsing
        
        common_skills = [
            "python", "java", "javascript", "sql", "react", "fastapi",
            "docker", "kubernetes", "aws", "gcp", "azure", "git",
            "machine learning", "deep learning", "nlp", "computer vision"
        ]
        
        resume_lower = resume_text.lower()
        for skill in common_skills:
            if skill in resume_lower:
                metadata["skills"].append(skill)
        
        return metadata
