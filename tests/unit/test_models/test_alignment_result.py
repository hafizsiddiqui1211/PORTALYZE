"""Tests for the AlignmentResult model"""
import pytest
from datetime import datetime
from src.models.alignment_result import AlignmentResult


class TestAlignmentResult:
    """Test cases for AlignmentResult entity"""

    def test_alignment_result_creation_success(self):
        """Test successful creation of an AlignmentResult entity"""
        alignment_result = AlignmentResult(
            alignment_id="test-alignment-id",
            overall_score=75.0,
            skill_alignment={"GitHub": 80.0, "LinkedIn": 70.0},
            experience_alignment={"GitHub": 60.0, "LinkedIn": 85.0},
            project_alignment={"GitHub": 75.0, "LinkedIn": 65.0},
            discrepancies=["Example discrepancy"],
            recommendations=["Example recommendation"],
            analysis_timestamp=datetime.now()
        )

        assert alignment_result.alignment_id == "test-alignment-id"
        assert alignment_result.overall_score == 75.0
        assert alignment_result.skill_alignment == {"GitHub": 80.0, "LinkedIn": 70.0}
        assert alignment_result.experience_alignment == {"GitHub": 60.0, "LinkedIn": 85.0}
        assert alignment_result.project_alignment == {"GitHub": 75.0, "LinkedIn": 65.0}
        assert alignment_result.discrepancies == ["Example discrepancy"]
        assert alignment_result.recommendations == ["Example recommendation"]

    def test_alignment_result_creation_with_invalid_overall_score_low(self):
        """Test AlignmentResult creation fails with overall score below 0"""
        with pytest.raises(ValueError, match="overall_score must be between 0 and 100"):
            AlignmentResult(
                alignment_id="test-alignment-id",
                overall_score=-10.0,  # Invalid: below 0
                skill_alignment={"GitHub": 80.0},
                experience_alignment={"GitHub": 60.0},
                project_alignment={"GitHub": 75.0},
                discrepancies=[],
                recommendations=[],
                analysis_timestamp=datetime.now()
            )

    def test_alignment_result_creation_with_invalid_overall_score_high(self):
        """Test AlignmentResult creation fails with overall score above 100"""
        with pytest.raises(ValueError, match="overall_score must be between 0 and 100"):
            AlignmentResult(
                alignment_id="test-alignment-id",
                overall_score=150.0,  # Invalid: above 100
                skill_alignment={"GitHub": 80.0},
                experience_alignment={"GitHub": 60.0},
                project_alignment={"GitHub": 75.0},
                discrepancies=[],
                recommendations=[],
                analysis_timestamp=datetime.now()
            )

    def test_alignment_result_creation_with_invalid_skill_alignment_score(self):
        """Test AlignmentResult creation fails with invalid skill alignment score"""
        with pytest.raises(ValueError, match="Skill alignment score for GitHub must be between 0 and 100"):
            AlignmentResult(
                alignment_id="test-alignment-id",
                overall_score=75.0,
                skill_alignment={"GitHub": 150.0},  # Invalid: above 100
                experience_alignment={"GitHub": 60.0},
                project_alignment={"GitHub": 75.0},
                discrepancies=[],
                recommendations=[],
                analysis_timestamp=datetime.now()
            )

    def test_alignment_result_creation_with_invalid_experience_alignment_score(self):
        """Test AlignmentResult creation fails with invalid experience alignment score"""
        with pytest.raises(ValueError, match="Experience alignment score for GitHub must be between 0 and 100"):
            AlignmentResult(
                alignment_id="test-alignment-id",
                overall_score=75.0,
                skill_alignment={"GitHub": 80.0},
                experience_alignment={"GitHub": -10.0},  # Invalid: below 0
                project_alignment={"GitHub": 75.0},
                discrepancies=[],
                recommendations=[],
                analysis_timestamp=datetime.now()
            )

    def test_alignment_result_creation_with_invalid_project_alignment_score(self):
        """Test AlignmentResult creation fails with invalid project alignment score"""
        with pytest.raises(ValueError, match="Project alignment score for GitHub must be between 0 and 100"):
            AlignmentResult(
                alignment_id="test-alignment-id",
                overall_score=75.0,
                skill_alignment={"GitHub": 80.0},
                experience_alignment={"GitHub": 60.0},
                project_alignment={"GitHub": 120.0},  # Invalid: above 100
                discrepancies=[],
                recommendations=[],
                analysis_timestamp=datetime.now()
            )

    def test_alignment_result_creation_with_non_dict_alignments(self):
        """Test AlignmentResult creation fails with non-dict alignment values"""
        with pytest.raises(ValueError, match="skill_alignment must be a dictionary"):
            AlignmentResult(
                alignment_id="test-alignment-id",
                overall_score=75.0,
                skill_alignment="not_a_dict",  # Invalid: not a dict
                experience_alignment={"GitHub": 60.0},
                project_alignment={"GitHub": 75.0},
                discrepancies=[],
                recommendations=[],
                analysis_timestamp=datetime.now()
            )

        with pytest.raises(ValueError, match="experience_alignment must be a dictionary"):
            AlignmentResult(
                alignment_id="test-alignment-id",
                overall_score=75.0,
                skill_alignment={"GitHub": 80.0},
                experience_alignment=["not_a_dict"],  # Invalid: not a dict
                project_alignment={"GitHub": 75.0},
                discrepancies=[],
                recommendations=[],
                analysis_timestamp=datetime.now()
            )

        with pytest.raises(ValueError, match="project_alignment must be a dictionary"):
            AlignmentResult(
                alignment_id="test-alignment-id",
                overall_score=75.0,
                skill_alignment={"GitHub": 80.0},
                experience_alignment={"GitHub": 60.0},
                project_alignment=50.0,  # Invalid: not a dict
                discrepancies=[],
                recommendations=[],
                analysis_timestamp=datetime.now()
            )

    def test_alignment_result_creation_with_non_list_discrepancies(self):
        """Test AlignmentResult creation fails with non-list discrepancies"""
        with pytest.raises(ValueError, match="discrepancies must be a list"):
            AlignmentResult(
                alignment_id="test-alignment-id",
                overall_score=75.0,
                skill_alignment={"GitHub": 80.0},
                experience_alignment={"GitHub": 60.0},
                project_alignment={"GitHub": 75.0},
                discrepancies="not_a_list",  # Invalid: not a list
                recommendations=[],
                analysis_timestamp=datetime.now()
            )

    def test_alignment_result_creation_with_non_list_recommendations(self):
        """Test AlignmentResult creation fails with non-list recommendations"""
        with pytest.raises(ValueError, match="recommendations must be a list"):
            AlignmentResult(
                alignment_id="test-alignment-id",
                overall_score=75.0,
                skill_alignment={"GitHub": 80.0},
                experience_alignment={"GitHub": 60.0},
                project_alignment={"GitHub": 75.0},
                discrepancies=[],
                recommendations={"not": "a_list"},  # Invalid: not a list
                analysis_timestamp=datetime.now()
            )

    def test_alignment_result_creation_with_empty_id(self):
        """Test AlignmentResult creation fails with empty ID"""
        with pytest.raises(ValueError, match="alignment_id cannot be empty"):
            AlignmentResult(
                alignment_id="",  # Invalid: empty
                overall_score=75.0,
                skill_alignment={"GitHub": 80.0},
                experience_alignment={"GitHub": 60.0},
                project_alignment={"GitHub": 75.0},
                discrepancies=[],
                recommendations=[],
                analysis_timestamp=datetime.now()
            )

    def test_create_new_classmethod(self):
        """Test the create_new class method"""
        result = AlignmentResult.create_new(
            overall_score=80.0,
            skill_alignment={"GitHub": 85.0, "LinkedIn": 75.0},
            experience_alignment={"GitHub": 80.0, "LinkedIn": 70.0},
            project_alignment={"GitHub": 90.0, "LinkedIn": 85.0},
            discrepancies=["Example discrepancy"],
            recommendations=["Example recommendation"]
        )

        assert result.alignment_id is not None
        assert result.alignment_id != ""
        assert result.overall_score == 80.0
        assert result.skill_alignment == {"GitHub": 85.0, "LinkedIn": 75.0}
        assert result.experience_alignment == {"GitHub": 80.0, "LinkedIn": 70.0}
        assert result.project_alignment == {"GitHub": 90.0, "LinkedIn": 85.0}
        assert result.discrepancies == ["Example discrepancy"]
        assert result.recommendations == ["Example recommendation"]
        assert result.analysis_timestamp is not None

    def test_get_highest_alignment_platform(self):
        """Test getting the platform with highest alignment"""
        result = AlignmentResult.create_new(
            overall_score=75.0,
            skill_alignment={"GitHub": 80.0, "LinkedIn": 70.0, "Portfolio": 90.0},
            experience_alignment={"GitHub": 60.0, "LinkedIn": 85.0, "Portfolio": 70.0},
            project_alignment={"GitHub": 75.0, "LinkedIn": 65.0, "Portfolio": 80.0},
            discrepancies=[],
            recommendations=[]
        )

        highest_platform = result.get_highest_alignment_platform()
        # Portfolio has the highest average: (90+70+80)/3 = 80
        assert highest_platform == "Portfolio"

    def test_get_lowest_alignment_platform(self):
        """Test getting the platform with lowest alignment"""
        result = AlignmentResult.create_new(
            overall_score=70.0,
            skill_alignment={"GitHub": 80.0, "LinkedIn": 70.0, "Portfolio": 60.0},
            experience_alignment={"GitHub": 60.0, "LinkedIn": 85.0, "Portfolio": 50.0},
            project_alignment={"GitHub": 75.0, "LinkedIn": 65.0, "Portfolio": 70.0},
            discrepancies=[],
            recommendations=[]
        )

        lowest_platform = result.get_lowest_alignment_platform()
        # Portfolio has the lowest average: (60+50+70)/3 = 60
        assert lowest_platform == "Portfolio"

    def test_get_skill_gaps(self):
        """Test getting platforms with significant skill gaps"""
        result = AlignmentResult.create_new(
            overall_score=60.0,
            skill_alignment={"GitHub": 40.0, "LinkedIn": 70.0, "Portfolio": 30.0},
            experience_alignment={"GitHub": 60.0, "LinkedIn": 80.0, "Portfolio": 70.0},
            project_alignment={"GitHub": 50.0, "LinkedIn": 65.0, "Portfolio": 60.0},
            discrepancies=[],
            recommendations=[]
        )

        skill_gaps = result.get_skill_gaps()
        # Should return platforms with skill alignment below 70%
        assert "GitHub" in skill_gaps  # 40% < 70%
        assert "Portfolio" in skill_gaps  # 30% < 70%
        assert "LinkedIn" not in skill_gaps  # 70% = 70%

    def test_get_experience_gaps(self):
        """Test getting platforms with significant experience gaps"""
        result = AlignmentResult.create_new(
            overall_score=65.0,
            skill_alignment={"GitHub": 70.0, "LinkedIn": 75.0, "Portfolio": 80.0},
            experience_alignment={"GitHub": 40.0, "LinkedIn": 90.0, "Portfolio": 30.0},
            project_alignment={"GitHub": 60.0, "LinkedIn": 70.0, "Portfolio": 70.0},
            discrepancies=[],
            recommendations=[]
        )

        experience_gaps = result.get_experience_gaps()
        # Should return platforms with experience alignment below 70%
        assert "GitHub" in experience_gaps  # 40% < 70%
        assert "Portfolio" in experience_gaps  # 30% < 70%
        assert "LinkedIn" not in experience_gaps  # 90% > 70%

    def test_get_project_gaps(self):
        """Test getting platforms with significant project gaps"""
        result = AlignmentResult.create_new(
            overall_score=70.0,
            skill_alignment={"GitHub": 80.0, "LinkedIn": 75.0, "Portfolio": 85.0},
            experience_alignment={"GitHub": 70.0, "LinkedIn": 80.0, "Portfolio": 75.0},
            project_alignment={"GitHub": 40.0, "LinkedIn": 60.0, "Portfolio": 30.0},
            discrepancies=[],
            recommendations=[]
        )

        project_gaps = result.get_project_gaps()
        # Should return platforms with project alignment below 70%
        assert "GitHub" in project_gaps  # 40% < 70%
        assert "Portfolio" in project_gaps  # 30% < 70%
        assert "LinkedIn" in project_gaps  # 60% < 70%

    def test_has_critical_discrepancies_true(self):
        """Test detection of critical discrepancies"""
        result = AlignmentResult.create_new(
            overall_score=50.0,
            skill_alignment={"GitHub": 50.0, "LinkedIn": 50.0},
            experience_alignment={"GitHub": 50.0, "LinkedIn": 50.0},
            project_alignment={"GitHub": 50.0, "LinkedIn": 50.0},
            discrepancies=["Resume shows 5 years experience but LinkedIn shows 3 years"],
            recommendations=[]
        )

        assert result.has_critical_discrepancies() is True

    def test_has_critical_discrepancies_false(self):
        """Test detection of non-critical discrepancies"""
        result = AlignmentResult.create_new(
            overall_score=50.0,
            skill_alignment={"GitHub": 50.0, "LinkedIn": 50.0},
            experience_alignment={"GitHub": 50.0, "LinkedIn": 50.0},
            project_alignment={"GitHub": 50.0, "LinkedIn": 50.0},
            discrepancies=["Different formatting between resume and profile"],
            recommendations=[]
        )

        assert result.has_critical_discrepancies() is False

    def test_get_priority_recommendations(self):
        """Test getting priority recommendations"""
        result = AlignmentResult.create_new(
            overall_score=70.0,
            skill_alignment={"GitHub": 70.0, "LinkedIn": 70.0},
            experience_alignment={"GitHub": 70.0, "LinkedIn": 70.0},
            project_alignment={"GitHub": 70.0, "LinkedIn": 70.0},
            discrepancies=[],
            recommendations=[
                "Add more technical skills to GitHub profile",
                "HIGH PRIORITY: Align experience dates between resume and LinkedIn",
                "Consider adding more projects to portfolio"
            ]
        )

        priority_recs = result.get_priority_recommendations()
        # Should include recommendations with priority indicators
        assert len(priority_recs) > 0

    def test_get_alignment_quality_level_excellent(self):
        """Test getting excellent alignment quality level"""
        result = AlignmentResult.create_new(
            overall_score=90.0,
            skill_alignment={"GitHub": 90.0},
            experience_alignment={"GitHub": 90.0},
            project_alignment={"GitHub": 90.0},
            discrepancies=[],
            recommendations=[]
        )

        assert result.get_alignment_quality_level() == "EXCELLENT"

    def test_get_alignment_quality_level_good(self):
        """Test getting good alignment quality level"""
        result = AlignmentResult.create_new(
            overall_score=75.0,
            skill_alignment={"GitHub": 75.0},
            experience_alignment={"GitHub": 75.0},
            project_alignment={"GitHub": 75.0},
            discrepancies=[],
            recommendations=[]
        )

        assert result.get_alignment_quality_level() == "GOOD"

    def test_get_alignment_quality_level_fair(self):
        """Test getting fair alignment quality level"""
        result = AlignmentResult.create_new(
            overall_score=60.0,
            skill_alignment={"GitHub": 60.0},
            experience_alignment={"GitHub": 60.0},
            project_alignment={"GitHub": 60.0},
            discrepancies=[],
            recommendations=[]
        )

        assert result.get_alignment_quality_level() == "FAIR"

    def test_get_alignment_quality_level_poor(self):
        """Test getting poor alignment quality level"""
        result = AlignmentResult.create_new(
            overall_score=40.0,
            skill_alignment={"GitHub": 40.0},
            experience_alignment={"GitHub": 40.0},
            project_alignment={"GitHub": 40.0},
            discrepancies=[],
            recommendations=[]
        )

        assert result.get_alignment_quality_level() == "POOR"

    def test_get_alignment_summary(self):
        """Test getting alignment summary"""
        result = AlignmentResult.create_new(
            overall_score=70.0,
            skill_alignment={"GitHub": 80.0, "LinkedIn": 60.0},
            experience_alignment={"GitHub": 60.0, "LinkedIn": 80.0},
            project_alignment={"GitHub": 70.0, "LinkedIn": 65.0},
            discrepancies=[],
            recommendations=[]
        )

        summary = result.get_alignment_summary()
        assert "average_skill_alignment" in summary
        assert "average_experience_alignment" in summary
        assert "average_project_alignment" in summary

        # Check that averages are correct
        expected_avg_skills = (80.0 + 60.0) / 2  # 70.0
        expected_avg_experience = (60.0 + 80.0) / 2  # 70.0
        expected_avg_projects = (70.0 + 65.0) / 2  # 67.5

        assert summary["average_skill_alignment"] == expected_avg_skills
        assert summary["average_experience_alignment"] == expected_avg_experience
        assert summary["average_project_alignment"] == expected_avg_projects

    def test_get_platform_alignment_details(self):
        """Test getting platform alignment details"""
        result = AlignmentResult.create_new(
            overall_score=75.0,
            skill_alignment={"GitHub": 80.0, "LinkedIn": 70.0},
            experience_alignment={"GitHub": 60.0, "LinkedIn": 85.0},
            project_alignment={"GitHub": 75.0, "LinkedIn": 65.0},
            discrepancies=[],
            recommendations=[]
        )

        github_details = result.get_platform_alignment_details("GitHub")
        assert github_details["skill_score"] == 80.0
        assert github_details["experience_score"] == 60.0
        assert github_details["project_score"] == 75.0
        # Average should be (80 + 60 + 75) / 3 = 71.67
        expected_avg = (80.0 + 60.0 + 75.0) / 3
        assert abs(github_details["average_score"] - expected_avg) < 0.01

        linkedin_details = result.get_platform_alignment_details("LinkedIn")
        assert linkedin_details["skill_score"] == 70.0
        assert linkedin_details["experience_score"] == 85.0
        assert linkedin_details["project_score"] == 65.0
        # Average should be (70 + 85 + 65) / 3 = 73.33
        expected_avg = (70.0 + 85.0 + 65.0) / 3
        assert abs(linkedin_details["average_score"] - expected_avg) < 0.01

    def test_get_total_discrepancies_count(self):
        """Test getting total discrepancies count"""
        result = AlignmentResult.create_new(
            overall_score=70.0,
            skill_alignment={"GitHub": 70.0},
            experience_alignment={"GitHub": 70.0},
            project_alignment={"GitHub": 70.0},
            discrepancies=["Discrepancy 1", "Discrepancy 2", "Discrepancy 3"],
            recommendations=[]
        )

        assert result.get_total_discrepancies_count() == 3

    def test_get_total_recommendations_count(self):
        """Test getting total recommendations count"""
        result = AlignmentResult.create_new(
            overall_score=70.0,
            skill_alignment={"GitHub": 70.0},
            experience_alignment={"GitHub": 70.0},
            project_alignment={"GitHub": 70.0},
            discrepancies=[],
            recommendations=["Rec 1", "Rec 2"]
        )

        assert result.get_total_recommendations_count() == 2

    def test_to_dict_and_from_dict(self):
        """Test serialization and deserialization"""
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
        assert "alignment_id" in result_dict
        assert "overall_score" in result_dict
        assert "skill_alignment" in result_dict
        assert "experience_alignment" in result_dict
        assert "project_alignment" in result_dict
        assert "discrepancies" in result_dict
        assert "recommendations" in result_dict
        assert "analysis_timestamp" in result_dict

        # Create from dict
        restored_result = AlignmentResult.from_dict(result_dict)
        assert restored_result.alignment_id == original_result.alignment_id
        assert restored_result.overall_score == original_result.overall_score
        assert restored_result.skill_alignment == original_result.skill_alignment
        assert restored_result.experience_alignment == original_result.experience_alignment
        assert restored_result.project_alignment == original_result.project_alignment
        assert restored_result.discrepancies == original_result.discrepancies
        assert restored_result.recommendations == original_result.recommendations

    def test_get_actionable_insights(self):
        """Test getting actionable insights"""
        result = AlignmentResult.create_new(
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

        insights = result.get_actionable_insights()
        assert len(insights) > 0
        # Should include quality level
        assert any("FAIR" in insight for insight in insights)
        # Should mention number of discrepancies
        assert any("discrepancies" in insight.lower() for insight in insights)
        # Should mention recommendations
        assert any("recommendations" in insight.lower() for insight in insights)