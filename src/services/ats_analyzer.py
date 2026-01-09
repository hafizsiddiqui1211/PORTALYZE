"""ATS scoring service for Resume Analyzer Core"""
import re
from typing import List, Dict, Any
from src.utils.constants import ATS_KEYWORD_WEIGHT, ATS_FORMATTING_WEIGHT, ATS_SECTION_WEIGHT
from src.utils.logger import get_logger


class ATSAnalyzer:
    """Analyzes resume content and calculates ATS compatibility score"""

    def __init__(self):
        self.logger = get_logger("ATSAnalyzer")

        # Common keywords for tech roles
        self.tech_keywords = [
            # Programming languages
            "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "TypeScript", "PHP", "Ruby",
            # Frameworks and libraries
            "React", "Angular", "Vue", "Node.js", "Django", "Flask", "Spring", "Express", "FastAPI",
            # Technologies and tools
            "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Git", "Jenkins", "CI/CD", "SQL", "MongoDB",
            "PostgreSQL", "MySQL", "Linux", "Unix", "REST", "API", "Agile", "Scrum", "Jira",
            # Skills
            "Machine Learning", "AI", "Data Science", "DevOps", "Full Stack", "Frontend", "Backend",
            "Cloud", "Microservices", "Testing", "TDD", "BDD", "Security", "CI/CD", "Automation"
        ]

        # Common resume sections
        self.resume_sections = [
            "experience", "education", "skills", "summary", "objective", "projects",
            "certifications", "awards", "contact", "references"
        ]

    def calculate_ats_score(self, resume_text: str) -> float:
        """
        Calculate ATS compatibility score based on keyword presence, formatting, and section completeness.

        Args:
            resume_text: The text content of the resume

        Returns:
            ATS compatibility score (0-100)
        """
        self.logger.info("Starting ATS score calculation")

        if not resume_text:
            self.logger.warning("Empty resume text provided, returning score of 0.0")
            return 0.0

        # Log resume text length for debugging
        self.logger.debug(f"Analyzing resume text of length: {len(resume_text)} characters")

        # Analyze different aspects of the resume
        keyword_score = self._analyze_keywords(resume_text)
        self.logger.debug(f"Keyword score calculated: {keyword_score}")

        formatting_score = self._analyze_formatting(resume_text)
        self.logger.debug(f"Formatting score calculated: {formatting_score}")

        section_score = self._analyze_section_completeness(resume_text)
        self.logger.debug(f"Section score calculated: {section_score}")

        # Calculate weighted score
        total_score = (
            keyword_score * ATS_KEYWORD_WEIGHT +
            formatting_score * ATS_FORMATTING_WEIGHT +
            section_score * ATS_SECTION_WEIGHT
        )

        # Ensure score is within 0-100 range
        final_score = max(0.0, min(100.0, total_score))
        self.logger.info(f"ATS score calculation completed: {final_score}")

        return final_score

    def _analyze_keywords(self, resume_text: str, keywords: List[str] = None) -> float:
        """
        Analyze how many relevant keywords are present in the resume.

        Args:
            resume_text: The text content of the resume
            keywords: List of keywords to search for (uses default if None)

        Returns:
            Keyword score (0-100)
        """
        if keywords is None:
            keywords = self.tech_keywords

        if not resume_text:
            return 0.0

        # Convert to lowercase for case-insensitive matching
        text_lower = resume_text.lower()
        found_count = 0

        for keyword in keywords:
            # Use word boundaries to avoid partial matches
            if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text_lower):
                found_count += 1

        # Calculate percentage of keywords found
        if len(keywords) == 0:
            return 0.0

        percentage = (found_count / len(keywords)) * 100
        return min(100.0, percentage)

    def _analyze_formatting(self, resume_text: str) -> float:
        """
        Analyze the formatting quality of the resume.

        Args:
            resume_text: The text content of the resume

        Returns:
            Formatting score (0-100)
        """
        if not resume_text:
            return 0.0

        # Check for formatting indicators
        lines = resume_text.split('\n')

        # Count lines that look like section headers (all caps or followed by separator)
        section_headers = 0
        for line in lines:
            line = line.strip()
            if line.isupper() and len(line) > 2 and len(line) < 50:
                section_headers += 1
            elif re.match(r'^[A-Z][A-Z\s]+$', line):  # Lines that are mostly uppercase
                section_headers += 1

        # Count bullet points (indicating organized content)
        bullet_points = len(re.findall(r'[-•·]\s', resume_text))

        # Count lines with dates (indicating structured experience)
        date_patterns = [
            r'\b\d{4}\s*[-–—]\s*\d{4}\b',  # YYYY - YYYY
            r'\b\d{4}\s*[-–—]\s*(present|current)\b',  # YYYY - Present
            r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}\b',  # Month YYYY
        ]
        date_count = 0
        for pattern in date_patterns:
            date_count += len(re.findall(pattern, resume_text, re.IGNORECASE))

        # Calculate formatting score based on these indicators
        # Weights: section headers (30%), bullet points (40%), dates (30%)
        header_score = min(100.0, section_headers * 15)  # Up to 3 headers = 45 points
        bullet_score = min(100.0, bullet_points * 5)    # Up to 15 bullets = 75 points
        date_score = min(100.0, date_count * 10)        # Up to 8 dates = 80 points

        # Weighted average
        formatting_score = (header_score * 0.3) + (bullet_score * 0.4) + (date_score * 0.3)
        return min(100.0, formatting_score)

    def _analyze_section_completeness(self, resume_text: str) -> float:
        """
        Analyze how many important sections are present in the resume.

        Args:
            resume_text: The text content of the resume

        Returns:
            Section completeness score (0-100)
        """
        if not resume_text:
            return 0.0

        text_lower = resume_text.lower()
        found_sections = 0

        for section in self.resume_sections:
            if section.lower() in text_lower:
                found_sections += 1

        # Calculate percentage of sections found
        percentage = (found_sections / len(self.resume_sections)) * 100
        return min(100.0, percentage)

    def get_improvement_suggestions(self, resume_text: str) -> List[str]:
        """
        Generate improvement suggestions based on ATS analysis.

        Args:
            resume_text: The text content of the resume

        Returns:
            List of improvement suggestions
        """
        suggestions = []

        # Check for missing keywords
        missing_keywords = []
        for keyword in self.tech_keywords[:10]:  # Check first 10 common keywords
            if not re.search(r'\b' + re.escape(keyword.lower()) + r'\b', resume_text.lower()):
                missing_keywords.append(keyword)

        if len(missing_keywords) > 5:  # If more than 5 common keywords are missing
            suggestions.append(f"Consider adding relevant keywords like: {', '.join(missing_keywords[:5])}")

        # Check for formatting issues
        if not re.search(r'[-•·]\s', resume_text):  # No bullet points found
            suggestions.append("Use bullet points to organize your experience and skills")

        # Check for missing sections
        text_lower = resume_text.lower()
        missing_sections = []
        for section in ["skills", "experience", "education"]:
            if section not in text_lower:
                missing_sections.append(section.title())

        if missing_sections:
            suggestions.append(f"Consider adding missing sections: {', '.join(missing_sections)}")

        if not suggestions:
            suggestions.append("Your resume looks good for ATS systems!")

        return suggestions

    def get_standard_keywords(self) -> List[str]:
        """
        Get the list of standard keywords used for ATS analysis.

        Returns:
            List of standard keywords
        """
        return self.tech_keywords.copy()