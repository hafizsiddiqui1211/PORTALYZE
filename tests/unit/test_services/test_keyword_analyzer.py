"""Tests for the keyword analyzer service"""
import pytest
from unittest.mock import Mock, patch
from src.services.keyword_analyzer import KeywordAnalyzer


class TestKeywordAnalyzer:
    """Test cases for KeywordAnalyzer service"""

    def test_get_relevant_keywords_for_software_engineer(self):
        """Test keyword extraction for software engineering roles"""
        analyzer = KeywordAnalyzer()

        resume_text = """
        Software Engineer with 3 years of experience in Python, JavaScript, and React.
        Experience with AWS, Docker, and CI/CD pipelines.
        Bachelor's degree in Computer Science.
        """

        keywords = analyzer.get_relevant_keywords(resume_text, "Software Engineer")
        assert len(keywords) > 0
        # Should include some technical keywords from the text
        assert any("Python" in kw or "JavaScript" in kw or "React" in kw for kw in keywords)

    def test_get_relevant_keywords_for_data_science(self):
        """Test keyword extraction for data science roles"""
        analyzer = KeywordAnalyzer()

        resume_text = """
        Data Scientist with experience in Python, R, and machine learning.
        Worked with pandas, scikit-learn, and TensorFlow.
        PhD in Statistics.
        """

        keywords = analyzer.get_relevant_keywords(resume_text, "Data Scientist")
        assert len(keywords) > 0
        # Should include data science related keywords
        assert any("Python" in kw or "R" in kw or "machine learning" in kw for kw in keywords)

    def test_identify_keyword_gaps_existing_keywords(self):
        """Test identification of keyword gaps when some keywords exist"""
        analyzer = KeywordAnalyzer()

        resume_text = "Experienced in Python and JavaScript"
        required_keywords = ["Python", "JavaScript", "React", "Node.js", "AWS"]

        gaps = analyzer.identify_keyword_gaps(resume_text, required_keywords)
        # Should identify React, Node.js, and AWS as gaps
        assert "React" in gaps
        assert "Node.js" in gaps
        assert "AWS" in gaps
        # Should not include Python and JavaScript as gaps
        assert "Python" not in gaps
        assert "JavaScript" not in gaps

    def test_identify_keyword_gaps_no_gaps(self):
        """Test identification of keyword gaps when no gaps exist"""
        analyzer = KeywordAnalyzer()

        resume_text = "Experienced in Python, JavaScript, React, Node.js, AWS"
        required_keywords = ["Python", "JavaScript", "React"]

        gaps = analyzer.identify_keyword_gaps(resume_text, required_keywords)
        # Should have no gaps since all required keywords are present
        assert len(gaps) == 0

    def test_identify_keyword_gaps_all_gaps(self):
        """Test identification of keyword gaps when all keywords are missing"""
        analyzer = KeywordAnalyzer()

        resume_text = "Experienced in cooking and gardening"
        required_keywords = ["Python", "JavaScript", "React"]

        gaps = analyzer.identify_keyword_gaps(resume_text, required_keywords)
        # Should identify all required keywords as gaps
        assert "Python" in gaps
        assert "JavaScript" in gaps
        assert "React" in gaps

    def test_calculate_keyword_relevance(self):
        """Test calculation of keyword relevance scores"""
        analyzer = KeywordAnalyzer()

        resume_text = "Software Engineer with 3 years of experience in Python and JavaScript"
        keywords = ["Python", "JavaScript", "React", "AWS"]

        relevance_scores = analyzer.calculate_keyword_relevance(resume_text, keywords)
        assert len(relevance_scores) == len(keywords)

        # Python and JavaScript should have higher relevance scores
        python_score = next(score for kw, score in relevance_scores if kw == "Python")
        javascript_score = next(score for kw, score in relevance_scores if kw == "JavaScript")
        react_score = next(score for kw, score in relevance_scores if kw == "React")
        aws_score = next(score for kw, score in relevance_scores if kw == "AWS")

        # Python and JavaScript appear in the text, so they should have higher scores
        assert python_score > react_score
        assert javascript_score > aws_score

    def test_get_role_specific_keywords_software_engineering(self):
        """Test retrieval of role-specific keywords for software engineering"""
        analyzer = KeywordAnalyzer()

        keywords = analyzer.get_role_specific_keywords("Software Engineer")
        assert len(keywords) > 0
        # Should include software engineering related keywords
        assert any("Python" in kw or "JavaScript" in kw or "React" in kw for kw in keywords)

    def test_get_role_specific_keywords_data_science(self):
        """Test retrieval of role-specific keywords for data science"""
        analyzer = KeywordAnalyzer()

        keywords = analyzer.get_role_specific_keywords("Data Scientist")
        assert len(keywords) > 0
        # Should include data science related keywords
        assert any("Python" in kw or "R" in kw or "machine learning" in kw for kw in keywords)

    def test_generate_keyword_suggestions(self):
        """Test generation of keyword suggestions"""
        analyzer = KeywordAnalyzer()

        resume_text = "Software Engineer with experience in Python"
        suggestions = analyzer.generate_keyword_suggestions(resume_text, "Software Engineer")

        assert len(suggestions) > 0
        for suggestion in suggestions:
            assert hasattr(suggestion, 'keyword')
            assert hasattr(suggestion, 'relevance_score')
            assert hasattr(suggestion, 'category')
            assert hasattr(suggestion, 'justification')
            assert 0 <= suggestion.relevance_score <= 1

    def test_get_keyword_categories(self):
        """Test that keywords are properly categorized"""
        analyzer = KeywordAnalyzer()

        resume_text = "Software Engineer with experience in Python and leadership"
        suggestions = analyzer.generate_keyword_suggestions(resume_text, "Software Engineer")

        # Check that suggestions have appropriate categories
        technical_categories = ["Technical", "Programming Language", "Framework", "Tool", "Platform"]
        soft_categories = ["Soft Skill", "Communication", "Leadership"]

        has_technical = any(s.category in technical_categories for s in suggestions)
        has_soft = any(s.category in soft_categories for s in suggestions)

        # Should have at least some technical keywords
        assert has_technical

    def test_keyword_extraction_with_punctuation(self):
        """Test that keyword extraction works with punctuation"""
        analyzer = KeywordAnalyzer()

        resume_text = "Experienced in Python, JavaScript; and React: development"
        keywords = analyzer.get_relevant_keywords(resume_text, "Software Engineer")

        # Should extract keywords despite punctuation
        assert any("Python" in kw for kw in keywords)
        assert any("JavaScript" in kw for kw in keywords)
        assert any("React" in kw for kw in keywords)

    def test_empty_resume_text_handling(self):
        """Test handling of empty resume text"""
        analyzer = KeywordAnalyzer()

        # Should handle empty text gracefully
        keywords = analyzer.get_relevant_keywords("", "Software Engineer")
        assert len(keywords) == 0

        gaps = analyzer.identify_keyword_gaps("", ["Python", "JavaScript"])
        assert len(gaps) == 2  # Both keywords should be considered gaps