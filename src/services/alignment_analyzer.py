"""Alignment Analyzer Service for Resume Analyzer Core"""
import re
from typing import Dict, List, Any, Tuple
from src.models.alignment_result import AlignmentResult
from src.utils.logger import get_logger


class AlignmentAnalyzer:
    """Analyzes alignment between resume and profile data with scoring"""

    def __init__(self):
        self.logger = get_logger("AlignmentAnalyzer")

        # Common skills and technologies that should be consistent across profiles
        self.common_tech_keywords = [
            # Programming languages
            "python", "javascript", "java", "typescript", "c++", "c#", "go", "rust", "php", "ruby",
            # Frameworks and libraries
            "react", "angular", "vue", "node.js", "django", "flask", "spring", "express", "fastapi",
            # Technologies and tools
            "aws", "azure", "gcp", "docker", "kubernetes", "git", "linux", "sql", "mongodb", "postgresql",
            # Skills
            "machine learning", "artificial intelligence", "data science", "devops", "agile", "scrum"
        ]

        # Common experience patterns to look for
        self.experience_patterns = [
            r"software.*engineer", r"developer", r"programmer", r"data.*scientist",
            r"full.*stack", r"front.*end", r"back.*end", r"devops", r"product.*manager"
        ]

    def analyze_alignment(
        self,
        resume_data: Dict[str, Any],
        profile_data_list: List[Dict[str, Any]]
    ) -> AlignmentResult:
        """
        Analyze alignment between resume and profile data.

        Args:
            resume_data: Dictionary containing resume analysis data
            profile_data_list: List of dictionaries containing profile data

        Returns:
            AlignmentResult entity with alignment scores and recommendations
        """
        self.logger.info(f"Starting alignment analysis between resume and {len(profile_data_list)} profiles")

        # Extract key elements from resume
        resume_skills = self._extract_skills(resume_data)
        resume_experience = self._extract_experience(resume_data)
        resume_projects = self._extract_projects(resume_data)

        # Calculate alignment scores
        skill_alignment = {}
        experience_alignment = {}
        project_alignment = {}

        all_discrepancies = []
        all_recommendations = []

        for profile_data in profile_data_list:
            platform = profile_data.get("profile_type", "Unknown")

            # Calculate skill alignment
            profile_skills = self._extract_skills_from_profile(profile_data)
            skill_score = self._calculate_skill_alignment(resume_skills, profile_skills)
            skill_alignment[platform] = skill_score

            # Calculate experience alignment
            profile_experience = self._extract_experience_from_profile(profile_data)
            experience_score = self._calculate_experience_alignment(resume_experience, profile_experience)
            experience_alignment[platform] = experience_score

            # Calculate project alignment
            profile_projects = self._extract_projects_from_profile(profile_data)
            project_score = self._calculate_project_alignment(resume_projects, profile_projects)
            project_alignment[platform] = project_score

            # Identify discrepancies
            discrepancies = self._identify_discrepancies(
                resume_skills, profile_skills,
                resume_experience, profile_experience,
                resume_projects, profile_projects
            )
            all_discrepancies.extend([f"[{platform}] {disc}" for disc in discrepancies])

            # Generate recommendations
            recommendations = self._generate_recommendations(
                resume_skills, profile_skills,
                resume_experience, profile_experience,
                resume_projects, profile_projects,
                platform
            )
            all_recommendations.extend(recommendations)

        # Calculate overall alignment score (weighted average)
        overall_score = self._calculate_overall_alignment_score(
            skill_alignment, experience_alignment, project_alignment
        )

        # Create and return alignment result
        alignment_result = AlignmentResult.create_new(
            overall_score=overall_score,
            skill_alignment=skill_alignment,
            experience_alignment=experience_alignment,
            project_alignment=project_alignment,
            discrepancies=list(set(all_discrepancies)),  # Remove duplicates
            recommendations=list(set(all_recommendations))  # Remove duplicates
        )

        self.logger.info(f"Alignment analysis completed with overall score: {overall_score}")
        return alignment_result

    def _extract_skills(self, resume_data: Dict[str, Any]) -> List[str]:
        """
        Extract skills from resume data.

        Args:
            resume_data: Dictionary containing resume analysis data

        Returns:
            List of extracted skills
        """
        skills = []

        # Extract from strengths and weaknesses
        strengths = resume_data.get("strengths", [])
        weaknesses = resume_data.get("weaknesses", [])

        for text in strengths + weaknesses:
            # Look for skills mentioned in feedback
            for keyword in self.common_tech_keywords:
                if keyword in text.lower():
                    skills.append(keyword.title())

        # Extract from section feedback
        section_feedback = resume_data.get("section_feedback", {})
        for section_name, feedback in section_feedback.items():
            for keyword in self.common_tech_keywords:
                if keyword in feedback.lower():
                    skills.append(keyword.title())

        # Remove duplicates while preserving order
        return list(dict.fromkeys(skills))

    def _extract_experience(self, resume_data: Dict[str, Any]) -> List[str]:
        """
        Extract experience highlights from resume data.

        Args:
            resume_data: Dictionary containing resume analysis data

        Returns:
            List of experience highlights
        """
        experience = []

        # Extract from section feedback, particularly experience section
        section_feedback = resume_data.get("section_feedback", {})
        for section_name, feedback in section_feedback.items():
            if "experience" in section_name.lower() or "work" in section_name.lower():
                # Extract company names, roles, or experience details
                # This is a simplified extraction - in practice, this would be more sophisticated
                experience.append(feedback[:100] + "..." if len(feedback) > 100 else feedback)

        return experience

    def _extract_projects(self, resume_data: Dict[str, Any]) -> List[str]:
        """
        Extract project information from resume data.

        Args:
            resume_data: Dictionary containing resume analysis data

        Returns:
            List of project descriptions
        """
        projects = []

        # Extract from section feedback, particularly projects section
        section_feedback = resume_data.get("section_feedback", {})
        for section_name, feedback in section_feedback.items():
            if "project" in section_name.lower():
                # Extract project descriptions
                projects.append(feedback[:100] + "..." if len(feedback) > 100 else feedback)

        return projects

    def _extract_skills_from_profile(self, profile_data: Dict[str, Any]) -> List[str]:
        """
        Extract skills from profile data.

        Args:
            profile_data: Dictionary containing profile data

        Returns:
            List of extracted skills
        """
        skills = []

        # Extract from normalized content
        normalized_content = profile_data.get("normalized_content", {})

        if "skills" in normalized_content:
            profile_skills = normalized_content["skills"]
            if isinstance(profile_skills, list):
                skills.extend(profile_skills)
            elif isinstance(profile_skills, str):
                # If skills is a string, split by common separators
                skills.extend(re.split(r'[,\n;]', profile_skills))

        # Extract from other sections that might contain skills
        for key, value in normalized_content.items():
            if isinstance(value, str) and any(keyword in key.lower() for keyword in ["skill", "tech", "language"]):
                # Look for common tech keywords in the text
                for keyword in self.common_tech_keywords:
                    if keyword in value.lower():
                        skills.append(keyword.title())

        # Remove duplicates while preserving order
        return list(dict.fromkeys([skill.strip() for skill in skills if skill.strip()]))

    def _extract_experience_from_profile(self, profile_data: Dict[str, Any]) -> List[str]:
        """
        Extract experience from profile data.

        Args:
            profile_data: Dictionary containing profile data

        Returns:
            List of experience highlights
        """
        experience = []

        normalized_content = profile_data.get("normalized_content", {})

        # Look for experience-related keys
        for key, value in normalized_content.items():
            if "experience" in key.lower() or "work" in key.lower() or "employment" in key.lower():
                if isinstance(value, list):
                    experience.extend(value)
                elif isinstance(value, str):
                    experience.append(value[:100] + "..." if len(value) > 100 else value)
                elif isinstance(value, dict):
                    # If it's a dictionary, extract relevant information
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, str):
                            experience.append(sub_value[:100] + "..." if len(sub_value) > 100 else sub_value)

        return experience

    def _extract_projects_from_profile(self, profile_data: Dict[str, Any]) -> List[str]:
        """
        Extract projects from profile data.

        Args:
            profile_data: Dictionary containing profile data

        Returns:
            List of project descriptions
        """
        projects = []

        normalized_content = profile_data.get("normalized_content", {})

        # Look for project-related keys
        if "projects" in normalized_content:
            profile_projects = normalized_content["projects"]
            if isinstance(profile_projects, list):
                for project in profile_projects:
                    if isinstance(project, dict):
                        # If project is a dict, extract name and description
                        name = project.get("name", "")
                        description = project.get("description", "")
                        project_text = f"{name}: {description}" if name and description else name or description
                        projects.append(project_text[:100] + "..." if len(project_text) > 100 else project_text)
                    elif isinstance(project, str):
                        projects.append(project[:100] + "..." if len(project) > 100 else project)
            elif isinstance(profile_projects, str):
                projects.append(profile_projects[:100] + "..." if len(profile_projects) > 100 else profile_projects)

        return projects

    def _calculate_skill_alignment(self, resume_skills: List[str], profile_skills: List[str]) -> float:
        """
        Calculate skill alignment score between resume and profile.

        Args:
            resume_skills: List of skills from resume
            profile_skills: List of skills from profile

        Returns:
            Skill alignment score (0-100)
        """
        if not resume_skills and not profile_skills:
            return 100.0  # Perfect alignment if both are empty
        if not resume_skills or not profile_skills:
            return 0.0  # No alignment if one is empty

        # Convert to lowercase for comparison
        resume_set = {skill.lower() for skill in resume_skills}
        profile_set = {skill.lower() for skill in profile_skills}

        # Calculate intersection and union
        intersection = resume_set & profile_set
        union = resume_set | profile_set

        # Jaccard similarity coefficient
        jaccard_similarity = len(intersection) / len(union) if union else 0

        # Convert to percentage (0-100)
        return jaccard_similarity * 100

    def _calculate_experience_alignment(self, resume_experience: List[str], profile_experience: List[str]) -> float:
        """
        Calculate experience alignment score between resume and profile.

        Args:
            resume_experience: List of experience highlights from resume
            profile_experience: List of experience highlights from profile

        Returns:
            Experience alignment score (0-100)
        """
        if not resume_experience and not profile_experience:
            return 100.0
        if not resume_experience or not profile_experience:
            return 0.0

        # Simple text-based alignment using common patterns
        matches = 0
        total_checks = 0

        for resume_exp in resume_experience:
            for profile_exp in profile_experience:
                # Check for common experience patterns
                for pattern in self.experience_patterns:
                    if (re.search(pattern, resume_exp, re.IGNORECASE) and
                        re.search(pattern, profile_exp, re.IGNORECASE)):
                        matches += 1
                        break
                total_checks += 1

        if total_checks == 0:
            return 0.0

        return (matches / total_checks) * 100

    def _calculate_project_alignment(self, resume_projects: List[str], profile_projects: List[str]) -> float:
        """
        Calculate project alignment score between resume and profile.

        Args:
            resume_projects: List of projects from resume
            profile_projects: List of projects from profile

        Returns:
            Project alignment score (0-100)
        """
        if not resume_projects and not profile_projects:
            return 100.0
        if not resume_projects or not profile_projects:
            return 0.0

        # Simple alignment based on common keywords
        matches = 0
        total_checks = 0

        for resume_proj in resume_projects:
            for profile_proj in profile_projects:
                # Check for common tech keywords in both project descriptions
                resume_lower = resume_proj.lower()
                profile_lower = profile_proj.lower()

                for keyword in self.common_tech_keywords:
                    if keyword in resume_lower and keyword in profile_lower:
                        matches += 1
                        break
                total_checks += 1

        if total_checks == 0:
            return 0.0

        return (matches / total_checks) * 100

    def _calculate_overall_alignment_score(
        self,
        skill_alignment: Dict[str, float],
        experience_alignment: Dict[str, float],
        project_alignment: Dict[str, float]
    ) -> float:
        """
        Calculate overall alignment score as weighted average.

        Args:
            skill_alignment: Dictionary of skill alignment scores by platform
            experience_alignment: Dictionary of experience alignment scores by platform
            project_alignment: Dictionary of project alignment scores by platform

        Returns:
            Overall alignment score (0-100)
        """
        if not skill_alignment and not experience_alignment and not project_alignment:
            return 0.0

        # Calculate average scores across all platforms
        avg_skill_score = sum(skill_alignment.values()) / len(skill_alignment) if skill_alignment else 0
        avg_experience_score = sum(experience_alignment.values()) / len(experience_alignment) if experience_alignment else 0
        avg_project_score = sum(project_alignment.values()) / len(project_alignment) if project_alignment else 0

        # Weighted average (skills: 40%, experience: 40%, projects: 20%)
        overall_score = (
            avg_skill_score * 0.4 +
            avg_experience_score * 0.4 +
            avg_project_score * 0.2
        )

        return overall_score

    def _identify_discrepancies(
        self,
        resume_skills: List[str],
        profile_skills: List[str],
        resume_experience: List[str],
        profile_experience: List[str],
        resume_projects: List[str],
        profile_projects: List[str]
    ) -> List[str]:
        """
        Identify discrepancies between resume and profile data.

        Args:
            resume_skills: Skills from resume
            profile_skills: Skills from profile
            resume_experience: Experience from resume
            profile_experience: Experience from profile
            resume_projects: Projects from resume
            profile_projects: Projects from profile

        Returns:
            List of identified discrepancies
        """
        discrepancies = []

        # Check for skills discrepancies
        resume_skills_set = {skill.lower() for skill in resume_skills}
        profile_skills_set = {skill.lower() for skill in profile_skills}

        missing_in_profile = resume_skills_set - profile_skills_set
        missing_in_resume = profile_skills_set - resume_skills_set

        if missing_in_profile:
            discrepancies.append(
                f"Skills mentioned in resume but not in profile: {', '.join(list(missing_in_profile)[:3])}{'...' if len(missing_in_profile) > 3 else ''}"
            )

        if missing_in_resume:
            discrepancies.append(
                f"Skills mentioned in profile but not in resume: {', '.join(list(missing_in_resume)[:3])}{'...' if len(missing_in_resume) > 3 else ''}"
            )

        # Check for experience discrepancies
        if not resume_experience and profile_experience:
            discrepancies.append("Resume has no experience section but profile does")
        elif resume_experience and not profile_experience:
            discrepancies.append("Profile has no experience section but resume does")

        # Check for project discrepancies
        if not resume_projects and profile_projects:
            discrepancies.append("Resume has no projects section but profile does")
        elif resume_projects and not profile_projects:
            discrepancies.append("Profile has no projects section but resume does")

        return discrepancies

    def _generate_recommendations(
        self,
        resume_skills: List[str],
        profile_skills: List[str],
        resume_experience: List[str],
        profile_experience: List[str],
        resume_projects: List[str],
        profile_projects: List[str],
        platform: str
    ) -> List[str]:
        """
        Generate recommendations to improve alignment.

        Args:
            resume_skills: Skills from resume
            profile_skills: Skills from profile
            resume_experience: Experience from resume
            profile_experience: Experience from profile
            resume_projects: Projects from resume
            profile_projects: Projects from profile
            platform: Profile platform name

        Returns:
            List of recommendations
        """
        recommendations = []

        # Skills alignment recommendations
        resume_skills_set = {skill.lower() for skill in resume_skills}
        profile_skills_set = {skill.lower() for skill in profile_skills}

        missing_in_profile = resume_skills_set - profile_skills_set
        missing_in_resume = profile_skills_set - resume_skills_set

        if missing_in_profile:
            recommendations.append(
                f"For better alignment with your resume, add these skills to your {platform} profile: {', '.join(list(missing_in_profile)[:3])}"
            )

        if missing_in_resume:
            recommendations.append(
                f"To highlight your {platform} skills in your resume, add these skills: {', '.join(list(missing_in_resume)[:3])}"
            )

        # Experience alignment recommendations
        if not resume_experience and profile_experience:
            recommendations.append(
                f"Consider adding experience details to your resume to match your {platform} profile"
            )
        elif resume_experience and not profile_experience:
            recommendations.append(
                f"Consider adding experience details to your {platform} profile to match your resume"
            )

        # Project alignment recommendations
        if not resume_projects and profile_projects:
            recommendations.append(
                f"Consider adding project details to your resume to match your {platform} profile"
            )
        elif resume_projects and not profile_projects:
            recommendations.append(
                f"Consider adding project details to your {platform} profile to match your resume"
            )

        return recommendations

    def calculate_role_alignment_score(
        self,
        resume_data: Dict[str, Any],
        profile_data_list: List[Dict[str, Any]],
        target_role: str
    ) -> float:
        """
        Calculate how well resume and profiles align with a target role.

        Args:
            resume_data: Resume analysis data
            profile_data_list: List of profile data
            target_role: Target role to align with

        Returns:
            Role alignment score (0-100)
        """
        # Extract key elements
        resume_skills = self._extract_skills(resume_data)
        all_profile_skills = []
        for profile_data in profile_data_list:
            all_profile_skills.extend(self._extract_skills_from_profile(profile_data))

        # Combine all skills
        all_skills = list(set(resume_skills + all_profile_skills))

        # Calculate how well skills match the target role
        role_keywords = self._get_role_keywords(target_role.lower())
        matching_skills = [skill for skill in all_skills if skill.lower() in role_keywords]

        if not role_keywords:
            return 50.0  # Neutral score if we can't determine role keywords

        alignment_score = (len(matching_skills) / len(role_keywords)) * 100
        return min(100.0, alignment_score)  # Cap at 100%

    def _get_role_keywords(self, role: str) -> List[str]:
        """
        Get relevant keywords for a target role.

        Args:
            role: Target role name

        Returns:
            List of relevant keywords
        """
        role_keywords_map = {
            "software engineer": ["python", "javascript", "java", "react", "node.js", "api", "testing", "agile"],
            "data scientist": ["python", "r", "sql", "machine learning", "statistics", "pandas", "numpy", "visualization"],
            "product manager": ["product", "strategy", "analytics", "user research", "agile", "roadmap", "stakeholders"],
            "devops engineer": ["docker", "kubernetes", "aws", "ci/cd", "linux", "monitoring", "automation"],
            "frontend developer": ["javascript", "react", "html", "css", "typescript", "responsive", "ux"],
            "backend developer": ["python", "java", "node.js", "api", "database", "scalability", "microservices"]
        }

        return role_keywords_map.get(role, self.common_tech_keywords)