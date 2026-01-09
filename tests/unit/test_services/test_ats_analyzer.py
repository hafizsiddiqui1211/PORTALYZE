"""Tests for the ATS analyzer service"""
import pytest
from unittest.mock import Mock, patch
from src.services.ats_analyzer import ATSAnalyzer


class TestATSAnalyzer:
    """Test cases for ATSAnalyzer service"""

    def test_calculate_ats_score(self):
        """Test ATS score calculation with sample resume content"""
        analyzer = ATSAnalyzer()

        # Sample resume content with good keywords
        resume_text = """
        Software Engineer with 5 years of experience in Python, JavaScript, and React.
        Experience with AWS, Docker, and CI/CD pipelines.
        Bachelor's degree in Computer Science.
        Led a team of 5 developers to deliver project on time.
        """

        # Mock the keyword analysis
        with patch.object(analyzer, '_analyze_keywords', return_value=80.0), \
             patch.object(analyzer, '_analyze_formatting', return_value=75.0), \
             patch.object(analyzer, '_analyze_section_completeness', return_value=85.0):

            score = analyzer.calculate_ats_score(resume_text)
            # Score should be weighted combination: 0.4*80 + 0.3*75 + 0.3*85 = 32 + 22.5 + 25.5 = 80
            assert score == pytest.approx(80.0, abs=0.1)

    def test_analyze_keywords_with_good_content(self):
        """Test keyword analysis with good resume content"""
        analyzer = ATSAnalyzer()

        # Set up some common tech keywords for testing
        resume_text = "Python JavaScript React AWS Docker"
        keywords = ["Python", "JavaScript", "React", "AWS", "Docker"]

        score = analyzer._analyze_keywords(resume_text, keywords)
        assert score == 100.0  # All keywords present

    def test_analyze_keywords_with_partial_content(self):
        """Test keyword analysis with partial resume content"""
        analyzer = ATSAnalyzer()

        # Set up some common tech keywords for testing
        resume_text = "Python JavaScript"
        keywords = ["Python", "JavaScript", "React", "AWS", "Docker"]

        score = analyzer._analyze_keywords(resume_text, keywords)
        assert score == 40.0  # 2 out of 5 keywords present

    def test_analyze_keywords_with_no_content(self):
        """Test keyword analysis with no matching keywords"""
        analyzer = ATSAnalyzer()

        resume_text = "Cooking gardening"
        keywords = ["Python", "JavaScript", "React", "AWS", "Docker"]

        score = analyzer._analyze_keywords(resume_text, keywords)
        assert score == 0.0

    def test_analyze_formatting_good_formatting(self):
        """Test formatting analysis with well-formatted content"""
        resume_text = """
        EXPERIENCE
        Software Engineer | Company | 2020-Present
        - Developed applications
        - Led team projects

        SKILLS
        - Python
        - JavaScript
        - React
        """
        score = ATSAnalyzer()._analyze_formatting(resume_text)
        # Should have good formatting with clear sections and bullet points
        assert score >= 70.0

    def test_analyze_formatting_poor_formatting(self):
        """Test formatting analysis with poorly formatted content"""
        resume_text = "Software Engineer Company 2020-Present Developed applications Led team projects Python JavaScript React"
        score = ATSAnalyzer()._analyze_formatting(resume_text)
        # Should have poor formatting without clear sections or bullet points
        assert score <= 30.0

    def test_analyze_section_completeness_complete_resume(self):
        """Test section completeness with complete resume"""
        resume_text = """
        EXPERIENCE
        Software Engineer | Company | 2020-Present
        EDUCATION
        Bachelor's Degree | University | 2016-2020
        SKILLS
        Python, JavaScript, React
        CONTACT
        email@example.com
        """
        score = ATSAnalyzer()._analyze_section_completeness(resume_text)
        # Should have all important sections
        assert score >= 80.0

    def test_analyze_section_completeness_incomplete_resume(self):
        """Test section completeness with incomplete resume"""
        resume_text = """
        EXPERIENCE
        Software Engineer | Company | 2020-Present
        """
        score = ATSAnalyzer()._analyze_section_completeness(resume_text)
        # Missing important sections like education, skills, contact
        assert score <= 40.0

    def test_get_standard_keywords(self):
        """Test retrieval of standard keywords"""
        analyzer = ATSAnalyzer()
        keywords = analyzer.get_standard_keywords()

        # Should have a reasonable number of keywords
        assert len(keywords) > 0
        assert "Python" in keywords or "JavaScript" in keywords or "React" in keywords