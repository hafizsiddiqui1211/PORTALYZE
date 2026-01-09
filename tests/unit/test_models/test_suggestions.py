"""Tests for the KeywordSuggestion model"""
import pytest
from datetime import datetime
from src.models.suggestions import KeywordSuggestion


class TestKeywordSuggestion:
    """Test cases for KeywordSuggestion entity"""

    def test_keyword_suggestion_creation_success(self):
        """Test successful creation of a KeywordSuggestion entity"""
        suggestion = KeywordSuggestion(
            suggestion_id="test-suggestion-id",
            analysis_id="test-analysis-id",
            keyword="Python",
            relevance_score=0.9,
            category="Technical",
            justification="Important for the target role",
            role_alignment="Software Engineer",
            created_timestamp=datetime.now()
        )

        assert suggestion.suggestion_id == "test-suggestion-id"
        assert suggestion.analysis_id == "test-analysis-id"
        assert suggestion.keyword == "Python"
        assert suggestion.relevance_score == 0.9
        assert suggestion.category == "Technical"
        assert suggestion.justification == "Important for the target role"
        assert suggestion.role_alignment == "Software Engineer"

    def test_keyword_suggestion_creation_with_invalid_relevance_score_high(self):
        """Test KeywordSuggestion creation fails with relevance score > 1"""
        with pytest.raises(ValueError, match="relevance_score must be between 0 and 1"):
            KeywordSuggestion(
                suggestion_id="test-suggestion-id",
                analysis_id="test-analysis-id",
                keyword="Python",
                relevance_score=1.5,  # Invalid: > 1
                category="Technical",
                justification="Important for the target role",
                role_alignment="Software Engineer",
                created_timestamp=datetime.now()
            )

    def test_keyword_suggestion_creation_with_invalid_relevance_score_low(self):
        """Test KeywordSuggestion creation fails with relevance score < 0"""
        with pytest.raises(ValueError, match="relevance_score must be between 0 and 1"):
            KeywordSuggestion(
                suggestion_id="test-suggestion-id",
                analysis_id="test-analysis-id",
                keyword="Python",
                relevance_score=-0.1,  # Invalid: < 0
                category="Technical",
                justification="Important for the target role",
                role_alignment="Software Engineer",
                created_timestamp=datetime.now()
            )

    def test_keyword_suggestion_creation_with_empty_keyword(self):
        """Test KeywordSuggestion creation fails with empty keyword"""
        with pytest.raises(ValueError, match="keyword must be non-empty"):
            KeywordSuggestion(
                suggestion_id="test-suggestion-id",
                analysis_id="test-analysis-id",
                keyword="",  # Invalid: empty
                relevance_score=0.9,
                category="Technical",
                justification="Important for the target role",
                role_alignment="Software Engineer",
                created_timestamp=datetime.now()
            )

    def test_keyword_suggestion_creation_with_whitespace_keyword(self):
        """Test KeywordSuggestion creation fails with whitespace-only keyword"""
        with pytest.raises(ValueError, match="keyword must be non-empty"):
            KeywordSuggestion(
                suggestion_id="test-suggestion-id",
                analysis_id="test-analysis-id",
                keyword="   ",  # Invalid: whitespace only
                relevance_score=0.9,
                category="Technical",
                justification="Important for the target role",
                role_alignment="Software Engineer",
                created_timestamp=datetime.now()
            )

    def test_keyword_suggestion_creation_with_invalid_category(self):
        """Test KeywordSuggestion creation fails with invalid category"""
        with pytest.raises(ValueError, match="category must be one of"):
            KeywordSuggestion(
                suggestion_id="test-suggestion-id",
                analysis_id="test-analysis-id",
                keyword="Python",
                relevance_score=0.9,
                category="InvalidCategory",  # Invalid category
                justification="Important for the target role",
                role_alignment="Software Engineer",
                created_timestamp=datetime.now()
            )

    def test_keyword_suggestion_creation_with_empty_justification(self):
        """Test KeywordSuggestion creation fails with empty justification"""
        with pytest.raises(ValueError, match="justification must be non-empty"):
            KeywordSuggestion(
                suggestion_id="test-suggestion-id",
                analysis_id="test-analysis-id",
                keyword="Python",
                relevance_score=0.9,
                category="Technical",
                justification="",  # Invalid: empty
                role_alignment="Software Engineer",
                created_timestamp=datetime.now()
            )

    def test_keyword_suggestion_creation_with_whitespace_justification(self):
        """Test KeywordSuggestion creation fails with whitespace-only justification"""
        with pytest.raises(ValueError, match="justification must be non-empty"):
            KeywordSuggestion(
                suggestion_id="test-suggestion-id",
                analysis_id="test-analysis-id",
                keyword="Python",
                relevance_score=0.9,
                category="Technical",
                justification="   ",  # Invalid: whitespace only
                role_alignment="Software Engineer",
                created_timestamp=datetime.now()
            )

    def test_keyword_suggestion_create_new_method(self):
        """Test the create_new class method"""
        suggestion = KeywordSuggestion.create_new(
            analysis_id="test-analysis-id",
            keyword="JavaScript",
            relevance_score=0.85,
            category="Technical",
            justification="Essential for web development roles",
            role_alignment="Frontend Developer"
        )

        # Should have generated a valid UUID
        assert suggestion.suggestion_id is not None
        assert suggestion.suggestion_id != ""
        assert suggestion.analysis_id == "test-analysis-id"
        assert suggestion.keyword == "JavaScript"
        assert suggestion.relevance_score == 0.85
        assert suggestion.category == "Technical"
        assert suggestion.justification == "Essential for web development roles"
        assert suggestion.role_alignment == "Frontend Developer"
        assert suggestion.created_timestamp is not None

    def test_keyword_suggestion_valid_categories(self):
        """Test that all valid categories work correctly"""
        valid_categories = ["Technical", "SoftSkill", "IndustrySpecific"]

        for category in valid_categories:
            suggestion = KeywordSuggestion.create_new(
                analysis_id="test-analysis-id",
                keyword="TestKeyword",
                relevance_score=0.7,
                category=category,
                justification="Test justification",
                role_alignment="Test Role"
            )
            assert suggestion.category == category

    def test_keyword_suggestion_case_sensitive_category_validation(self):
        """Test that category validation is case sensitive"""
        with pytest.raises(ValueError, match="category must be one of"):
            KeywordSuggestion.create_new(
                analysis_id="test-analysis-id",
                keyword="Python",
                relevance_score=0.9,
                category="technical",  # Invalid: lowercase
                justification="Important for the target role",
                role_alignment="Software Engineer"
            )

    def test_keyword_suggestion_creation_without_timestamp(self):
        """Test that KeywordSuggestion can be created without a timestamp"""
        suggestion = KeywordSuggestion(
            suggestion_id="test-suggestion-id",
            analysis_id="test-analysis-id",
            keyword="Python",
            relevance_score=0.9,
            category="Technical",
            justification="Important for the target role",
            role_alignment="Software Engineer"
            # created_timestamp is None
        )

        assert suggestion.suggestion_id == "test-suggestion-id"
        assert suggestion.created_timestamp is None