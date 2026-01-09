"""GitHub Profile Extractor Service for Resume Analyzer Core"""
import re
from typing import Dict, Any, List, Optional
from github import Github
from github.GithubException import GithubException
import httpx
from src.services.http_client import HttpClient, SyncHttpClient
from src.services.rate_limiter import RateLimiter
from src.utils.logger import get_logger
from src.utils.constants import HTTP_TIMEOUT_DEFAULT
from src.utils.validation_utils import validate_url_security


class GitHubExtractor:
    """Extracts public profile data from GitHub profiles"""

    def __init__(self, github_token: Optional[str] = None, http_timeout: int = HTTP_TIMEOUT_DEFAULT):
        self.github_token = github_token or self._get_github_token()
        self.http_timeout = http_timeout
        self.logger = get_logger("GitHubExtractor")
        self.http_client = SyncHttpClient(timeout=http_timeout)
        self.rate_limiter = RateLimiter()

        # Initialize GitHub client
        self.github_client = Github(self.github_token) if self.github_token else Github()

    def _get_github_token(self) -> Optional[str]:
        """Get GitHub token from environment variables."""
        import os
        return os.getenv('GITHUB_TOKEN')

    def extract_profile(self, url: str) -> Dict[str, Any]:
        """
        Extract profile data from a GitHub URL.

        Args:
            url: GitHub profile URL

        Returns:
            Dictionary with normalized profile data
        """
        self.logger.info(f"Starting GitHub profile extraction from: {url}")

        # Validate URL security
        is_valid, error_msg = validate_url_security(url)
        if not is_valid:
            raise ValueError(f"Invalid GitHub URL: {error_msg}")

        # Extract username from URL
        username = self._extract_username_from_url(url)
        if not username:
            raise ValueError(f"Could not extract username from GitHub URL: {url}")

        # Apply rate limiting
        self.rate_limiter.wait_if_needed()

        try:
            # Get GitHub user profile
            user = self.github_client.get_user(username)

            # Extract profile data
            profile_data = self._extract_normalized_content(user, url)

            self.logger.info(f"Successfully extracted GitHub profile data from: {url}")
            return profile_data

        except GithubException as e:
            self.logger.error(f"GitHub API error during extraction: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error during GitHub extraction: {str(e)}")
            raise

    def _extract_username_from_url(self, url: str) -> Optional[str]:
        """
        Extract GitHub username from URL.

        Args:
            url: GitHub profile URL

        Returns:
            GitHub username or None if not found
        """
        # Pattern for GitHub profile URLs: https://github.com/username
        pattern = r'https?://(?:www\.)?github\.com/([a-zA-Z0-9_-]+)/?'
        match = re.match(pattern, url)
        return match.group(1) if match else None

    def _extract_normalized_content(self, user, url: str) -> Dict[str, Any]:
        """
        Extract and normalize content from GitHub profile.

        Args:
            user: GitHub user object
            url: Original profile URL

        Returns:
            Dictionary with normalized profile data
        """
        # Extract repositories
        repositories = self._extract_repositories(user)

        normalized_content = {
            "url": url,
            "profile_type": "GITHUB",
            "username": user.login,
            "bio": user.bio,
            "name": user.name,
            "company": user.company,
            "location": user.location,
            "email": user.email,
            "blog": user.blog,
            "public_repos": user.public_repos,
            "public_gists": user.public_gists,
            "followers": user.followers,
            "following": user.following,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            "repositories": repositories,
            "total_stars": self._calculate_total_stars(repositories),
            "recent_activity": self._get_recent_activity(user),
            "top_languages": self._get_top_languages(repositories),
            "profile_image": user.avatar_url,
            "hireable": user.hireable,
            "twitter_username": user.twitter_username
        }

        # Remove None values
        normalized_content = {k: v for k, v in normalized_content.items() if v is not None}

        return normalized_content

    def _extract_repositories(self, user) -> List[Dict[str, Any]]:
        """
        Extract repository information from user.

        Args:
            user: GitHub user object

        Returns:
            List of repository dictionaries
        """
        repositories = []
        try:
            # Get user's repositories
            repos = user.get_repos(sort='updated', direction='desc')  # Sort by most recently updated

            # Limit to first 20 repositories to avoid excessive API calls
            for repo in repos[:20]:
                try:
                    repo_data = {
                        "name": repo.name,
                        "full_name": repo.full_name,
                        "description": repo.description,
                        "language": repo.language,
                        "stars": repo.stargazers_count,
                        "forks": repo.forks_count,
                        "watchers": repo.watchers_count,
                        "size": repo.size,
                        "created_at": repo.created_at.isoformat() if repo.created_at else None,
                        "updated_at": repo.updated_at.isoformat() if repo.updated_at else None,
                        "primary_language": repo.language,
                        "is_fork": repo.fork,
                        "is_private": repo.private,
                        "has_issues": repo.has_issues,
                        "has_projects": repo.has_projects,
                        "has_wiki": repo.has_wiki,
                        "license": repo.license.name if repo.license else None,
                        "default_branch": repo.default_branch,
                        "clone_url": repo.clone_url,
                        "html_url": repo.html_url,
                        "topics": repo.get_topics() if repo.get_topics() else []
                    }

                    # Remove None values
                    repo_data = {k: v for k, v in repo_data.items() if v is not None}
                    repositories.append(repo_data)
                except Exception as e:
                    self.logger.warning(f"Error extracting repository {repo.name}: {str(e)}")
                    continue  # Continue with next repository

        except GithubException as e:
            self.logger.error(f"Error getting repositories: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error getting repositories: {str(e)}")

        return repositories

    def _calculate_total_stars(self, repositories: List[Dict[str, Any]]) -> int:
        """
        Calculate total stars across all repositories.

        Args:
            repositories: List of repository dictionaries

        Returns:
            Total star count
        """
        total_stars = 0
        for repo in repositories:
            stars = repo.get('stars', 0)
            if isinstance(stars, int) and stars > 0:
                total_stars += stars
        return total_stars

    def _get_recent_activity(self, user) -> List[Dict[str, Any]]:
        """
        Get recent activity from user's events.

        Args:
            user: GitHub user object

        Returns:
            List of recent activity events
        """
        recent_activity = []
        try:
            # Get user's events (limited to recent ones)
            events = user.get_events()[:10]  # Get last 10 events

            for event in events:
                try:
                    activity = {
                        "type": event.type,
                        "repo": event.repo.name if event.repo else None,
                        "created_at": event.created_at.isoformat() if event.created_at else None,
                        "payload": event.payload
                    }

                    # Remove None values
                    activity = {k: v for k, v in activity.items() if v is not None}
                    recent_activity.append(activity)
                except Exception as e:
                    self.logger.warning(f"Error extracting event: {str(e)}")
                    continue  # Continue with next event

        except GithubException as e:
            self.logger.error(f"Error getting recent activity: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error getting recent activity: {str(e)}")

        return recent_activity

    def _get_top_languages(self, repositories: List[Dict[str, Any]]) -> List[str]:
        """
        Get top programming languages from repositories.

        Args:
            repositories: List of repository dictionaries

        Returns:
            List of top languages
        """
        language_count = {}
        for repo in repositories:
            language = repo.get('language')
            if language:
                language_count[language] = language_count.get(language, 0) + 1

        # Sort by count and return top languages
        sorted_languages = sorted(language_count.items(), key=lambda x: x[1], reverse=True)
        return [lang for lang, count in sorted_languages if lang is not None]

    def validate_github_url(self, url: str) -> bool:
        """
        Validate if a URL is a valid GitHub profile URL.

        Args:
            url: URL to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            # Check if URL matches GitHub pattern
            is_valid, _ = validate_url_security(url)
            if not is_valid:
                return False

            # Extract username and check if it's valid
            username = self._extract_username_from_url(url)
            if not username:
                return False

            # Check if it's a valid GitHub URL format
            pattern = r'https?://(?:www\.)?github\.com/[a-zA-Z0-9_-]+/?'
            return bool(re.match(pattern, url))

        except Exception:
            return False

    def extract(self, url: str) -> Dict[str, Any]:
        """
        Extract profile data from a GitHub URL (alias for extract_profile).

        Args:
            url: GitHub profile URL

        Returns:
            Dictionary with normalized profile data
        """
        return self.extract_profile(url)

    def get_user_stats(self, username: str) -> Dict[str, Any]:
        """
        Get basic stats for a GitHub user.

        Args:
            username: GitHub username

        Returns:
            Dictionary with user statistics
        """
        try:
            user = self.github_client.get_user(username)
            return {
                "public_repos": user.public_repos,
                "followers": user.followers,
                "following": user.following,
                "total_stars": self._calculate_total_stars(self._extract_repositories(user)),
                "most_used_languages": self._get_top_languages(self._extract_repositories(user))[:5]  # Top 5
            }
        except GithubException:
            return {}