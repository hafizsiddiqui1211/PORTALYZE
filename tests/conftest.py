"""Pytest configuration and fixtures for Resume Analyzer Core"""
import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, MagicMock


@pytest.fixture
def sample_pdf_content():
    """Sample PDF content for testing"""
    # This is a minimal valid PDF header
    return b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000053 00000 n \n0000000133 00000 n \ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n177\n%%EOF'


@pytest.fixture
def sample_docx_content():
    """Sample DOCX content for testing (minimal valid DOCX structure)"""
    import zipfile
    import io

    # Create a minimal DOCX in memory
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add minimal DOCX structure
        zip_file.writestr('[Content_Types].xml', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>''')
        zip_file.writestr('_rels/.rels', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>''')
        zip_file.writestr('word/_rels/document.xml.rels', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>''')
        zip_file.writestr('word/document.xml', '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>
<w:p>
<w:r>
<w:t>Test content</w:t>
</w:r>
</w:p>
</w:body>
</w:document>''')

    return buffer.getvalue()


@pytest.fixture
def temp_file():
    """Create a temporary file for testing"""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        yield tmp.name
        # Clean up after test
        os.unlink(tmp.name)


@pytest.fixture
def mock_resume_data():
    """Mock resume data for testing"""
    return {
        'resume_id': 'test-resume-id',
        'original_filename': 'test_resume.pdf',
        'file_type': 'PDF',
        'file_path': '/tmp/test_resume.pdf',
        'text_content': 'John Doe Software Engineer',
        'metadata': {'author': 'John Doe', 'title': 'Resume'},
        'upload_timestamp': '2023-01-01T00:00:00',
        'session_id': 'test-session-id'
    }


@pytest.fixture
def mock_analysis_result():
    """Mock analysis result data for testing"""
    return {
        'analysis_id': 'test-analysis-id',
        'resume_id': 'test-resume-id',
        'ats_score': 85.5,
        'strengths': ['Strong technical skills', 'Good experience'],
        'weaknesses': ['Missing keywords', 'Poor formatting'],
        'section_feedback': {
            'experience': 'Good experience section',
            'skills': 'Technical skills well presented',
            'education': 'Education properly formatted'
        },
        'overall_feedback': 'Overall good resume with some areas for improvement',
        'confidence_level': 0.9
    }


@pytest.fixture
def mock_keyword_suggestion():
    """Mock keyword suggestion data for testing"""
    return {
        'suggestion_id': 'test-suggestion-id',
        'analysis_id': 'test-analysis-id',
        'keyword': 'Python',
        'relevance_score': 0.9,
        'category': 'Technical',
        'justification': 'Python is a key skill for the target role',
        'role_alignment': 'Software Engineer'
    }


# Phase 2: Portfolio + LinkedIn / GitHub Integration fixtures

@pytest.fixture
def mock_profile_urls():
    """Mock profile URLs for testing"""
    return {
        'linkedin_url': 'https://www.linkedin.com/in/johndoe',
        'github_url': 'https://github.com/johndoe',
        'portfolio_url': 'https://johndoe.com'
    }


@pytest.fixture
def mock_http_responses():
    """Mock HTTP responses for testing"""
    from unittest.mock import Mock

    # Mock successful response
    success_response = Mock()
    success_response.status_code = 200
    success_response.text = '<html><body><h1>Test Content</h1></body></html>'
    success_response.content = b'<html><body><h1>Test Content</h1></body></html>'

    # Mock failed response
    failed_response = Mock()
    failed_response.status_code = 404
    failed_response.text = 'Not Found'

    # Mock rate limited response
    rate_limited_response = Mock()
    rate_limited_response.status_code = 429
    rate_limited_response.text = 'Rate Limited'

    return {
        'success': success_response,
        'failed': failed_response,
        'rate_limited': rate_limited_response
    }


@pytest.fixture
def mock_profile_data():
    """Mock profile data for testing"""
    from src.models.profile_data import ProfileData
    from datetime import datetime

    return ProfileData.create_new(
        url_id='test-url-id',
        profile_type='LINKEDIN',
        raw_content='<html><body>John Doe Software Engineer</body></html>',
        normalized_content={
            'headline': 'Senior Software Engineer',
            'summary': 'Experienced software engineer with expertise in Python and JavaScript',
            'skills': ['Python', 'JavaScript', 'React'],
            'experience_highlights': [
                {'company': 'Tech Corp', 'title': 'Senior Developer', 'duration': '2020-2023'}
            ]
        },
        extraction_status='SUCCESS',
        limitations=[]
    )


@pytest.fixture
def mock_github_data():
    """Mock GitHub profile data for testing"""
    from src.models.profile_data import ProfileData
    from datetime import datetime

    return ProfileData.create_new(
        url_id='test-github-url-id',
        profile_type='GITHUB',
        raw_content='<html><body>GitHub Profile</body></html>',
        normalized_content={
            'username': 'johndoe',
            'bio': 'Software developer passionate about open source',
            'repositories': [
                {
                    'name': 'my-project',
                    'description': 'A great project',
                    'stars': 42,
                    'forks': 5,
                    'language': 'Python',
                    'readme_snippet': 'This is a great project'
                }
            ],
            'total_stars': 42,
            'recent_activity': ['Updated README', 'Fixed bug in main'],
            'top_languages': ['Python', 'JavaScript']
        },
        extraction_status='SUCCESS',
        limitations=[]
    )


@pytest.fixture
def mock_portfolio_data():
    """Mock portfolio website data for testing"""
    from src.models.profile_data import ProfileData
    from datetime import datetime

    return ProfileData.create_new(
        url_id='test-portfolio-url-id',
        profile_type='PORTFOLIO',
        raw_content='<html><body>Portfolio Site</body></html>',
        normalized_content={
            'site_title': 'John Doe - Software Engineer',
            'bio_about': 'I am a passionate software engineer',
            'projects': [
                {
                    'name': 'E-commerce Platform',
                    'description': 'A full-stack e-commerce solution',
                    'technologies': ['React', 'Node.js', 'PostgreSQL'],
                    'links': ['https://demo.com']
                }
            ],
            'skills': ['React', 'Node.js', 'PostgreSQL'],
            'contact_visible': True,
            'pages_analyzed': 3
        },
        extraction_status='SUCCESS',
        limitations=[]
    )


@pytest.fixture
def mock_profile_analysis():
    """Mock profile analysis for testing"""
    from src.models.profile_analysis import ProfileAnalysis
    from src.models.improvement import ImprovementSuggestion

    # Create mock suggestions
    suggestions = [
        ImprovementSuggestion.create_new(
            profile_analysis_id='test-analysis-id',
            category='CONTENT',
            priority='HIGH',
            suggestion_text='Add more technical details to your projects',
            rationale='Provides more evidence of your technical skills',
            example='Instead of "built a web app", say "built a React web app with Node.js backend"'
        ),
        ImprovementSuggestion.create_new(
            profile_analysis_id='test-analysis-id',
            category='VISIBILITY',
            priority='MEDIUM',
            suggestion_text='Make your contact information more prominent',
            rationale='Recruiters need to be able to contact you easily',
            affected_section='Contact'
        )
    ]

    return ProfileAnalysis.create_new(
        profile_id='test-profile-id',
        profile_type='LINKEDIN',
        strengths=['Clear headline', 'Good skills section'],
        weaknesses=['Limited experience details'],
        suggestions=suggestions,
        clarity_score=75.0,
        impact_score=68.0
    )


@pytest.fixture
def mock_alignment_result():
    """Mock alignment result for testing"""
    from src.models.alignment import AlignmentResult

    return AlignmentResult.create_new(
        overall_score=82.5,
        skill_alignment={'Python': 90.0, 'JavaScript': 75.0, 'React': 85.0},
        experience_alignment={'Software Engineer': 88.0, 'Developer': 72.0},
        project_alignment={'Web App': 95.0, 'API': 78.0},
        discrepancies=[
            'Resume lists Java skills but GitHub shows primarily Python projects',
            'LinkedIn shows 5 years experience but resume shows 3 years'
        ],
        recommendations=[
            'Align skill priorities between resume and GitHub projects',
            'Update experience timeline to match LinkedIn profile'
        ]
    )


# Phase 3: Job Role Recommender fixtures

@pytest.fixture
def mock_industry_selection():
    """Mock industry selection for testing"""
    from src.models.industry import IndustrySelection
    from datetime import datetime

    return IndustrySelection(
        selection_id='test-industry-selection-id',
        session_id='test-session-id',
        industries=['Software Engineering', 'AI/ML'],
        specializations=['Backend Development', 'Machine Learning'],
        selection_timestamp=datetime.now()
    )


@pytest.fixture
def mock_profile_signals():
    """Mock profile signals for testing"""
    from src.models.profile_signals import ProfileSignals, ResumeSignals, ProfileSignalsData, ExperienceSummary

    return ProfileSignals(
        signals_id='test-signals-id',
        resume_signals=ResumeSignals(
            skills=['Python', 'JavaScript', 'React', 'Node.js'],
            experience_years=5.5,
            job_titles=['Software Engineer', 'Senior Developer'],
            industries=['Technology', 'FinTech'],
            education=[{
                'degree': 'B.S. Computer Science',
                'institution': 'University of Tech',
                'graduation_year': 2018
            }],
            certifications=['AWS Certified', 'Google Cloud Professional']
        ).dict(),
        profile_signals=ProfileSignalsData(
            github_activity={
                'total_commits': 1200,
                'repositories': 15,
                'stars_received': 42,
                'recent_activity': True
            },
            linkedin_summary={
                'headline': 'Senior Software Engineer',
                'summary': 'Experienced engineer with expertise in full-stack development',
                'connections': 500
            },
            portfolio_projects=[
                {
                    'name': 'E-commerce Platform',
                    'technologies': ['React', 'Node.js', 'PostgreSQL'],
                    'description': 'Full-stack e-commerce solution'
                }
            ],
            social_signals={
                'activity_level': 'HIGH',
                'professional_network': 'STRONG',
                'technical_recognition': 'GOOD'
            }
        ).dict(),
        aggregated_skills=['Python', 'JavaScript', 'React', 'Node.js', 'AWS', 'Docker'],
        experience_summary=ExperienceSummary(
            total_years=5.5,
            domains=['Web Development', 'Cloud Computing', 'DevOps'],
            leadership_indicators=['Team Lead', 'Mentor', 'Project Owner'],
            technology_stack=['Python', 'JavaScript', 'React', 'Node.js', 'AWS', 'Docker']
        ).dict(),
        project_highlights=[
            {
                'name': 'E-commerce Platform',
                'technologies': ['React', 'Node.js', 'PostgreSQL'],
                'impact': 'Increased sales by 25%',
                'role': 'Lead Developer'
            }
        ]
    )


@pytest.fixture
def mock_role_recommendation():
    """Mock role recommendation for testing"""
    from src.models.role_recommendation import RoleRecommendation, RecommendedRole
    from datetime import datetime

    return RoleRecommendation(
        recommendation_id='test-recommendation-id',
        session_id='test-session-id',
        roles=[
            RecommendedRole(
                role_id='test-role-1',
                title='Senior Software Engineer',
                industry='Software Engineering',
                seniority_level='SENIOR',
                fit_score=0.85,
                justification={
                    'skill_alignment': 'Strong Python and React experience aligns well',
                    'project_relevance': 'E-commerce project experience matches role requirements',
                    'technology_match': 'Experience with required tech stack (React, Node.js)',
                    'experience_alignment': '5+ years experience matches senior role requirements'
                },
                confidence_factors=['Strong skill alignment', 'Relevant project experience'],
                skill_gaps=['Kubernetes', 'Microservices architecture'],
                improvement_suggestions=['Learn Kubernetes for container orchestration', 'Study microservices design patterns']
            )
        ],
        overall_confidence=0.82,
        confidence_factors=['Strong technical background', 'Relevant experience'],
        recommendation_timestamp=datetime.now(),
        industry='Software Engineering'
    )


@pytest.fixture
def mock_role_archetypes():
    """Mock role archetypes for testing"""
    from src.services.knowledge_base import RoleArchetype

    archetypes = {
        'software_engineering_software_engineer': RoleArchetype({
            'title': 'Software Engineer',
            'industry': 'Software Engineering',
            'description': 'Develops, tests, and maintains software applications',
            'required_skills': ['Programming fundamentals', 'Software design patterns', 'Version control'],
            'preferred_skills': ['Testing frameworks', 'CI/CD pipelines', 'Cloud platforms'],
            'technologies': ['Python', 'JavaScript', 'Java', 'Docker'],
            'responsibilities': [
                'Write clean, maintainable code',
                'Collaborate with team members',
                'Participate in code reviews'
            ],
            'seniority_requirements': {
                'junior': {
                    'years_experience': '0-2',
                    'responsibilities': ['Implement features', 'Fix bugs', 'Write tests']
                },
                'mid': {
                    'years_experience': '3-5',
                    'responsibilities': ['Design components', 'Lead small projects', 'Mentor junior developers']
                },
                'senior': {
                    'years_experience': '6+',
                    'responsibilities': ['System architecture', 'Technical leadership', 'Strategic planning']
                }
            },
            'role_signals': {
                'technical_depth': 'Complex problem solving',
                'collaboration': 'Team work and communication',
                'innovation': 'New solutions and improvements'
            }
        }),
        'ai_ml_machine_learning_engineer': RoleArchetype({
            'title': 'Machine Learning Engineer',
            'industry': 'AI/ML',
            'description': 'Designs, builds, and deploys machine learning models and systems',
            'required_skills': ['Machine learning algorithms', 'Python programming', 'Data preprocessing', 'Model evaluation'],
            'preferred_skills': ['Deep learning frameworks', 'MLOps tools', 'Cloud ML platforms', 'Statistical analysis'],
            'technologies': ['TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy'],
            'responsibilities': [
                'Develop ML models for business problems',
                'Optimize model performance and accuracy',
                'Deploy models to production',
                'Monitor model performance'
            ],
            'seniority_requirements': {
                'junior': {
                    'years_experience': '0-2',
                    'responsibilities': ['Implement ML models', 'Data preprocessing', 'Basic model evaluation']
                },
                'mid': {
                    'years_experience': '3-5',
                    'responsibilities': ['Design ML systems', 'Model optimization', 'MLOps implementation']
                },
                'senior': {
                    'years_experience': '6+',
                    'responsibilities': ['ML architecture', 'Strategic ML initiatives', 'Team leadership']
                }
            },
            'role_signals': {
                'technical_depth': 'Advanced ML algorithms and systems',
                'innovation': 'Novel applications and improvements',
                'business_impact': 'Measurable outcomes from ML solutions'
            }
        })
    }

    return archetypes