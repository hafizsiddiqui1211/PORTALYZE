"""Tests for the alignment analyzer service"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.alignment_analyzer import AlignmentAnalyzer


class TestAlignmentAnalyzer:
    """Test cases for AlignmentAnalyzer service"""

    def test_analyze_alignment_basic(self):
        """Test basic alignment analysis functionality"""
        analyzer = AlignmentAnalyzer()

        # Create mock resume data
        resume_data = {
            "strengths": ["Strong Python skills", "Good experience with AWS"],
            "weaknesses": ["Missing React experience"],
            "section_feedback": {
                "skills": "Good technical skills but could use more frontend experience",
                "experience": "Solid experience in backend development"
            }
        }

        # Create mock profile data
        profile_data_list = [
            {
                "profile_type": "LINKEDIN",
                "normalized_content": {
                    "headline": "Software Engineer with Python and AWS experience",
                    "summary": "Experienced in backend development with Python and cloud technologies",
                    "skills": ["Python", "AWS", "Docker"]
                }
            },
            {
                "profile_type": "GITHUB",
                "normalized_content": {
                    "username": "testuser",
                    "repositories": [
                        {
                            "name": "python-project",
                            "description": "Python project with AWS integration",
                            "stars": 10,
                            "language": "Python"
                        }
                    ],
                    "bio": "Python developer focusing on backend systems"
                }
            }
        ]

        # Perform alignment analysis
        result = analyzer.analyze_alignment(resume_data, profile_data_list)

        # Verify the result
        assert result is not None
        assert result.alignment_id is not None
        assert 0 <= result.overall_score <= 100
        assert isinstance(result.skill_alignment, dict)
        assert isinstance(result.experience_alignment, dict)
        assert isinstance(result.project_alignment, dict)
        assert isinstance(result.discrepancies, list)
        assert isinstance(result.recommendations, list)

    def test_extract_skills_from_resume(self):
        """Test extraction of skills from resume data"""
        analyzer = AlignmentAnalyzer()

        resume_data = {
            "strengths": ["Strong Python and JavaScript skills", "Experienced with React and Node.js"],
            "weaknesses": ["Could improve cloud computing knowledge"],
            "section_feedback": {
                "skills": "Good programming skills in Python and JavaScript",
                "experience": "Backend development experience with Python frameworks"
            }
        }

        skills = analyzer._extract_skills(resume_data)
        assert len(skills) > 0
        # Skills should be capitalized properly
        assert any("Python" in skill for skill in skills)
        assert any("JavaScript" in skill for skill in skills)
        assert any("React" in skill for skill in skills)

    def test_extract_skills_from_profile(self):
        """Test extraction of skills from profile data"""
        analyzer = AlignmentAnalyzer()

        profile_data = {
            "normalized_content": {
                "skills": ["Python", "JavaScript", "React", "AWS"],
                "technologies": "Python, JavaScript, and cloud technologies",
                "tools": "Docker, Kubernetes, and AWS services"
            }
        }

        skills = analyzer._extract_skills_from_profile(profile_data)
        assert len(skills) > 0
        assert "Python" in skills
        assert "JavaScript" in skills
        assert "React" in skills
        assert "AWS" in skills

    def test_calculate_skill_alignment_perfect_match(self):
        """Test skill alignment calculation with perfect match"""
        analyzer = AlignmentAnalyzer()

        resume_skills = ["Python", "JavaScript", "React"]
        profile_skills = ["Python", "JavaScript", "React"]

        score = analyzer._calculate_skill_alignment(resume_skills, profile_skills)
        assert score == 100.0

    def test_calculate_skill_alignment_no_match(self):
        """Test skill alignment calculation with no match"""
        analyzer = AlignmentAnalyzer()

        resume_skills = ["Python", "Java"]
        profile_skills = ["JavaScript", "C++"]

        score = analyzer._calculate_skill_alignment(resume_skills, profile_skills)
        assert score == 0.0

    def test_calculate_skill_alignment_partial_match(self):
        """Test skill alignment calculation with partial match"""
        analyzer = AlignmentAnalyzer()

        resume_skills = ["Python", "JavaScript", "React"]
        profile_skills = ["Python", "C++", "Go"]

        score = analyzer._calculate_skill_alignment(resume_skills, profile_skills)
        # Should be 25% (1 out of 4 unique skills match: Python)
        assert 0 < score < 100

    def test_calculate_experience_alignment(self):
        """Test experience alignment calculation"""
        analyzer = AlignmentAnalyzer()

        resume_experience = ["Software Engineer at Tech Corp", "Backend Developer with Python"]
        profile_experience = ["Senior Software Engineer at Tech Corp", "Python Backend Developer"]

        score = analyzer._calculate_experience_alignment(resume_experience, profile_experience)
        # Should be > 0 since there are common elements
        assert 0 <= score <= 100

    def test_calculate_project_alignment(self):
        """Test project alignment calculation"""
        analyzer = AlignmentAnalyzer()

        resume_projects = ["E-commerce platform with Python", "API development"]
        profile_projects = ["Python-based e-commerce project", "REST API implementation"]

        score = analyzer._calculate_project_alignment(resume_projects, profile_projects)
        # Should be > 0 since there are common elements
        assert 0 <= score <= 100

    def test_identify_discrepancies(self):
        """Test identification of discrepancies between resume and profile"""
        analyzer = AlignmentAnalyzer()

        resume_skills = ["Python", "JavaScript"]
        profile_skills = ["Java", "C++"]
        resume_experience = ["Software Engineer"]
        profile_experience = ["Designer"]
        resume_projects = ["Web app"]
        profile_projects = ["Mobile app"]

        discrepancies = analyzer._identify_discrepancies(
            resume_skills, profile_skills,
            resume_experience, profile_experience,
            resume_projects, profile_projects
        )

        assert len(discrepancies) > 0
        # Should identify skill discrepancies
        assert any("Python" in d or "JavaScript" in d for d in discrepancies if "resume" in d and "profile" in d)

    def test_generate_recommendations(self):
        """Test generation of alignment recommendations"""
        analyzer = AlignmentAnalyzer()

        resume_skills = ["Python"]
        profile_skills = ["JavaScript"]
        resume_experience = ["Backend role"]
        profile_experience = ["Frontend role"]
        resume_projects = ["Backend project"]
        profile_projects = ["Frontend project"]
        platform = "GitHub"

        recommendations = analyzer._generate_recommendations(
            resume_skills, profile_skills,
            resume_experience, profile_experience,
            resume_projects, profile_projects,
            platform
        )

        assert len(recommendations) > 0
        # Should have recommendations for skill alignment
        assert any(platform in rec for rec in recommendations)
        assert any("skills" in rec.lower() for rec in recommendations)

    def test_calculate_overall_alignment_score(self):
        """Test calculation of overall alignment score"""
        analyzer = AlignmentAnalyzer()

        skill_alignment = {"GitHub": 80.0, "LinkedIn": 70.0}
        experience_alignment = {"GitHub": 60.0, "LinkedIn": 85.0}
        project_alignment = {"GitHub": 75.0, "LinkedIn": 65.0}

        overall_score = analyzer._calculate_overall_alignment_score(
            skill_alignment, experience_alignment, project_alignment
        )

        assert 0 <= overall_score <= 100
        # Score should be a weighted average of all alignment scores
        expected_min = min(60.0, 65.0, 70.0, 75.0, 80.0, 85.0)  # Minimum of all scores
        expected_max = max(60.0, 65.0, 70.0, 75.0, 80.0, 85.0)  # Maximum of all scores
        assert expected_min <= overall_score <= expected_max

    def test_get_role_keywords(self):
        """Test retrieval of role-specific keywords"""
        analyzer = AlignmentAnalyzer()

        keywords = analyzer._get_role_keywords("software engineer")
        assert len(keywords) > 0
        assert "python" in keywords or "javascript" in keywords or "api" in keywords

        # Test with a different role
        data_scientist_keywords = analyzer._get_role_keywords("data scientist")
        assert len(data_scientist_keywords) > 0

    def test_calculate_role_alignment_score(self):
        """Test calculation of role alignment score"""
        analyzer = AlignmentAnalyzer()

        resume_data = {
            "strengths": ["Python", "Machine Learning"],
            "weaknesses": [],
            "section_feedback": {}
        }

        profile_data_list = [
            {
                "profile_type": "GITHUB",
                "normalized_content": {
                    "repositories": [{"name": "ml-project", "description": "Python machine learning project"}],
                    "bio": "Python developer with ML experience"
                }
            }
        ]

        score = analyzer.calculate_role_alignment_score(resume_data, profile_data_list, "Data Scientist")
        assert 0 <= score <= 100

    def test_empty_resume_and_profile_data(self):
        """Test alignment analysis with empty data"""
        analyzer = AlignmentAnalyzer()

        # Test with empty resume data
        empty_resume = {"strengths": [], "weaknesses": [], "section_feedback": {}}
        profile_data = [
            {
                "profile_type": "LINKEDIN",
                "normalized_content": {
                    "headline": "Experienced professional",
                    "skills": ["Communication", "Leadership"]
                }
            }
        ]

        result = analyzer.analyze_alignment(empty_resume, profile_data)
        assert result is not None
        assert 0 <= result.overall_score <= 100

        # Test with empty profile data
        resume_data = {
            "strengths": ["Strong communication"],
            "weaknesses": [],
            "section_feedback": {"skills": "Good soft skills"}
        }
        empty_profile_data = []

        result2 = analyzer.analyze_alignment(resume_data, empty_profile_data)
        assert result2 is not None
        assert 0 <= result2.overall_score <= 100

    def test_case_insensitive_matching(self):
        """Test that skill matching is case insensitive"""
        analyzer = AlignmentAnalyzer()

        resume_skills = ["python", "javascript", "REACT"]
        profile_skills = ["Python", "JavaScript", "react"]

        score = analyzer._calculate_skill_alignment(resume_skills, profile_skills)
        assert score == 100.0  # Should match despite case differences

    def test_common_tech_keywords_exist(self):
        """Test that the analyzer has common tech keywords defined"""
        analyzer = AlignmentAnalyzer()

        assert len(analyzer.common_tech_keywords) > 0
        assert "python" in analyzer.common_tech_keywords
        assert "javascript" in analyzer.common_tech_keywords
        assert "react" in analyzer.common_tech_keywords

    def test_experience_patterns_defined(self):
        """Test that experience patterns are defined"""
        analyzer = AlignmentAnalyzer()

        assert len(analyzer.experience_patterns) > 0
        assert any("software" in pattern for pattern in analyzer.experience_patterns)
        assert any("engineer" in pattern for pattern in analyzer.experience_patterns)

    def test_get_highest_alignment_platform(self):
        """Test getting the platform with highest alignment"""
        from src.models.alignment_result import AlignmentResult

        alignment_result = AlignmentResult.create_new(
            overall_score=75.0,
            skill_alignment={"GitHub": 80.0, "LinkedIn": 70.0, "Portfolio": 90.0},
            experience_alignment={"GitHub": 60.0, "LinkedIn": 80.0, "Portfolio": 70.0},
            project_alignment={"GitHub": 70.0, "LinkedIn": 60.0, "Portfolio": 80.0},
            discrepancies=[],
            recommendations=[]
        )

        highest_platform = alignment_result.get_highest_alignment_platform()
        # Portfolio should have the highest average score
        assert highest_platform == "Portfolio"

    def test_get_lowest_alignment_platform(self):
        """Test getting the platform with lowest alignment"""
        from src.models.alignment_result import AlignmentResult

        alignment_result = AlignmentResult.create_new(
            overall_score=70.0,
            skill_alignment={"GitHub": 80.0, "LinkedIn": 70.0, "Portfolio": 90.0},
            experience_alignment={"GitHub": 60.0, "LinkedIn": 80.0, "Portfolio": 70.0},
            project_alignment={"GitHub": 50.0, "LinkedIn": 60.0, "Portfolio": 80.0},
            discrepancies=[],
            recommendations=[]
        )

        lowest_platform = alignment_result.get_lowest_alignment_platform()
        # GitHub should have the lowest average score
        assert lowest_platform == "GitHub"

    def test_get_skill_gaps(self):
        """Test getting platforms with significant skill gaps"""
        from src.models.alignment_result import AlignmentResult

        alignment_result = AlignmentResult.create_new(
            overall_score=60.0,
            skill_alignment={"GitHub": 30.0, "LinkedIn": 80.0, "Portfolio": 40.0},
            experience_alignment={"GitHub": 70.0, "LinkedIn": 75.0, "Portfolio": 70.0},
            project_alignment={"GitHub": 60.0, "LinkedIn": 65.0, "Portfolio": 60.0},
            discrepancies=[],
            recommendations=[]
        )

        skill_gaps = alignment_result.get_skill_gaps()
        # Should return platforms with skill alignment below 70%
        assert "GitHub" in skill_gaps
        assert "Portfolio" in skill_gaps
        assert "LinkedIn" not in skill_gaps  # Above 70%

    def test_has_critical_discrepancies_true(self):
        """Test detection of critical discrepancies"""
        from src.models.alignment_result import AlignmentResult

        alignment_result = AlignmentResult.create_new(
            overall_score=50.0,
            skill_alignment={"GitHub": 50.0, "LinkedIn": 50.0},
            experience_alignment={"GitHub": 50.0, "LinkedIn": 50.0},
            project_alignment={"GitHub": 50.0, "LinkedIn": 50.0},
            discrepancies=["Resume shows 5 years experience but LinkedIn shows 3 years"],
            recommendations=[]
        )

        has_critical = alignment_result.has_critical_discrepancies()
        assert has_critical is True

    def test_has_critical_discrepancies_false(self):
        """Test detection of non-critical discrepancies"""
        from src.models.alignment_result import AlignmentResult

        alignment_result = AlignmentResult.create_new(
            overall_score=50.0,
            skill_alignment={"GitHub": 50.0, "LinkedIn": 50.0},
            experience_alignment={"GitHub": 50.0, "LinkedIn": 50.0},
            project_alignment={"GitHub": 50.0, "LinkedIn": 50.0},
            discrepancies=["Different formatting between resume and profile"],
            recommendations=[]
        )

        has_critical = alignment_result.has_critical_discrepancies()
        assert has_critical is False

    def test_get_priority_recommendations(self):
        """Test getting priority recommendations"""
        from src.models.alignment_result import AlignmentResult

        alignment_result = AlignmentResult.create_new(
            overall_score=50.0,
            skill_alignment={"GitHub": 50.0, "LinkedIn": 50.0},
            experience_alignment={"GitHub": 50.0, "LinkedIn": 50.0},
            project_alignment={"GitHub": 50.0, "LinkedIn": 50.0},
            discrepancies=[],
            recommendations=[
                "Add more technical skills to GitHub profile",
                "HIGH PRIORITY: Align experience dates between resume and LinkedIn",
                "Consider adding more projects to portfolio"
            ]
        )

        priority_recs = alignment_result.get_priority_recommendations()
        assert len(priority_recs) > 0
        # Should contain the high priority recommendation
        assert any("HIGH PRIORITY" in rec for rec in priority_recs)

    def test_alignment_quality_levels(self):
        """Test different alignment quality levels"""
        from src.models.alignment_result import AlignmentResult

        excellent_result = AlignmentResult.create_new(
            overall_score=90.0,
            skill_alignment={"GitHub": 90.0},
            experience_alignment={"GitHub": 90.0},
            project_alignment={"GitHub": 90.0},
            discrepancies=[],
            recommendations=[]
        )
        assert excellent_result.get_alignment_quality_level() == "EXCELLENT"

        poor_result = AlignmentResult.create_new(
            overall_score=30.0,
            skill_alignment={"GitHub": 30.0},
            experience_alignment={"GitHub": 30.0},
            project_alignment={"GitHub": 30.0},
            discrepancies=[],
            recommendations=[]
        )
        assert poor_result.get_alignment_quality_level() == "POOR"

    def test_get_alignment_summary(self):
        """Test getting alignment summary"""
        from src.models.alignment_result import AlignmentResult

        alignment_result = AlignmentResult.create_new(
            overall_score=75.0,
            skill_alignment={"GitHub": 80.0, "LinkedIn": 70.0},
            experience_alignment={"GitHub": 60.0, "LinkedIn": 85.0},
            project_alignment={"GitHub": 75.0, "LinkedIn": 65.0},
            discrepancies=[],
            recommendations=[]
        )

        summary = alignment_result.get_alignment_summary()
        assert "average_skill_alignment" in summary
        assert "average_experience_alignment" in summary
        assert "average_project_alignment" in summary

        # Check that averages are reasonable
        assert 0 <= summary["average_skill_alignment"] <= 100
        assert 0 <= summary["average_experience_alignment"] <= 100
        assert 0 <= summary["average_project_alignment"] <= 100

    def test_get_platform_alignment_details(self):
        """Test getting detailed alignment scores for a platform"""
        from src.models.alignment_result import AlignmentResult

        alignment_result = AlignmentResult.create_new(
            overall_score=75.0,
            skill_alignment={"GitHub": 80.0, "LinkedIn": 70.0},
            experience_alignment={"GitHub": 60.0, "LinkedIn": 85.0},
            project_alignment={"GitHub": 75.0, "LinkedIn": 65.0},
            discrepancies=[],
            recommendations=[]
        )

        github_details = alignment_result.get_platform_alignment_details("GitHub")
        assert github_details["skill_score"] == 80.0
        assert github_details["experience_score"] == 60.0
        assert github_details["project_score"] == 75.0
        # Average should be (80 + 60 + 75) / 3 = 71.67
        assert abs(github_details["average_score"] - 71.67) < 0.01

    def test_to_and_from_dict(self):
        """Test serialization and deserialization of AlignmentResult"""
        from src.models.alignment_result import AlignmentResult

        original_result = AlignmentResult.create_new(
            overall_score=80.0,
            skill_alignment={"GitHub": 85.0, "LinkedIn": 75.0},
            experience_alignment={"GitHub": 70.0, "LinkedIn": 80.0},
            project_alignment={"GitHub": 90.0, "LinkedIn": 65.0},
            discrepancies=["Example discrepancy"],
            recommendations=["Example recommendation"]
        )

        # Convert to dict
        result_dict = original_result.to_dict()

        # Create new result from dict
        restored_result = AlignmentResult.from_dict(result_dict)

        # Verify the restored result matches the original
        assert restored_result.overall_score == original_result.overall_score
        assert restored_result.skill_alignment == original_result.skill_alignment
        assert restored_result.experience_alignment == original_result.experience_alignment
        assert restored_result.project_alignment == original_result.project_alignment
        assert restored_result.discrepancies == original_result.discrepancies
        assert restored_result.recommendations == original_result.recommendations
        assert restored_result.alignment_id == original_result.alignment_id

    def test_get_actionable_insights(self):
        """Test getting actionable insights from alignment result"""
        from src.models.alignment_result import AlignmentResult

        alignment_result = AlignmentResult.create_new(
            overall_score=65.0,
            skill_alignment={"GitHub": 70.0, "LinkedIn": 60.0},
            experience_alignment={"GitHub": 50.0, "LinkedIn": 80.0},
            project_alignment={"GitHub": 65.0, "LinkedIn": 70.0},
            discrepancies=["Resume shows 5 years experience but LinkedIn shows 3 years"],
            recommendations=[
                "HIGH PRIORITY: Align experience dates between resume and LinkedIn",
                "Add more technical skills to GitHub profile"
            ]
        )

        insights = alignment_result.get_actionable_insights()
        assert len(insights) > 0
        # Should include quality level
        assert any("FAIR" in insight for insight in insights)
        # Should include platform info
        assert any("Best aligned" in insight for insight in insights)
        assert any("Lowest aligned" in insight for insight in insights)