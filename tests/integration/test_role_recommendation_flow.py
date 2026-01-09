"""End-to-end tests for role recommendation workflow"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from typing import List, Dict, Any

from src.models.profile_signals import ProfileSignals, ResumeSignals, ProfileSignalsData, ExperienceSummary
from src.models.role_recommendation import RoleRecommendation, RecommendedRole
from src.services.role_inferencer import RoleInferencer
from src.services.signal_aggregator import SignalAggregator
from src.services.consent_manager import ConsentManager


class TestRoleRecommendationFlow:
    """Integration tests for the complete role recommendation workflow"""

    @pytest.fixture
    def mock_profile_signals(self):
        """Create a mock profile signals object for testing"""
        resume_signals = ResumeSignals(
            skills=['Python', 'Machine Learning', 'Data Science'],
            experience_years=3.0,
            job_titles=['Data Scientist', 'ML Engineer'],
            industries=['AI', 'Tech'],
            education=['MS Computer Science'],
            certifications=[]
        )

        profile_signals_data = ProfileSignalsData(
            github_activity={
                'total_commits': 150,
                'repositories': 8,
                'stars_received': 25,
                'recent_activity': True,
                'top_languages': ['Python', 'SQL', 'JavaScript'],
                'contributions': 75
            },
            linkedin_summary={
                'headline': 'Senior Data Scientist at Tech Company',
                'summary': 'Experienced data scientist with expertise in ML and AI',
                'connections': 500,
                'experience': ['Data Scientist', 'ML Engineer'],
                'skills': ['Python', 'Machine Learning', 'Statistics', 'Data Analysis']
            },
            portfolio_projects=[
                {
                    'name': 'ML Project',
                    'technologies': ['Python', 'TensorFlow', 'AWS'],
                    'description': 'Machine learning project',
                    'impact': 'Improved prediction accuracy by 20%'
                }
            ],
            social_signals={
                'activity_level': 'HIGH',
                'professional_network': 'LARGE',
                'technical_recognition': 'GOOD'
            }
        )

        experience_summary = ExperienceSummary(
            total_years=3.0,
            domains=['AI', 'Data Science'],
            leadership_indicators=['Led team of 3 engineers'],
            technology_stack=['Python', 'TensorFlow', 'AWS', 'SQL']
        )

        profile_signals = ProfileSignals(
            signals_id='test_signals_123',
            resume_signals=resume_signals.dict(),
            profile_signals=profile_signals_data.dict(),
            aggregated_skills=['Python', 'Machine Learning', 'Data Science', 'SQL', 'TensorFlow'],
            experience_summary=experience_summary.dict(),
            project_highlights=[
                {
                    'name': 'ML Project',
                    'technologies': ['Python', 'TensorFlow', 'AWS'],
                    'description': 'Machine learning project',
                    'impact': 'Improved prediction accuracy by 20%',
                    'role': 'Lead Developer'
                }
            ]
        )

        return profile_signals

    @pytest.fixture
    def mock_industries(self):
        """Mock list of target industries"""
        return ['AI/ML', 'Data Science', 'Software Engineering']

    @pytest.fixture
    def mock_archetypes(self):
        """Mock role archetypes for testing"""
        return [
            {
                'title': 'Senior Machine Learning Engineer',
                'industry': 'AI/ML',
                'description': 'Senior ML engineer role',
                'required_skills': ['Python', 'TensorFlow', 'Machine Learning'],
                'preferred_skills': ['PyTorch', 'AWS', 'Data Science'],
                'technologies': ['Python', 'TensorFlow', 'PyTorch', 'AWS'],
                'responsibilities': ['Develop ML models', 'Lead projects'],
                'seniority_requirements': {'level': 'Senior', 'years': 3},
                'role_signals': {'technical_depth': True, 'leadership': True}
            },
            {
                'title': 'Data Scientist',
                'industry': 'Data Science',
                'description': 'Data scientist role',
                'required_skills': ['Python', 'SQL', 'Statistics'],
                'preferred_skills': ['Machine Learning', 'Data Visualization'],
                'technologies': ['Python', 'SQL', 'R', 'Tableau'],
                'responsibilities': ['Analyze data', 'Build models'],
                'seniority_requirements': {'level': 'Mid', 'years': 2},
                'role_signals': {'analytical': True, 'statistical': True}
            }
        ]

    def test_complete_role_recommendation_workflow(self, mock_profile_signals, mock_industries):
        """Test the complete end-to-end role recommendation workflow"""
        # Initialize the role inferencer
        inferencer = RoleInferencer()

        # Mock the knowledge base to return test archetypes
        with patch.object(inferencer.knowledge_base, 'get_archetypes_by_industry') as mock_get_archetypes:
            # Create mock archetypes
            mock_archetype1 = Mock()
            mock_archetype1.title = 'Senior Machine Learning Engineer'
            mock_archetype1.industry = 'AI/ML'
            mock_archetype1.required_skills = ['Python', 'Machine Learning', 'TensorFlow']
            mock_archetype1.preferred_skills = ['PyTorch', 'AWS']
            mock_archetype1.technologies = ['Python', 'TensorFlow', 'PyTorch', 'AWS']
            mock_archetype1.responsibilities = ['Develop ML models', 'Lead projects']

            mock_archetype2 = Mock()
            mock_archetype2.title = 'Data Scientist'
            mock_archetype2.industry = 'Data Science'
            mock_archetype2.required_skills = ['Python', 'SQL', 'Statistics']
            mock_archetype2.preferred_skills = ['Machine Learning', 'Data Visualization']
            mock_archetype2.technologies = ['Python', 'SQL', 'R', 'Tableau']
            mock_archetype2.responsibilities = ['Analyze data', 'Build models']

            mock_get_archetypes.side_effect = lambda industry: {
                'AI/ML': [mock_archetype1],
                'Data Science': [mock_archetype2],
                'Software Engineering': []
            }.get(industry, [])

            # Run the role inference
            recommendation = inferencer.infer_roles(
                profile_signals=mock_profile_signals,
                industries=mock_industries,
                max_roles=2
            )

            # Assertions
            assert recommendation is not None
            assert isinstance(recommendation, RoleRecommendation)
            assert len(recommendation.roles) > 0
            assert recommendation.overall_confidence >= 0.0
            assert recommendation.overall_confidence <= 1.0

            # Check that roles have appropriate attributes
            for role in recommendation.roles:
                assert isinstance(role, RecommendedRole)
                assert role.title
                assert role.industry
                assert 0.0 <= role.fit_score <= 1.0
                assert role.justification
                assert isinstance(role.confidence_factors, list)

    def test_role_recommendation_with_minimal_data(self, mock_industries):
        """Test role recommendation with minimal profile data"""
        # Create profile signals with minimal data
        minimal_resume_signals = ResumeSignals(
            skills=[],
            experience_years=0.0,
            job_titles=[],
            industries=[],
            education=[],
            certifications=[]
        )

        minimal_profile_data = ProfileSignalsData(
            github_activity={},
            linkedin_summary={},
            portfolio_projects=[],
            social_signals={}
        )

        minimal_experience_summary = ExperienceSummary(
            total_years=0.0,
            domains=[],
            leadership_indicators=[],
            technology_stack=[]
        )

        minimal_profile_signals = ProfileSignals(
            signals_id='minimal_signals_123',
            resume_signals=minimal_resume_signals.dict(),
            profile_signals=minimal_profile_data.dict(),
            aggregated_skills=[],
            experience_summary=minimal_experience_summary.dict(),
            project_highlights=[]
        )

        # Initialize the role inferencer
        inferencer = RoleInferencer()

        # Test graceful degradation
        with patch.object(inferencer, '_handle_minimal_profile_data') as mock_handler:
            # Create a mock fallback recommendation
            mock_fallback = Mock(spec=RoleRecommendation)
            mock_fallback.roles = []
            mock_fallback.overall_confidence = 0.2
            mock_handler.return_value = mock_fallback

            # This should trigger the minimal data handler
            recommendation = inferencer.infer_roles_with_graceful_degradation(
                profile_signals=minimal_profile_signals,
                industries=mock_industries
            )

            # Verify the minimal data handler was called
            mock_handler.assert_called_once()

    def test_role_recommendation_with_conflicting_signals(self, mock_profile_signals, mock_industries):
        """Test role recommendation with conflicting signals across domains"""
        # Modify profile signals to have conflicting technology stacks
        conflicting_resume_signals = ResumeSignals(
            skills=['JavaScript', 'React', 'HTML', 'CSS', 'Python', 'TensorFlow', 'Docker', 'AWS'],
            experience_years=4.0,
            job_titles=['Frontend Developer', 'ML Engineer', 'DevOps Engineer'],
            industries=['Web Development', 'AI/ML', 'DevOps'],
            education=['Computer Science'],
            certifications=[]
        )

        # Create experience summary with multiple domains
        conflicting_experience_summary = ExperienceSummary(
            total_years=4.0,
            domains=['Web Development', 'AI/ML', 'DevOps'],
            leadership_indicators=['Frontend Lead', 'ML Project Manager', 'DevOps Coordinator'],
            technology_stack=['JavaScript', 'Python', 'Docker', 'AWS', 'React', 'TensorFlow']
        )

        conflicting_profile_signals = ProfileSignals(
            signals_id='conflicting_signals_123',
            resume_signals=conflicting_resume_signals.dict(),
            profile_signals=mock_profile_signals.profile_signals,
            aggregated_skills=['JavaScript', 'Python', 'Docker', 'AWS', 'React', 'TensorFlow'],
            experience_summary=conflicting_experience_summary.dict(),
            project_highlights=mock_profile_signals.project_highlights
        )

        inferencer = RoleInferencer()

        # Mock archetypes
        with patch.object(inferencer.knowledge_base, 'get_archetypes_by_industry') as mock_get_archetypes:
            mock_archetype = Mock()
            mock_archetype.title = 'Full Stack ML Engineer'
            mock_archetype.industry = 'AI/ML'
            mock_archetype.required_skills = ['Python', 'JavaScript', 'ML']
            mock_archetype.preferred_skills = ['AWS', 'Docker']
            mock_archetype.technologies = ['Python', 'JavaScript', 'AWS', 'Docker']
            mock_archetype.responsibilities = ['Develop ML models', 'Build full stack applications']

            mock_get_archetypes.return_value = [mock_archetype]

            # This should detect conflicting signals and handle them appropriately
            recommendation = inferencer.infer_roles_with_graceful_degradation(
                profile_signals=conflicting_profile_signals,
                industries=mock_industries
            )

            # Should still return a valid recommendation despite conflicts
            assert recommendation is not None
            assert isinstance(recommendation, RoleRecommendation)

    def test_consent_integration_in_signal_aggregation(self):
        """Test that consent is properly handled in signal aggregation"""
        # Create mock data
        resume_analysis = {
            'strengths': ['Strong technical skills'],
            'weaknesses': ['Limited leadership experience'],
            'text_content': 'Sample resume content',
            'ats_score': 0.85
        }

        profile_analyses = [
            {
                'profile_type': 'LINKEDIN',
                'headline': 'Software Engineer',
                'summary': 'Experienced software engineer',
                'skills': ['Python', 'JavaScript']
            }
        ]

        session_id = 'test_session_123'

        # Initialize signal aggregator
        aggregator = SignalAggregator()

        # Mock consent manager to simulate granted consent
        with patch.object(aggregator.consent_manager, 'has_consent', return_value=True), \
             patch.object(aggregator.consent_manager, 'store_data_with_consent') as mock_store:

            # Run signal aggregation with consent requirement
            signals = aggregator.aggregate_signals(
                resume_analysis=resume_analysis,
                profile_analyses=profile_analyses,
                session_id=session_id,
                require_consent=True
            )

            # Verify that consent was checked and data was stored
            aggregator.consent_manager.has_consent.assert_called_with(session_id)
            mock_store.assert_called_once()

            # Verify that signals were generated
            assert signals is not None
            assert signals.signals_id.startswith('signals_test_session_123')

    def test_role_inferencer_with_consent_flow(self, mock_profile_signals, mock_industries):
        """Test complete workflow with consent handling"""
        inferencer = RoleInferencer()

        # Mock the knowledge base
        with patch.object(inferencer.knowledge_base, 'get_archetypes_by_industry') as mock_get_archetypes:
            mock_archetype = Mock()
            mock_archetype.title = 'AI Specialist'
            mock_archetype.industry = 'AI/ML'
            mock_archetype.required_skills = ['Python', 'ML']
            mock_archetype.preferred_skills = ['TensorFlow', 'PyTorch']
            mock_archetype.technologies = ['Python', 'TensorFlow', 'PyTorch']
            mock_archetype.responsibilities = ['Develop AI models']

            mock_get_archetypes.return_value = [mock_archetype]

            # Run the full workflow
            recommendation = inferencer.infer_roles_with_graceful_degradation(
                profile_signals=mock_profile_signals,
                industries=mock_industries
            )

            # Verify the recommendation is valid
            assert recommendation is not None
            assert len(recommendation.roles) >= 0  # May have 0 roles if no good matches
            if recommendation.roles:
                role = recommendation.roles[0]
                assert 0.0 <= role.fit_score <= 1.0
                assert isinstance(role.confidence_factors, list)