"""Keyword analysis service for Resume Analyzer Core"""
import json
import os
import re
from typing import List, Dict, Tuple, Set
from src.models.suggestions import KeywordSuggestion


class KeywordAnalyzer:
    """Analyzes resume content to identify relevant keywords and gaps"""

    def __init__(self):
        # Load keyword mappings from JSON file
        self.keyword_mappings = self._load_keyword_mappings()

        # Extract role-specific keyword databases
        self.role_keywords = self._extract_role_keywords()

        # Extract keyword categories
        self.keyword_categories = self._extract_keyword_categories()

    def _load_keyword_mappings(self) -> Dict:
        """Load keyword mappings from the JSON file."""
        # Define the path to the keyword mappings file
        mappings_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                     "data", "templates", "keyword_mappings.json")

        try:
            with open(mappings_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # If the file doesn't exist, return default mappings
            print(f"Warning: keyword_mappings.json not found at {mappings_path}")
            return self._get_default_keyword_mappings()

    def _get_default_keyword_mappings(self) -> Dict:
        """Return default keyword mappings if JSON file is not available."""
        return {
            "software_engineering": {
                "role_keywords": [
                    "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust", "Ruby", "PHP",
                    "React", "Angular", "Vue", "Node.js", "Express", "Django", "Flask", "Spring", "FastAPI",
                    "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
                    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins", "CI/CD", "Git", "Linux",
                    "REST", "API", "Microservices", "Agile", "Scrum", "Jira", "TDD", "BDD"
                ],
                "keyword_categories": {
                    "Technical": ["Python", "JavaScript", "Java", "C++", "React", "Angular", "Node.js", "AWS", "Docker", "Kubernetes",
                        "SQL", "MongoDB", "PostgreSQL", "Git", "Linux", "REST", "API", "Machine Learning", "AI", "Data Science"],
                    "Programming Language": ["Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust", "Ruby", "PHP", "R", "Scala"],
                    "Framework": ["React", "Angular", "Vue", "Node.js", "Express", "Django", "Flask", "Spring", "FastAPI", "TensorFlow",
                        "PyTorch", "Keras", "Bootstrap", "jQuery"],
                    "Tool": ["Docker", "Kubernetes", "Jenkins", "Git", "AWS", "Azure", "GCP", "Jira", "Confluence", "Terraform",
                        "Ansible", "Chef", "Puppet", "Sass", "Less", "Webpack", "Babel"],
                    "Platform": ["AWS", "Azure", "GCP", "EC2", "S3", "Lambda", "IAM", "VPC", "EKS", "AKS", "GKE", "Heroku", "Netlify"],
                    "Soft Skill": ["Leadership", "Communication", "Teamwork", "Problem Solving", "Critical Thinking", "Adaptability",
                        "Collaboration", "Project Management", "Time Management", "Negotiation", "Conflict Resolution"],
                    "IndustrySpecific": ["Fintech", "EdTech", "Healthcare", "E-commerce", "SaaS", "B2B", "B2C", "Agile", "Scrum", "Kanban"]
                }
            },
            "data_science": {
                "role_keywords": [
                    "Python", "R", "SQL", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Keras", "pandas", "numpy",
                    "scikit-learn", "Jupyter", "RStudio", "Tableau", "PowerBI", "Excel", "SAS", "SPSS", "statsmodels", "plotly",
                    "dplyr", "ggplot2", "Data Mining", "NLP", "Computer Vision", "Big Data", "Hadoop", "Spark", "Statistical Modeling"
                ],
                "keyword_categories": {
                    "Technical": ["Python", "R", "SQL", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Keras", "pandas", "numpy"],
                    "Programming Language": ["Python", "R", "SQL", "SAS", "SPSS"],
                    "Framework": ["TensorFlow", "PyTorch", "Keras", "scikit-learn", "pandas", "numpy"],
                    "Tool": ["Jupyter", "RStudio", "Tableau", "PowerBI", "Excel", "SAS", "SPSS"],
                    "Soft Skill": ["Data Analysis", "Statistical Analysis", "Problem Solving", "Critical Thinking", "Communication"]
                }
            },
            "common_skills": [
                "Communication", "Leadership", "Teamwork", "Problem Solving", "Critical Thinking", "Project Management",
                "Time Management", "Adaptability", "Creativity", "Attention to Detail", "Analytical Skills"
            ]
        }

    def _extract_role_keywords(self) -> Dict[str, List[str]]:
        """Extract role-specific keywords from the loaded mappings."""
        role_keywords = {}

        # Map role names from the JSON to the expected format
        role_mapping = {
            "software_engineering": "Software Engineer",
            "data_science": "Data Scientist",
            "product_management": "Product Manager",
            "devops_engineering": "DevOps Engineer",
            "marketing": "Marketing Specialist"
        }

        for json_key, role_name in role_mapping.items():
            if json_key in self.keyword_mappings:
                if "role_keywords" in self.keyword_mappings[json_key]:
                    role_keywords[role_name] = self.keyword_mappings[json_key]["role_keywords"]

        # Add default if no mappings were found
        if not role_keywords:
            role_keywords["Software Engineer"] = self._get_default_keyword_mappings()["software_engineering"]["role_keywords"]

        return role_keywords

    def _extract_keyword_categories(self) -> Dict[str, List[str]]:
        """Extract keyword categories from the loaded mappings."""
        all_categories = {}

        # Extract categories from each role that has them
        for role_key, role_data in self.keyword_mappings.items():
            if isinstance(role_data, dict) and "keyword_categories" in role_data:
                for category, keywords in role_data["keyword_categories"].items():
                    if category not in all_categories:
                        all_categories[category] = []
                    all_categories[category].extend(keywords)

        # Remove duplicates while preserving order
        for category in all_categories:
            seen = set()
            unique_keywords = []
            for keyword in all_categories[category]:
                if keyword not in seen:
                    seen.add(keyword)
                    unique_keywords.append(keyword)
            all_categories[category] = unique_keywords

        # Add common skills if they exist
        if "common_skills" in self.keyword_mappings:
            if "Common Skills" not in all_categories:
                all_categories["Common Skills"] = []
            all_categories["Common Skills"].extend(self.keyword_mappings["common_skills"])

        # Add default categories if none were found
        if not all_categories:
            default_mappings = self._get_default_keyword_mappings()
            all_categories = default_mappings["software_engineering"]["keyword_categories"]

        return all_categories

    def get_relevant_keywords(self, resume_text: str, target_role: str = "Software Engineer") -> List[str]:
        """
        Extract relevant keywords from resume text based on target role.

        Args:
            resume_text: The text content of the resume
            target_role: The target role to focus keyword extraction on

        Returns:
            List of relevant keywords found in the resume
        """
        if not resume_text:
            return []

        # Get role-specific keywords
        role_keywords = self.role_keywords.get(target_role, self.role_keywords["Software Engineer"])

        # Find keywords in resume text (case-insensitive)
        found_keywords = []
        text_lower = resume_text.lower()

        for keyword in role_keywords:
            # Use word boundaries to avoid partial matches
            if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text_lower):
                found_keywords.append(keyword)

        return found_keywords

    def identify_keyword_gaps(self, resume_text: str, required_keywords: List[str]) -> List[str]:
        """
        Identify which required keywords are missing from the resume.

        Args:
            resume_text: The text content of the resume
            required_keywords: List of keywords that should be present

        Returns:
            List of missing keywords
        """
        if not resume_text:
            return required_keywords

        missing_keywords = []
        text_lower = resume_text.lower()

        for keyword in required_keywords:
            # Use word boundaries to avoid partial matches
            if not re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text_lower):
                missing_keywords.append(keyword)

        return missing_keywords

    def calculate_keyword_relevance(self, resume_text: str, keywords: List[str]) -> List[Tuple[str, float]]:
        """
        Calculate relevance scores for each keyword based on presence and frequency in resume.

        Args:
            resume_text: The text content of the resume
            keywords: List of keywords to calculate relevance for

        Returns:
            List of tuples (keyword, relevance_score) sorted by relevance
        """
        if not resume_text:
            return [(kw, 0.0) for kw in keywords]

        relevance_scores = []
        text_lower = resume_text.lower()

        # Create a text words set with more flexible matching (handle punctuation)
        text_words = set()
        # Split by whitespace and common punctuation to get clean words
        import re
        text_word_matches = re.findall(r'\b\w+\b', text_lower)
        text_words = set(text_word_matches)

        for keyword in keywords:
            score = 0.0
            keyword_lower = keyword.lower()

            # Check for exact word match (more flexible)
            if keyword_lower in text_words:
                score += 0.5  # Base score for presence

            # Check for the keyword in the full text (handles cases with punctuation)
            if keyword_lower in text_lower:
                score += 0.3  # Additional score for presence in text

            # Check for regex-based word boundary match (backup method)
            if re.search(r'\b' + re.escape(keyword_lower) + r'\b', text_lower):
                # Don't double count if it was already matched above
                if keyword_lower not in text_words:
                    score += 0.3  # Additional score for exact match

            # Boost score for technical keywords if they appear in the text
            # Use a more flexible check for technical keywords
            is_technical = False
            for category, cat_keywords in self.keyword_categories.items():
                if keyword in cat_keywords:
                    is_technical = True
                    break

            if is_technical and keyword_lower in text_lower:
                score += 0.2

            # Ensure score doesn't exceed 1.0
            score = min(1.0, score)

            # Ensure minimum score of 0.0
            score = max(0.0, score)

            relevance_scores.append((keyword, score))

        # Sort by relevance score (descending)
        return sorted(relevance_scores, key=lambda x: x[1], reverse=True)

    def get_role_specific_keywords(self, target_role: str) -> List[str]:
        """
        Get role-specific keywords for a target role.

        Args:
            target_role: The target role to get keywords for

        Returns:
            List of role-specific keywords
        """
        return self.role_keywords.get(target_role, self.role_keywords["Software Engineer"])

    def categorize_keyword(self, keyword: str) -> str:
        """
        Categorize a keyword into one of the predefined categories.
        Maps to valid categories: Technical, SoftSkill, IndustrySpecific

        Args:
            keyword: The keyword to categorize

        Returns:
            The category of the keyword (mapped to valid categories)
        """
        for category, keywords in self.keyword_categories.items():
            if keyword in keywords:
                # Map dynamic categories to valid ones
                if "Programming" in category or "Language" in category:
                    return "Technical"
                elif "Framework" in category:
                    return "Technical"
                elif "Tool" in category:
                    return "Technical"
                elif "Database" in category:
                    return "Technical"
                elif "Methodology" in category or "Process" in category:
                    return "IndustrySpecific"
                elif "Soft" in category:
                    return "SoftSkill"
                elif "Specialization" in category:
                    return "IndustrySpecific"
                elif "Skills" in category:
                    return "SoftSkill"
                else:
                    return "Technical"  # Default to Technical

        # If not found in specific categories, try to infer from the keyword
        keyword_lower = keyword.lower()
        if any(term in keyword_lower for term in ["python", "java", "javascript", "c++", "c#", "go", "rust", "ruby", "php", "r", "scala"]):
            return "Technical"
        elif any(term in keyword_lower for term in ["react", "angular", "vue", "node", "express", "django", "flask", "spring", "fastapi"]):
            return "Technical"
        elif any(term in keyword_lower for term in ["docker", "kubernetes", "git", "aws", "azure", "gcp", "jenkins", "terraform"]):
            return "Technical"
        elif any(term in keyword_lower for term in ["leadership", "communication", "teamwork", "problem", "adaptability", "collaboration", "negotiation", "conflict resolution"]):
            return "SoftSkill"
        elif any(term in keyword_lower for term in ["agile", "scrum", "kanban", "lean", "design thinking"]):
            return "IndustrySpecific"
        else:
            return "Technical"  # Default category

    def generate_keyword_suggestions(self, resume_text: str, target_role: str = "Software Engineer") -> List[KeywordSuggestion]:
        """
        Generate keyword suggestions to improve the resume for the target role.

        Args:
            resume_text: The text content of the resume
            target_role: The target role to optimize for

        Returns:
            List of KeywordSuggestion entities
        """
        # Get role-specific keywords for the target role
        role_keywords = self.get_role_specific_keywords(target_role)

        # Calculate relevance scores for ALL role keywords to identify gaps and underrepresented terms
        all_relevance_scores = self.calculate_keyword_relevance(resume_text, role_keywords)

        suggestions = []
        for keyword, relevance_score in all_relevance_scores:
            # Focus on keywords that are missing or underrepresented in the resume
            # (keywords with low to medium relevance scores - meaning they're not adequately covered)
            if relevance_score <= 0.8:  # Suggest keywords that are not strongly represented (score > 0.8)
                # Double-check that the keyword is relevant to the target role
                if keyword in role_keywords:
                    # Calculate a relevance factor that accounts for importance to the target role
                    category = self.categorize_keyword(keyword)

                    # Enhance the relevance score based on the importance to the target role
                    # This ensures we prioritize keywords most important for the specific target role
                    enhanced_justification = self._generate_justification(keyword, target_role)
                    role_alignment = target_role

                    suggestion = KeywordSuggestion.create_new(
                        analysis_id="placeholder-analysis-id",  # This would be replaced with actual analysis ID
                        keyword=keyword,
                        relevance_score=relevance_score,
                        category=category,
                        justification=enhanced_justification,
                        role_alignment=role_alignment
                    )
                    suggestions.append(suggestion)

        # Remove duplicates while preserving order
        seen_keywords = set()
        unique_suggestions = []
        for suggestion in suggestions:
            if suggestion.keyword not in seen_keywords:
                seen_keywords.add(suggestion.keyword)
                unique_suggestions.append(suggestion)

        # Sort suggestions by relevance score (ascending - lowest first, so most missing appear first)
        # This prioritizes keywords that are most missing from the resume
        unique_suggestions.sort(key=lambda x: x.relevance_score)

        # Return top 10 suggestions that are most relevant and needed for the specific target role
        return unique_suggestions[:10]

    def _generate_justification(self, keyword: str, target_role: str) -> str:
        """
        Generate a justification for why a keyword is suggested.

        Args:
            keyword: The keyword to justify
            target_role: The target role

        Returns:
            Justification text
        """
        # Load justifications from the keyword mappings if available
        if 'justifications' in self.keyword_mappings:
            justifications = self.keyword_mappings['justifications']
            if keyword in justifications:
                # Use template replacement if needed
                template = justifications[keyword]
                return template.replace('{keyword}', keyword).replace('{target_role}', target_role)

        # If no specific justification is found, generate a generic one
        # Check if the keyword belongs to certain categories to customize the message
        for category, keywords_list in self.keyword_categories.items():
            if keyword in keywords_list:
                if 'Programming' in category or 'Language' in category:
                    return f"{keyword} is a valuable skill for {target_role} roles and appears frequently in job postings."
                elif 'Framework' in category:
                    return f"Experience with {keyword} framework is often required for {target_role} positions."
                elif 'Tool' in category:
                    return f"Proficiency in {keyword} is beneficial for {target_role} roles and enhances your competitiveness."
                elif 'Soft' in category:
                    return f"{keyword} skills are important for {target_role} collaboration and career advancement."
                elif 'Database' in category:
                    return f"Knowledge of {keyword} is essential for {target_role} roles dealing with data management."

        # Default generic justification
        return f"{keyword} is commonly mentioned in {target_role} job postings and would strengthen your resume."

    def get_keyword_suggestions_for_improvement(self, resume_text: str, target_role: str = "Software Engineer") -> List[Dict[str, any]]:
        """
        Get keyword suggestions with additional metadata for improvement recommendations.

        Args:
            resume_text: The text content of the resume
            target_role: The target role to optimize for

        Returns:
            List of dictionaries with keyword suggestion details
        """
        suggestions = self.generate_keyword_suggestions(resume_text, target_role)

        suggestion_details = []
        for suggestion in suggestions:
            detail = {
                "keyword": suggestion.keyword,
                "relevance_score": suggestion.relevance_score,
                "category": suggestion.category,
                "justification": suggestion.justification,
                "role_alignment": suggestion.role_alignment,
                "placement_suggestion": self._suggest_placement(suggestion.keyword, target_role)
            }
            suggestion_details.append(detail)

        return suggestion_details

    def _suggest_placement(self, keyword: str, target_role: str) -> str:
        """
        Suggest where to place a keyword in the resume.

        Args:
            keyword: The keyword to suggest placement for
            target_role: The target role

        Returns:
            Placement suggestion
        """
        if keyword in self.keyword_categories.get("Programming Language", []):
            return "Add to Skills section and mention in project descriptions"
        elif keyword in self.keyword_categories.get("Framework", []):
            return "Include in Skills section and highlight in relevant work experience"
        elif keyword in self.keyword_categories.get("Tool", []):
            return "List in Technical Skills section and reference in project or experience descriptions"
        elif keyword in self.keyword_categories.get("Soft Skill", []):
            return "Incorporate into summary/objective and demonstrate through experience descriptions"
        else:
            return "Include in relevant sections based on context"