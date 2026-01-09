"""Profile Analyzer Service for Resume Analyzer Core"""
import os
import time
import random
from typing import Dict, List, Any, Optional, Callable
from src.models.profile_analysis import ProfileAnalysis
from src.models.improvement import ImprovementSuggestion
from src.utils.logger import get_logger


class ProfileAnalyzer:
    """Analyzes profile data with Gemini API integration for profile analysis"""

    def __init__(self, api_key: Optional[str] = None, max_retries: int = 3, base_delay: float = 1.0):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.max_retries = max_retries
        self.base_delay = base_delay  # Base delay in seconds for exponential backoff
        self.logger = get_logger("ProfileAnalyzer")

        if not self.api_key:
            self.logger.warning("GEMINI_API_KEY not set. AI features will be limited.")

    def _exponential_backoff_delay(self, attempt: int) -> float:
        """
        Calculate delay using exponential backoff with jitter.

        Args:
            attempt: Current attempt number (0-indexed)

        Returns:
            Delay in seconds
        """
        # Exponential backoff: base_delay * (2^attempt)
        delay = self.base_delay * (2 ** attempt)
        # Add jitter to prevent thundering herd
        jitter = random.uniform(0, delay * 0.1)  # Up to 10% additional random delay
        return delay + jitter

    def _with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute a function with retry logic and exponential backoff.

        Args:
            func: Function to execute
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function

        Returns:
            Result of the function call
        """
        last_exception = None

        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries - 1:  # Don't sleep on the last attempt
                    delay = self._exponential_backoff_delay(attempt)
                    print(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {delay:.2f}s...")
                    time.sleep(delay)
                else:
                    print(f"All {self.max_retries} attempts failed. Last error: {str(e)}")

        # If we get here, all retries failed
        raise last_exception

    def analyze_profile(self, profile_data: Dict[str, Any], profile_type: str) -> ProfileAnalysis:
        """
        Perform AI analysis of profile data.

        Args:
            profile_data: The profile data to analyze
            profile_type: The type of profile (LINKEDIN, GITHUB, or PORTFOLIO)

        Returns:
            ProfileAnalysis entity with analysis results
        """
        self.logger.info(f"Starting AI analysis for {profile_type} profile")

        if not self.api_key:
            self.logger.warning("GEMINI_API_KEY not set, using fallback analysis")
            # Fallback to basic analysis if API key is not available
            return self._fallback_analysis(profile_data, profile_type)

        def _attempt_analysis():
            self.logger.debug("Creating analysis prompt")
            # Create the prompt for Gemini
            prompt = self._create_analysis_prompt(profile_data, profile_type)

            self.logger.debug("Generating Gemini response")
            # Call Gemini API (in a real implementation, this would use the actual Gemini API)
            # For this implementation, we'll simulate the response
            response = self._simulate_gemini_response(profile_data, profile_type)

            self.logger.debug("Gemini response generated successfully")
            return response

        try:
            result = self._with_retry(_attempt_analysis)
            self.logger.info("Profile analysis completed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Error in profile analysis after {self.max_retries} attempts: {str(e)}")
            # Return fallback analysis if Gemini call fails
            fallback_result = self._fallback_analysis(profile_data, profile_type)
            self.logger.info("Returned fallback analysis due to error")
            return fallback_result

    def _create_analysis_prompt(self, profile_data: Dict[str, Any], profile_type: str) -> str:
        """
        Create the prompt for Gemini AI analysis.

        Args:
            profile_data: The profile data to analyze
            profile_type: The type of profile (LINKEDIN, GITHUB, or PORTFOLIO)

        Returns:
            Formatted prompt string
        """
        normalized_content = profile_data.get("normalized_content", {})

        return f"""
        Analyze the following {profile_type} profile content and provide structured feedback:

        Profile Content:
        {str(normalized_content)}

        Please provide:
        1. 3-5 key strengths of the profile
        2. 3-5 areas for improvement
        3. Specific, actionable suggestions for improvement with categories and priorities
        4. Clarity score (0-100) - how clearly the profile communicates value proposition
        5. Impact score (0-100) - how effectively the profile showcases skills and experience

        Format your response as structured JSON with keys:
        - strengths: array of strings
        - weaknesses: array of strings
        - suggestions: array of objects with keys: category, priority, suggestion_text, rationale, example, affected_section
        - clarity_score: number between 0 and 100
        - impact_score: number between 0 and 100
        """

    def _simulate_gemini_response(self, profile_data: Dict[str, Any], profile_type: str) -> ProfileAnalysis:
        """
        Simulate Gemini's response for development purposes.

        Args:
            profile_data: The profile data to analyze
            profile_type: The type of profile (LINKEDIN, GITHUB, or PORTFOLIO)

        Returns:
            Simulated AI analysis response as ProfileAnalysis
        """
        # In a real implementation, this would call the Gemini API
        # For now, we'll generate a reasonable response based on the profile content

        normalized_content = profile_data.get("normalized_content", {})
        content_str = str(normalized_content)

        strengths = []
        weaknesses = []
        suggestions = []

        # Analyze content to generate realistic feedback
        if profile_type == "LINKEDIN":
            if "headline" in normalized_content and normalized_content["headline"]:
                strengths.append("Clear and professional headline")
            else:
                weaknesses.append("Missing or weak headline")
                suggestions.append(ImprovementSuggestion.create_new(
                    category="CONTENT",
                    priority="HIGH",
                    suggestion_text="Add a compelling headline that clearly states your professional identity",
                    rationale="A strong headline helps recruiters quickly understand your value proposition",
                    example="Senior Software Engineer | Python & AI Specialist | Building scalable solutions",
                    affected_section="headline"
                ))

            if "summary" in normalized_content and len(str(normalized_content.get("summary", ""))) > 50:
                strengths.append("Good summary section with sufficient detail")
            else:
                weaknesses.append("Summary section could be more detailed")
                suggestions.append(ImprovementSuggestion.create_new(
                    category="CONTENT",
                    priority="MEDIUM",
                    suggestion_text="Expand your summary to better showcase your experience and skills",
                    rationale="A detailed summary helps establish credibility and expertise",
                    example="Currently: 'Software engineer'. Better: 'Senior software engineer with 5+ years of experience in Python, cloud architecture, and AI/ML'",
                    affected_section="summary"
                ))

        elif profile_type == "GITHUB":
            if "repositories" in normalized_content and len(normalized_content["repositories"]) > 0:
                strengths.append("Active repository presence")
                # Check for README files
                repos = normalized_content["repositories"]
                repos_with_readme = [r for r in repos if r.get("description") or r.get("readme")]
                if len(repos_with_readme) > len(repos) * 0.5:  # More than 50% have descriptions
                    strengths.append("Good repository documentation")
                else:
                    weaknesses.append("Many repositories lack proper documentation")
                    suggestions.append(ImprovementSuggestion.create_new(
                        category="CONTENT",
                        priority="MEDIUM",
                        suggestion_text="Add README files with clear descriptions to your repositories",
                        rationale="Well-documented repositories help others understand your code and skills",
                        example="Add project overview, technologies used, setup instructions, and usage examples",
                        affected_section="repositories"
                    ))
            else:
                weaknesses.append("No repositories found")

        elif profile_type == "PORTFOLIO":
            if "bio_about" in normalized_content and len(str(normalized_content.get("bio_about", ""))) > 50:
                strengths.append("Good bio/about section with sufficient detail")
            else:
                weaknesses.append("Bio/about section could be more detailed")
                suggestions.append(ImprovementSuggestion.create_new(
                    category="CONTENT",
                    priority="HIGH",
                    suggestion_text="Add a detailed bio/about section that showcases your skills and experience",
                    rationale="A strong bio helps visitors understand your expertise and value proposition",
                    example="Include your background, key skills, notable projects, and career goals",
                    affected_section="bio_about"
                ))

            if "projects" in normalized_content and len(normalized_content["projects"]) > 0:
                strengths.append("Good project showcase")
            else:
                weaknesses.append("Missing or minimal project showcase")
                suggestions.append(ImprovementSuggestion.create_new(
                    category="VISIBILITY",
                    priority="HIGH",
                    suggestion_text="Add projects section to showcase your work",
                    rationale="Projects provide concrete examples of your skills and capabilities",
                    example="Include 3-5 key projects with descriptions, technologies used, and links to code/demos",
                    affected_section="projects"
                ))

        # Default scores
        clarity_score = 75.0
        impact_score = 70.0

        # Adjust scores based on content
        if len(content_str) < 100:
            clarity_score -= 15
            impact_score -= 20
        elif len(content_str) > 500:
            clarity_score += 5

        # Section feedback
        section_feedback = {
            "content": "Content appears well-structured with relevant information",
            "formatting": "Formatting looks good for readability",
            "visibility": "Key information is visible and accessible",
            "technical": "Technical aspects are well-presented"
        }

        # Overall feedback
        overall_feedback = (
            f"The {profile_type} profile shows potential with relevant information, "
            f"but could benefit from improvements in key areas to better showcase skills and experience."
        )

        # Create and return ProfileAnalysis
        profile_analysis = ProfileAnalysis.create_new(
            profile_type=profile_type,
            strengths=strengths or ["Profile has basic structure"],
            weaknesses=weaknesses or ["Could use more detailed content"],
            suggestions=suggestions,
            clarity_score=clarity_score,
            impact_score=impact_score
        )

        return profile_analysis

    def _fallback_analysis(self, profile_data: Dict[str, Any], profile_type: str) -> ProfileAnalysis:
        """
        Provide a fallback analysis when AI service is unavailable.

        Args:
            profile_data: The profile data to analyze
            profile_type: The type of profile (LINKEDIN, GITHUB, or PORTFOLIO)

        Returns:
            Basic analysis based on simple heuristics
        """
        # Simple heuristic-based analysis
        normalized_content = profile_data.get("normalized_content", {})
        content_length = len(str(normalized_content))

        strengths = []
        weaknesses = []
        suggestions = []

        # Basic analysis based on content presence
        if content_length > 200:
            strengths.append("Profile has good amount of content")
        else:
            weaknesses.append("Profile could be more detailed")

        if profile_type == "LINKEDIN":
            strengths.append("LinkedIn profile detected")
        elif profile_type == "GITHUB":
            strengths.append("GitHub profile detected")
        elif profile_type == "PORTFOLIO":
            strengths.append("Portfolio website detected")

        # Create basic suggestions
        suggestions.append(ImprovementSuggestion.create_new(
            category="CONTENT",
            priority="MEDIUM",
            suggestion_text="Add more specific examples of your work and achievements",
            rationale="Specific examples help demonstrate your skills and impact",
            example="Instead of 'Experienced in Python', say 'Developed Python applications that improved process efficiency by 30%'",
            affected_section="all"
        ))

        # Create and return ProfileAnalysis with basic scores
        profile_analysis = ProfileAnalysis.create_new(
            profile_type=profile_type,
            strengths=strengths,
            weaknesses=weaknesses,
            suggestions=suggestions,
            clarity_score=60.0,
            impact_score=55.0
        )

        return profile_analysis

    def generate_profile_improvements(self, profile_analysis: ProfileAnalysis, profile_data: Dict[str, Any]) -> List[ImprovementSuggestion]:
        """
        Generate improvement suggestions based on profile analysis.

        Args:
            profile_analysis: The analysis result to base suggestions on
            profile_data: The original profile data

        Returns:
            List of improvement suggestions
        """
        self.logger.info(f"Generating improvement suggestions for {profile_analysis.profile_type} profile")

        if not self.api_key:
            self.logger.warning("GEMINI_API_KEY not set, using fallback suggestions")
            return self._fallback_improvements(profile_analysis, profile_data)

        def _attempt_improvement_generation():
            self.logger.debug("Generating improvement suggestions")
            # In a real implementation, this would use Gemini for more sophisticated analysis
            # For now, we'll use the suggestions already in the profile analysis
            suggestions = profile_analysis.suggestions

            # Add more suggestions based on profile type
            profile_type = profile_analysis.profile_type
            normalized_content = profile_data.get("normalized_content", {})

            # Add specific suggestions based on profile type
            if profile_type == "LINKEDIN":
                if "skills" not in normalized_content or len(normalized_content.get("skills", [])) < 5:
                    suggestions.append(ImprovementSuggestion.create_new(
                        category="CONTENT",
                        priority="HIGH",
                        suggestion_text="Add more skills to showcase your technical abilities",
                        rationale="Having more skills increases your discoverability in recruiter searches",
                        example="Add 5-10 relevant technical and soft skills",
                        affected_section="skills"
                    ))

            elif profile_type == "GITHUB":
                if "bio" not in normalized_content or not normalized_content.get("bio", "").strip():
                    suggestions.append(ImprovementSuggestion.create_new(
                        category="CONTENT",
                        priority="HIGH",
                        suggestion_text="Add a bio to your GitHub profile",
                        rationale="A bio helps others quickly understand your expertise and interests",
                        example="Add a brief description of your technical background and interests",
                        affected_section="bio"
                    ))

            elif profile_type == "PORTFOLIO":
                if "contact_visible" not in normalized_content or not normalized_content.get("contact_visible", False):
                    suggestions.append(ImprovementSuggestion.create_new(
                        category="VISIBILITY",
                        priority="HIGH",
                        suggestion_text="Make your contact information visible on your portfolio",
                        rationale="Recruiters need to be able to contact you easily",
                        example="Add a contact form or visible email address",
                        affected_section="contact"
                    ))

            self.logger.debug(f"Generated {len(suggestions)} improvement suggestions")
            return suggestions

        try:
            result = self._with_retry(_attempt_improvement_generation)
            self.logger.info(f"Improvement suggestion generation completed successfully with {len(result)} suggestions")
            return result
        except Exception as e:
            self.logger.error(f"Error generating improvement suggestions after {self.max_retries} attempts: {str(e)}")
            fallback_result = self._fallback_improvements(profile_analysis, profile_data)
            self.logger.info(f"Returned {len(fallback_result)} fallback improvement suggestions due to error")
            return fallback_result

    def _create_improvement_prompt(self, profile_analysis: ProfileAnalysis, profile_data: Dict[str, Any]) -> str:
        """
        Create the prompt for Gemini improvement suggestions.

        Args:
            profile_analysis: The analysis result to base suggestions on
            profile_data: The original profile data

        Returns:
            Formatted prompt string for improvement suggestions
        """
        normalized_content = profile_data.get("normalized_content", {})

        return f"""
        Based on the following profile analysis and data, suggest specific improvements:

        Profile Type: {profile_analysis.profile_type}
        Profile Data: {str(normalized_content)}

        Analysis Strengths: {', '.join(profile_analysis.strengths)}
        Analysis Weaknesses: {', '.join(profile_analysis.weaknesses)}

        Please suggest 5-10 specific improvements with:
        1. Category (CONTENT, FORMATTING, VISIBILITY, ALIGNMENT, TECHNICAL)
        2. Priority (HIGH, MEDIUM, LOW)
        3. Specific suggestion text
        4. Rationale for the suggestion
        5. Example of how to implement
        6. Affected section

        Return as structured data with these fields.
        """

    def _fallback_improvements(self, profile_analysis: ProfileAnalysis, profile_data: Dict[str, Any]) -> List[ImprovementSuggestion]:
        """
        Provide fallback improvement suggestions when AI service is unavailable.

        Args:
            profile_analysis: The analysis result to base suggestions on
            profile_data: The original profile data

        Returns:
            List of basic improvement suggestions
        """
        # Basic improvement suggestions based on common best practices
        basic_suggestions = [
            ImprovementSuggestion.create_new(
                category="CONTENT",
                priority="MEDIUM",
                suggestion_text="Regularly update your profile with recent projects and achievements",
                rationale="Fresh content shows you're actively developing your skills",
                example="Add your latest project or a recent learning achievement",
                affected_section="all"
            ),
            ImprovementSuggestion.create_new(
                category="VISIBILITY",
                priority="HIGH",
                suggestion_text="Ensure your contact information is easily accessible",
                rationale="Recruiters need to be able to reach out to you",
                example="Add contact information in your profile bio or dedicated contact section",
                affected_section="contact"
            ),
            ImprovementSuggestion.create_new(
                category="TECHNICAL",
                priority="MEDIUM",
                suggestion_text="Add links to your other professional profiles",
                rationale="Cross-linking helps create a complete professional presence",
                example="Add links to your LinkedIn on your GitHub, and vice versa",
                affected_section="links"
            )
        ]

        return basic_suggestions