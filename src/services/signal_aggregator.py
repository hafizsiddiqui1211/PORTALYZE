"""Signal aggregation service for job role recommender"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import logging
from ..models.profile_signals import ProfileSignals, ResumeSignals, ProfileSignalsData, ExperienceSummary
from ..models.analysis import AnalysisResult
from ..utils.anonymizer import get_anonymizer
from ..services.consent_manager import get_consent_manager


class SignalAggregator:
    """Aggregates signals from resume analysis, LinkedIn, GitHub, and portfolio"""

    def __init__(self):
        self.anonymizer = get_anonymizer()
        self.consent_manager = get_consent_manager()
        self.logger = logging.getLogger(__name__)

    def aggregate_signals(
        self,
        resume_analysis: Union[Dict[str, Any], 'AnalysisResult'],
        profile_analyses: List[Dict[str, Any]],
        session_id: str,
        anonymize_data: bool = True,
        require_consent: bool = True
    ) -> ProfileSignals:
        """
        Aggregate signals from resume and profile analyses into a unified ProfileSignals object.

        Args:
            resume_analysis: Analysis result from resume processing (dictionary or AnalysisResult object)
            profile_analyses: List of analysis results from profile processing (LinkedIn, GitHub, portfolio)
            session_id: Session identifier for tracking
            anonymize_data: Whether to anonymize PII before aggregation
            require_consent: Whether to check for consent before processing

        Returns:
            ProfileSignals: Aggregated signals from all sources
        """
        from src.models.analysis import AnalysisResult

        self.logger.info(f"Starting signal aggregation for session {session_id} with {len(profile_analyses)} profile analyses")

        # Check for consent if required
        if require_consent:
            consent_granted = self.consent_manager.has_consent(session_id)
            if not consent_granted:
                self.logger.warning(f"Consent not granted for session {session_id}, attempting to get consent")
                # In a real implementation, you might want to raise an exception or return a default object
                # For now, we'll log and continue (in production, you should handle this differently)
                self.logger.info(f"Processing without explicit consent for session {session_id} - this should be handled based on your privacy policy")

        # Convert AnalysisResult object to dictionary if needed
        if isinstance(resume_analysis, AnalysisResult):
            resume_analysis_dict = {
                'analysis_id': resume_analysis.analysis_id,
                'resume_id': resume_analysis.resume_id,
                'ats_score': resume_analysis.ats_score,
                'strengths': resume_analysis.strengths,
                'weaknesses': resume_analysis.weaknesses,
                'section_feedback': resume_analysis.section_feedback,
                'overall_feedback': resume_analysis.overall_feedback,
                'confidence_level': resume_analysis.confidence_level,
                'analysis_timestamp': resume_analysis.analysis_timestamp
            }
        else:
            resume_analysis_dict = resume_analysis

        # Extract resume signals
        resume_signals = self._extract_resume_signals(resume_analysis_dict)
        self.logger.debug(f"Extracted resume signals with {len(resume_signals.skills)} skills")

        # Extract profile signals from all profile analyses
        profile_signals = self._extract_profile_signals(profile_analyses)
        self.logger.debug(f"Extracted profile signals with {len(profile_signals.linkedin_summary.get('skills', []))} LinkedIn skills")

        # Aggregate skills from all sources
        aggregated_skills = self._aggregate_skills(resume_signals, profile_signals)
        self.logger.debug(f"Aggregated {len(aggregated_skills)} unique skills from all sources")

        # Create experience summary
        experience_summary = self._create_experience_summary(resume_signals, profile_signals)
        self.logger.debug(f"Created experience summary with {experience_summary.total_years} years of experience")

        # Create project highlights
        project_highlights = self._create_project_highlights(resume_analysis_dict, profile_analyses)
        self.logger.debug(f"Created {len(project_highlights)} project highlights")

        # Create the ProfileSignals object
        signals_id = f"signals_{session_id}_{int(datetime.now().timestamp())}"

        profile_signals_obj = ProfileSignals(
            signals_id=signals_id,
            resume_signals=resume_signals.dict(),
            profile_signals=profile_signals.dict(),
            aggregated_skills=aggregated_skills,
            experience_summary=experience_summary.dict(),
            project_highlights=project_highlights
        )

        # Anonymize if requested
        if anonymize_data:
            self.logger.info("Applying anonymization to profile signals")
            profile_signals_obj = self._anonymize_signals(profile_signals_obj)

        # Store processed data with consent management
        if require_consent:
            self.consent_manager.store_data_with_consent(
                session_id=session_id,
                data_type="profile_signals",
                data=profile_signals_obj.dict(),
                retention_hours=24
            )

        self.logger.info(f"Completed signal aggregation with {len(profile_signals_obj.aggregated_skills)} aggregated skills")
        return profile_signals_obj

    def _extract_resume_signals(self, resume_analysis: Union[Dict[str, Any], AnalysisResult]) -> ResumeSignals:
        """Extract signals from resume analysis"""
        # Extract skills from strengths and weaknesses
        skills = []

        # Handle both dictionary and AnalysisResult object
        if isinstance(resume_analysis, AnalysisResult):
            strengths = resume_analysis.strengths
            section_feedback = resume_analysis.section_feedback
            text_content = str(resume_analysis.overall_feedback)  # Use overall feedback as text content if available
        else:  # Dictionary format
            strengths = resume_analysis.get('strengths', [])
            section_feedback = resume_analysis.get('section_feedback', {})
            text_content = resume_analysis.get('text_content', '')

        if strengths:
            for strength in strengths:
                # Simple extraction - in a real implementation, you'd use NLP to extract skills
                if 'skills' in str(strength).lower():
                    skills.extend([s.strip() for s in str(strength).split() if len(s) > 2])

        # Extract more skills from section feedback
        if section_feedback:
            for section, feedback in section_feedback.items():
                if 'skills' in str(section).lower() or 'technical' in str(feedback).lower():
                    # Extract skills mentioned in feedback
                    pass  # Simplified for now

        # Get experience years from resume
        experience_years = 0.0
        if text_content:
            # In a real implementation, you'd use NLP to extract experience years
            pass

        # Extract job titles
        job_titles = []
        if text_content:
            # In a real implementation, you'd extract job titles
            pass

        # Extract industries
        industries = []
        if text_content:
            # In a real implementation, you'd extract industries
            pass

        # Extract education
        education = []
        if text_content:
            # In a real implementation, you'd extract education
            pass

        # Extract certifications
        certifications = []
        if text_content:
            # In a real implementation, you'd extract certifications
            pass

        return ResumeSignals(
            skills=skills,
            experience_years=experience_years,
            job_titles=job_titles,
            industries=industries,
            education=education,
            certifications=certifications
        )

    def _extract_profile_signals(self, profile_analyses: List[Dict[str, Any]]) -> ProfileSignalsData:
        """Extract signals from profile analyses"""
        github_activity = {}
        linkedin_summary = {}
        portfolio_projects = []
        social_signals = {}

        for profile_analysis in profile_analyses:
            profile_type = profile_analysis.get('profile_type', '').upper()

            if profile_type == 'GITHUB':
                # Extract GitHub activity signals
                github_activity = self._extract_github_signals(profile_analysis)
            elif profile_type == 'LINKEDIN':
                # Extract LinkedIn summary signals
                linkedin_summary = self._extract_linkedin_signals(profile_analysis)
            elif profile_type == 'PORTFOLIO':
                # Extract portfolio project signals
                portfolio_projects = self._extract_portfolio_signals(profile_analysis)

        # Calculate social signals based on profile data
        social_signals = self._calculate_social_signals(
            github_activity, linkedin_summary, portfolio_projects
        )

        return ProfileSignalsData(
            github_activity=github_activity,
            linkedin_summary=linkedin_summary,
            portfolio_projects=portfolio_projects,
            social_signals=social_signals
        )

    def _extract_github_signals(self, github_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract signals from GitHub profile analysis"""
        # This would typically come from GitHub profile data
        # For now, returning a basic structure
        return {
            'total_commits': github_analysis.get('total_commits', 0),
            'repositories': github_analysis.get('repositories', 0),
            'stars_received': github_analysis.get('stars_received', 0),
            'recent_activity': github_analysis.get('recent_activity', False),
            'top_languages': github_analysis.get('top_languages', []),
            'contributions': github_analysis.get('contributions', 0)
        }

    def _extract_linkedin_signals(self, linkedin_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract signals from LinkedIn profile analysis"""
        # This would typically come from LinkedIn profile data
        # For now, returning a basic structure
        return {
            'headline': linkedin_analysis.get('headline', ''),
            'summary': linkedin_analysis.get('summary', ''),
            'connections': linkedin_analysis.get('connections', 0),
            'experience': linkedin_analysis.get('experience', []),
            'skills': linkedin_analysis.get('skills', [])
        }

    def _extract_portfolio_signals(self, portfolio_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract signals from portfolio website analysis"""
        # This would typically come from portfolio website data
        # For now, returning a basic structure
        return portfolio_analysis.get('projects', [])

    def _calculate_social_signals(
        self,
        github_activity: Dict[str, Any],
        linkedin_summary: Dict[str, Any],
        portfolio_projects: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate overall social signals from profile data"""
        activity_level = 'LOW'
        if github_activity.get('recent_activity', False) or len(portfolio_projects) > 0:
            activity_level = 'MEDIUM'
        if github_activity.get('recent_activity', False) and len(portfolio_projects) > 0:
            activity_level = 'HIGH'

        professional_network = 'SMALL'
        if linkedin_summary.get('connections', 0) > 500:
            professional_network = 'LARGE'
        elif linkedin_summary.get('connections', 0) > 100:
            professional_network = 'MEDIUM'

        technical_recognition = 'LOW'
        if github_activity.get('stars_received', 0) > 10:
            technical_recognition = 'GOOD'
        if github_activity.get('stars_received', 0) > 50:
            technical_recognition = 'EXCELLENT'

        return {
            'activity_level': activity_level,
            'professional_network': professional_network,
            'technical_recognition': technical_recognition
        }

    def _aggregate_skills(
        self,
        resume_signals: ResumeSignals,
        profile_signals: ProfileSignalsData
    ) -> List[str]:
        """Aggregate skills from resume and profile signals"""
        all_skills = set()

        # Add resume skills
        all_skills.update(resume_signals.skills)

        # Add skills from LinkedIn
        linkedin_skills = profile_signals.linkedin_summary.get('skills', [])
        all_skills.update(linkedin_skills)

        # Add skills from portfolio projects
        for project in profile_signals.portfolio_projects:
            if 'technologies' in project:
                all_skills.update(project['technologies'])

        # Add skills from GitHub
        github_skills = profile_signals.github_activity.get('top_languages', [])
        all_skills.update(github_skills)

        # Normalize skills (remove duplicates, normalize case, etc.)
        normalized_skills = list(set(skill.lower().strip() for skill in all_skills if skill))

        # Return skills in original case where possible
        original_case_skills = []
        skill_case_map = {}

        # Map lowercase to original case from resume signals first
        for skill in resume_signals.skills:
            skill_case_map[skill.lower()] = skill

        # Then from profile signals
        for skill in all_skills:
            if skill.lower() not in skill_case_map:
                skill_case_map[skill.lower()] = skill

        # Build final list in original case
        for skill_lower in normalized_skills:
            original_case_skills.append(skill_case_map[skill_lower])

        return original_case_skills

    def normalize_skill_strength(self, skill: str, source_confidence: float,
                               frequency: int, validation_sources: int) -> float:
        """
        Calculate normalized strength for a skill based on multiple factors.

        Args:
            skill: The skill name
            source_confidence: Confidence from the source (0.0-1.0)
            frequency: How many times the skill appears
            validation_sources: How many different sources validate this skill

        Returns:
            float: Normalized strength (0.0-1.0)
        """
        # Base confidence from source
        strength = source_confidence

        # Boost for frequency (capped)
        frequency_boost = min(frequency * 0.1, 0.2)  # Max 0.2 boost for frequency
        strength += frequency_boost

        # Boost for multiple validation sources
        source_boost = min((validation_sources - 1) * 0.15, 0.3)  # Max 0.3 boost for sources
        strength += source_boost

        # Cap at 1.0
        return min(strength, 1.0)

    def calculate_validation_strength(self, skill: str, profile_signals: ProfileSignalsData) -> float:
        """
        Calculate validation strength for a skill across different profile signals.

        Args:
            skill: The skill to validate
            profile_signals: Profile signals containing the skill data

        Returns:
            float: Validation strength (0.0-1.0)
        """
        validation_count = 0
        total_sources = 0

        # Check LinkedIn skills
        total_sources += 1
        if skill.lower() in [s.lower() for s in profile_signals.linkedin_summary.get('skills', [])]:
            validation_count += 1

        # Check GitHub top languages
        total_sources += 1
        if skill.lower() in [s.lower() for s in profile_signals.github_activity.get('top_languages', [])]:
            validation_count += 1

        # Check portfolio project technologies
        total_sources += 1
        for project in profile_signals.portfolio_projects:
            if 'technologies' in project:
                if skill.lower() in [s.lower() for s in project['technologies']]:
                    validation_count += 1
                    break  # Count only once per project set

        # Calculate strength based on validation ratio
        if total_sources == 0:
            return 0.0

        validation_ratio = validation_count / total_sources
        # Apply a logarithmic scaling to prevent overconfidence
        strength = min(validation_ratio * 1.2, 1.0)  # Slightly boost for cross-validation

        return strength

    def _create_experience_summary(
        self,
        resume_signals: ResumeSignals,
        profile_signals: ProfileSignalsData
    ) -> ExperienceSummary:
        """Create an experience summary from resume and profile signals"""
        # Calculate total years of experience
        total_years = resume_signals.experience_years

        # Extract domains from job titles and portfolio projects
        domains = set()
        for title in resume_signals.job_titles:
            title_lower = title.lower()
            if any(domain in title_lower for domain in ['web', 'frontend', 'backend', 'fullstack']):
                domains.add('Web Development')
            if any(domain in title_lower for domain in ['data', 'analytics', 'ml', 'ai', 'machine learning']):
                domains.add('Data/AI')
            if any(domain in title_lower for domain in ['cloud', 'devops', 'infrastructure', 'platform']):
                domains.add('Cloud/DevOps')
            if any(domain in title_lower for domain in ['mobile', 'ios', 'android']):
                domains.add('Mobile Development')
            if any(domain in title_lower for domain in ['security', 'cybersecurity', 'infosec']):
                domains.add('Security')

        # Add domains from portfolio projects
        for project in profile_signals.portfolio_projects:
            if 'technologies' in project:
                techs = [t.lower() for t in project['technologies']]
                if any(t in techs for t in ['react', 'javascript', 'html', 'css', 'vue', 'angular']):
                    domains.add('Web Development')
                if any(t in techs for t in ['python', 'r', 'sql', 'pandas', 'tensorflow', 'pytorch']):
                    domains.add('Data/AI')
                if any(t in techs for t in ['aws', 'azure', 'gcp', 'docker', 'kubernetes']):
                    domains.add('Cloud/DevOps')
                if any(t in techs for t in ['swift', 'kotlin', 'flutter', 'react native']):
                    domains.add('Mobile Development')
                if any(t in techs for t in ['cryptography', 'encryption', 'security']):
                    domains.add('Security')

        # Extract leadership indicators from job titles
        leadership_indicators = []
        for title in resume_signals.job_titles:
            title_lower = title.lower()
            if any(indicator in title_lower for indicator in ['lead', 'senior', 'manager', 'director', 'head', 'principal', 'architect']):
                leadership_indicators.append(title)

        # Extract leadership indicators from GitHub activity (contributions, stars, etc.)
        github_activity = profile_signals.github_activity
        if github_activity.get('total_commits', 0) > 500 or github_activity.get('stars_received', 0) > 20:
            leadership_indicators.append('Significant Technical Contributions')

        # Extract leadership indicators from portfolio projects
        for project in profile_signals.portfolio_projects:
            if project.get('role', '').lower() in ['lead developer', 'technical lead', 'architect', 'creator']:
                leadership_indicators.append(f"Lead on {project.get('name', 'project')}")

        # Extract technology stack
        technology_stack = list(set(resume_signals.skills + profile_signals.github_activity.get('top_languages', [])))

        # Extract leadership indicators from LinkedIn summary
        linkedin_summary = profile_signals.linkedin_summary
        if 'lead' in linkedin_summary.get('summary', '').lower():
            leadership_indicators.append('Team Leadership Mentioned')

        # Create experience summary with additional details
        return ExperienceSummary(
            total_years=total_years,
            domains=list(domains),
            leadership_indicators=list(set(leadership_indicators)),  # Remove duplicates
            technology_stack=technology_stack
        )

    def extract_experience_summary_from_text(self, text: str) -> Dict[str, Any]:
        """
        Extract experience-related information from text content.

        Args:
            text: Text content to analyze for experience information

        Returns:
            Dict with extracted experience information
        """
        import re
        from datetime import datetime

        # Look for year ranges in text (e.g., "2020-2023", "2020-present")
        year_pattern = r'(?:\b|from\s)(\d{4})(?:\s*[-–—]\s*(\d{4}|present))?\b'
        year_matches = re.findall(year_pattern, text, re.IGNORECASE)

        # Calculate years of experience based on date ranges
        years_of_experience = 0.0
        if year_matches:
            for start_year, end_year in year_matches:
                start = int(start_year)
                if end_year and end_year.lower() != 'present':
                    end = int(end_year)
                else:
                    end = datetime.now().year
                years_of_experience = max(years_of_experience, end - start)

        # Look for experience keywords
        experience_keywords = [
            r'(\d+)\s*years?\s*of\s*experience',
            r'(\d+)\s*years?\s*experience',
            r'experience\s*of\s*(\d+)\s*years?',
            r'(\d+)\s*yrs?\s*experience'
        ]

        for pattern in experience_keywords:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                years_from_text = float(match.group(1))
                years_of_experience = max(years_of_experience, years_from_text)

        # Extract domains from text
        domain_keywords = {
            'Web Development': [r'web', r'frontend', r'backend', r'full[ -]?stack', r'javascript', r'react', r'angular'],
            'Data/AI': [r'data', r'analytic', r'machine[ -]?learning', r'artificial[ -]?intelligence', r'python', r'r', r'sql'],
            'Cloud/DevOps': [r'cloud', r'aws', r'azure', r'gcp', r'devops', r'docker', r'kubernetes'],
            'Mobile Development': [r'mobile', r'ios', r'android', r'swift', r'kotlin'],
            'Security': [r'security', r'cyber', r'infosec', r'encryption']
        }

        domains = []
        for domain, keywords in domain_keywords.items():
            for keyword in keywords:
                if re.search(keyword, text, re.IGNORECASE):
                    domains.append(domain)
                    break

        return {
            'years_of_experience': years_of_experience,
            'domains': list(set(domains))
        }

    def _create_project_highlights(
        self,
        resume_analysis: Union[Dict[str, Any], 'AnalysisResult'],
        profile_analyses: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create project highlights from resume and profile data"""
        project_highlights = []

        # Add projects from portfolio
        for profile_analysis in profile_analyses:
            if profile_analysis.get('profile_type', '').upper() == 'PORTFOLIO':
                projects = profile_analysis.get('projects', [])
                for project in projects:
                    project_highlights.append({
                        'name': project.get('name', 'Unknown Project'),
                        'technologies': project.get('technologies', []),
                        'description': project.get('description', ''),
                        'impact': project.get('impact', 'Unknown impact'),
                        'role': project.get('role', 'Contributor')
                    })

        # Add projects from resume (simplified)
        # Handle both dictionary and AnalysisResult object
        has_text_content = False
        if isinstance(resume_analysis, AnalysisResult):
            # For AnalysisResult object, check if it has relevant content
            has_text_content = bool(resume_analysis.overall_feedback) or bool(resume_analysis.section_feedback)
        else:  # Dictionary format
            has_text_content = 'text_content' in resume_analysis

        if has_text_content:
            # In a real implementation, you'd extract projects from resume text
            pass

        return project_highlights

    def _anonymize_signals(self, signals: ProfileSignals) -> ProfileSignals:
        """Anonymize PII in the signals"""
        # Convert to dict for processing
        signals_dict = signals.dict()

        # Anonymize text fields
        if 'profile_signals' in signals_dict:
            profile_signals = signals_dict['profile_signals']
            if 'linkedin_summary' in profile_signals:
                linkedin_summary = profile_signals['linkedin_summary']
                if 'summary' in linkedin_summary:
                    linkedin_summary['summary'] = self.anonymizer.anonymize_text(linkedin_summary['summary'])
                if 'headline' in linkedin_summary:
                    linkedin_summary['headline'] = self.anonymizer.anonymize_text(linkedin_summary['headline'])

        # Reconstruct the ProfileSignals object
        return ProfileSignals(**signals_dict)


# Global signal aggregator instance
signal_aggregator = SignalAggregator()


def get_signal_aggregator() -> SignalAggregator:
    """Get the global signal aggregator instance"""
    return signal_aggregator