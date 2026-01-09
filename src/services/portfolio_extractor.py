"""Portfolio Website Extractor Service for Resume Analyzer Core"""
import re
from typing import Dict, Any, List, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import httpx
from src.services.http_client import HttpClient, SyncHttpClient
from src.services.rate_limiter import RateLimiter
from src.utils.logger import get_logger
from src.utils.constants import HTTP_TIMEOUT_DEFAULT, MAX_PORTFOLIO_PAGES_DEFAULT
from src.utils.validation_utils import validate_url_security, validate_content_security


class PortfolioExtractor:
    """Extracts public profile data from portfolio websites"""

    def __init__(self, http_timeout: int = HTTP_TIMEOUT_DEFAULT, max_pages: int = MAX_PORTFOLIO_PAGES_DEFAULT):
        self.http_timeout = http_timeout
        self.max_pages = max_pages
        self.logger = get_logger("PortfolioExtractor")
        self.http_client = SyncHttpClient(timeout=http_timeout)
        self.rate_limiter = RateLimiter()

    def extract_profile(self, url: str) -> Dict[str, Any]:
        """
        Extract profile data from a portfolio website URL.

        Args:
            url: Portfolio website URL

        Returns:
            Dictionary with normalized profile data
        """
        self.logger.info(f"Starting portfolio website extraction from: {url}")

        # Validate URL security
        is_valid, error_msg = validate_url_security(url)
        if not is_valid:
            raise ValueError(f"Invalid portfolio URL: {error_msg}")

        # Apply rate limiting
        self.rate_limiter.wait_if_needed()

        try:
            # Get the main portfolio page
            response = self.http_client.get(url)
            response.raise_for_status()

            # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract main page content
            main_content = self._extract_normalized_content(soup, url)

            # Extract additional pages if available
            additional_content = self._extract_additional_pages(url, soup)

            # Merge main and additional content
            profile_data = self._merge_content(main_content, additional_content)

            self.logger.info(f"Successfully extracted portfolio website data from: {url}")
            return profile_data

        except httpx.RequestError as e:
            self.logger.error(f"HTTP error during portfolio extraction: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Error during portfolio extraction: {str(e)}")
            raise

    def _extract_normalized_content(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """
        Extract and normalize content from portfolio website HTML.

        Args:
            soup: BeautifulSoup object with portfolio HTML
            url: Original portfolio URL

        Returns:
            Dictionary with normalized profile data
        """
        normalized_content = {
            "url": url,
            "profile_type": "PORTFOLIO",
            "site_title": self._extract_site_title(soup),
            "bio_about": self._extract_bio_about(soup),
            "name": self._extract_name(soup),
            "email": self._extract_email(soup),
            "location": self._extract_location(soup),
            "social_links": self._extract_social_links(soup),
            "projects": self._extract_projects(soup),
            "skills": self._extract_skills(soup),
            "experience": self._extract_experience(soup),
            "education": self._extract_education(soup),
            "contact_visible": self._is_contact_visible(soup),
            "pages_analyzed": 1,  # Start with 1 for the main page
            "profile_image": self._extract_profile_image(soup),
            "last_updated": self._extract_last_updated(soup),
            "technologies_used": self._extract_technologies(soup)
        }

        # Remove None values
        normalized_content = {k: v for k, v in normalized_content.items() if v is not None}

        # Validate content security
        for key, value in normalized_content.items():
            if isinstance(value, str):
                is_valid, error_msg = validate_content_security(value)
                if not is_valid:
                    self.logger.warning(f"Content security validation failed for {key}: {error_msg}")
                    normalized_content[key] = ""  # Sanitize by removing potentially dangerous content
            elif isinstance(value, list):
                # Sanitize list items
                sanitized_list = []
                for item in value:
                    if isinstance(item, str):
                        is_valid, error_msg = validate_content_security(item)
                        if not is_valid:
                            self.logger.warning(f"Content security validation failed for list item in {key}: {error_msg}")
                            continue  # Skip dangerous content
                        sanitized_list.append(item)
                    elif isinstance(item, dict):
                        # Sanitize dictionary values
                        sanitized_dict = {}
                        for k, v in item.items():
                            if isinstance(v, str):
                                is_valid, error_msg = validate_content_security(v)
                                if not is_valid:
                                    self.logger.warning(f"Content security validation failed for dict value in {key}.{k}: {error_msg}")
                                    continue  # Skip dangerous content
                                sanitized_dict[k] = v
                            else:
                                sanitized_dict[k] = v
                        sanitized_list.append(sanitized_dict)
                    else:
                        sanitized_list.append(item)
                normalized_content[key] = sanitized_list

        return normalized_content

    def _extract_site_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract site title from portfolio website."""
        try:
            # Try multiple selectors for site title
            selectors = [
                'title',  # Standard HTML title
                'h1.site-title',  # Common site title class
                '.site-title',  # Alternative site title class
                'h1.brand',  # Brand title
                '.brand',  # Alternative brand class
            ]

            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text().strip()
                    if text:
                        return text

            return None
        except Exception as e:
            self.logger.warning(f"Error extracting site title: {str(e)}")
            return None

    def _extract_bio_about(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract bio/about section from portfolio website."""
        try:
            # Try multiple selectors for bio/about
            selectors = [
                '.bio', '.about', '.bio-content', '.about-content',  # Common classes
                '[id*="bio"]', '[id*="about"]',  # IDs containing bio/about
                'section.about', 'div.about',  # Sections
                '.intro', '.introduction',  # Alternative names
                '.hero-text', '.hero-content'  # Hero sections
            ]

            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text().strip()
                    if text and len(text) > 10:  # Ensure it's substantial content
                        # Remove "Read more" and similar text
                        text = re.sub(r'\s*Read more\s*|\s*Learn more\s*|\s*See more\s*', '', text).strip()
                        return text

            return None
        except Exception as e:
            self.logger.warning(f"Error extracting bio/about: {str(e)}")
            return None

    def _extract_name(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract name from portfolio website."""
        try:
            # Try multiple selectors for name
            selectors = [
                '.name', '.full-name', '.person-name',  # Common name classes
                'h1.name', 'h2.name',  # Name in headers
                '.header-name', '.title-name',  # Header names
                '[id*="name"]',  # IDs containing name
            ]

            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text().strip()
                    if text and len(text.split()) >= 2:  # Ensure it's a full name
                        return text

            return None
        except Exception as e:
            self.logger.warning(f"Error extracting name: {str(e)}")
            return None

    def _extract_email(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract email from portfolio website."""
        try:
            # Look for email in mailto links
            mailto_links = soup.select('a[href^="mailto:"]')
            for link in mailto_links:
                href = link.get('href', '')
                if href.startswith('mailto:'):
                    email = href[7:]  # Remove 'mailto:' prefix
                    # Basic email validation
                    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                        return email

            # Look for text that looks like email
            text = soup.get_text()
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text)
            if emails:
                # Return the first valid email found
                return emails[0]

            return None
        except Exception as e:
            self.logger.warning(f"Error extracting email: {str(e)}")
            return None

    def _extract_location(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract location from portfolio website."""
        try:
            # Try multiple selectors for location
            selectors = [
                '.location', '.loc', '.address',  # Common location classes
                '[id*="location"]', '[id*="loc"]',  # IDs containing location
                '.contact .location',  # Location in contact section
                '.footer .location',  # Location in footer
            ]

            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text().strip()
                    if text:
                        return text

            return None
        except Exception as e:
            self.logger.warning(f"Error extracting location: {str(e)}")
            return None

    def _extract_social_links(self, soup: BeautifulSoup) -> Optional[List[str]]:
        """Extract social media links from portfolio website."""
        try:
            social_links = []
            # Look for social media links
            social_selectors = [
                'a[href*="linkedin.com"]',
                'a[href*="github.com"]',
                'a[href*="twitter.com"]',
                'a[href*="dribbble.com"]',
                'a[href*="behance.net"]',
                'a[href*="instagram.com"]',
                'a[href*="facebook.com"]',
                '.social-links a',  # Common social links class
                '.social-media a',  # Alternative social media class
            ]

            for selector in social_selectors:
                elements = soup.select(selector)
                for element in elements:
                    href = element.get('href', '')
                    if href:
                        # Validate URL security before adding
                        is_valid, _ = validate_url_security(href)
                        if is_valid and href not in social_links:
                            social_links.append(href)

            return social_links if social_links else None
        except Exception as e:
            self.logger.warning(f"Error extracting social links: {str(e)}")
            return None

    def _extract_projects(self, soup: BeautifulSoup) -> Optional[List[Dict[str, Any]]]:
        """Extract projects from portfolio website."""
        try:
            projects = []
            # Try multiple selectors for projects
            selectors = [
                '.project', '.portfolio-item', '.work-item',  # Common project classes
                '.project-item', '.project-card',  # Alternative project classes
                '[id*="project"]', '[id*="work"]',  # IDs containing project/work
            ]

            elements = []
            for selector in selectors:
                found_elements = soup.select(selector)
                if found_elements:
                    elements = found_elements
                    break  # Use the first selector that finds content

            for element in elements:
                project = {
                    "name": self._get_text_from_selector(element, '.project-title, .project-name, h3, h4'),
                    "description": self._get_text_from_selector(element, '.project-description, .project-text, p'),
                    "technologies": self._extract_technologies_from_element(element),
                    "link": self._get_link_from_element(element),
                    "image": self._get_image_from_element(element),
                    "year": self._get_year_from_element(element)
                }

                # Remove None values
                project = {k: v for k, v in project.items() if v is not None and v.strip()}
                if project:  # Only add if there's at least one field
                    projects.append(project)

            return projects if projects else None
        except Exception as e:
            self.logger.warning(f"Error extracting projects: {str(e)}")
            return None

    def _extract_skills(self, soup: BeautifulSoup) -> Optional[List[str]]:
        """Extract skills from portfolio website."""
        try:
            skills = []
            # Try multiple selectors for skills
            selectors = [
                '.skills', '.skills-list', '.tech-stack',  # Common skill classes
                '.skills-container', '.competencies',  # Alternative classes
                '[id*="skill"]', '[id*="tech"]',  # IDs containing skill/tech
            ]

            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    # Get all list items or span elements within the skills section
                    skill_elements = element.select('li, span, .skill-item')
                    for skill_elem in skill_elements:
                        skill_text = skill_elem.get_text().strip()
                        if skill_text:
                            skills.append(skill_text)
                    break  # Use the first selector that finds content

            return skills if skills else None
        except Exception as e:
            self.logger.warning(f"Error extracting skills: {str(e)}")
            return None

    def _extract_experience(self, soup: BeautifulSoup) -> Optional[List[Dict[str, Any]]]:
        """Extract experience information from portfolio website."""
        try:
            experiences = []
            # Try multiple selectors for experience
            selectors = [
                '.experience', '.work-experience', '.employment',  # Common experience classes
                '.job', '.position', '.work-history',  # Alternative classes
                '[id*="experience"]', '[id*="work"]',  # IDs containing experience/work
            ]

            elements = []
            for selector in selectors:
                found_elements = soup.select(selector)
                if found_elements:
                    elements = found_elements
                    break  # Use the first selector that finds content

            for element in elements:
                exp = {
                    "title": self._get_text_from_selector(element, '.job-title, .position-title, h3'),
                    "company": self._get_text_from_selector(element, '.company, .employer, .organization'),
                    "dates": self._get_text_from_selector(element, '.dates, .date, .duration'),
                    "location": self._get_text_from_selector(element, '.location'),
                    "description": self._get_text_from_selector(element, '.job-description, .description, p')
                }

                # Remove None values
                exp = {k: v for k, v in exp.items() if v is not None and v.strip()}
                if exp:  # Only add if there's at least one field
                    experiences.append(exp)

            return experiences if experiences else None
        except Exception as e:
            self.logger.warning(f"Error extracting experience: {str(e)}")
            return None

    def _extract_education(self, soup: BeautifulSoup) -> Optional[List[Dict[str, Any]]]:
        """Extract education information from portfolio website."""
        try:
            education = []
            # Try multiple selectors for education
            selectors = [
                '.education', '.education-history', '.school',  # Common education classes
                '.degree', '.academic',  # Alternative classes
                '[id*="education"]', '[id*="school"]',  # IDs containing education/school
            ]

            elements = []
            for selector in selectors:
                found_elements = soup.select(selector)
                if found_elements:
                    elements = found_elements
                    break  # Use the first selector that finds content

            for element in elements:
                edu = {
                    "school": self._get_text_from_selector(element, '.school-name, .institution, h3'),
                    "degree": self._get_text_from_selector(element, '.degree, .qualification'),
                    "field": self._get_text_from_selector(element, '.field, .major'),
                    "dates": self._get_text_from_selector(element, '.dates, .date')
                }

                # Remove None values
                edu = {k: v for k, v in edu.items() if v is not None and v.strip()}
                if edu:  # Only add if there's at least one field
                    education.append(edu)

            return education if education else None
        except Exception as e:
            self.logger.warning(f"Error extracting education: {str(e)}")
            return None

    def _is_contact_visible(self, soup: BeautifulSoup) -> bool:
        """Check if contact information is visible on the portfolio."""
        try:
            # Look for contact-related elements
            contact_selectors = [
                '.contact', '.contact-form', '[id*="contact"]',  # Contact sections
                'form[action*="contact"]',  # Contact forms
                '.email', '.phone', '[href^="mailto:"]',  # Contact info
                '.contact-button', '.get-in-touch'  # Contact buttons
            ]

            for selector in contact_selectors:
                element = soup.select_one(selector)
                if element:
                    return True

            return False
        except Exception as e:
            self.logger.warning(f"Error checking contact visibility: {str(e)}")
            return False

    def _extract_profile_image(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract profile image URL from portfolio website."""
        try:
            # Look for profile images
            selectors = [
                '.profile-image img', '.avatar img', '.photo img',  # Common profile image classes
                '.header img', '.hero img',  # Header/hero images
                'img[src*="profile"]', 'img[src*="avatar"]',  # Images with profile/avatar in URL
            ]

            for selector in selectors:
                element = soup.select_one(selector)
                if element and element.get('src'):
                    img_url = element.get('src')
                    # Convert relative URLs to absolute
                    if img_url.startswith('/'):
                        img_url = urljoin(soup.base_url, img_url) if soup.base_url else img_url
                    return img_url

            return None
        except Exception as e:
            self.logger.warning(f"Error extracting profile image: {str(e)}")
            return None

    def _extract_last_updated(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract last updated information from portfolio website."""
        try:
            # Look for last updated information
            selectors = [
                '.last-updated', '.updated', '[id*="updated"]',  # Common updated classes
                'time[datetime]',  # Time elements with datetime
                '.footer',  # Sometimes last updated is in footer
            ]

            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    text = element.get_text().strip()
                    if text and ('update' in text.lower() or 'last' in text.lower() or re.search(r'\d{4}', text)):
                        return text

            return None
        except Exception as e:
            self.logger.warning(f"Error extracting last updated: {str(e)}")
            return None

    def _extract_technologies(self, soup: BeautifulSoup) -> Optional[List[str]]:
        """Extract technologies used from portfolio website."""
        try:
            technologies = []
            # Look for technology-related elements
            selectors = [
                '.technologies', '.tech-stack', '.tools',  # Common tech classes
                '.skills', '.languages',  # Skills and languages
                '[id*="tech"]', '[id*="stack"]',  # IDs containing tech/stack
            ]

            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    # Get all text and try to identify technologies
                    text = element.get_text().strip()
                    # Common tech keywords to look for
                    tech_keywords = [
                        'Python', 'JavaScript', 'React', 'Node.js', 'Django', 'Flask',
                        'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'SQL', 'MongoDB',
                        'Java', 'C++', 'C#', 'Go', 'Rust', 'TypeScript', 'Vue', 'Angular',
                        'HTML', 'CSS', 'SASS', 'Git', 'Linux', 'Machine Learning', 'AI'
                    ]

                    for keyword in tech_keywords:
                        if keyword.lower() in text.lower():
                            if keyword not in technologies:
                                technologies.append(keyword)

                    # Also look for list items or spans
                    tech_elements = element.select('li, span, .tech-item')
                    for tech_elem in tech_elements:
                        tech_text = tech_elem.get_text().strip()
                        if tech_text and tech_text not in technologies:
                            technologies.append(tech_text)

                    if technologies:
                        break  # Use the first selector that finds content

            return technologies if technologies else None
        except Exception as e:
            self.logger.warning(f"Error extracting technologies: {str(e)}")
            return None

    def _extract_additional_pages(self, base_url: str, main_soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Extract content from additional pages linked from the main portfolio page.

        Args:
            base_url: Base URL of the portfolio
            main_soup: BeautifulSoup object of the main page

        Returns:
            Dictionary with additional content
        """
        additional_content = {
            "projects": [],
            "skills": [],
            "experience": [],
            "education": [],
            "pages_analyzed": 1  # Start with 1 for the main page
        }

        try:
            # Find links to other pages like 'projects', 'about', 'contact', etc.
            nav_links = main_soup.select('nav a, .navigation a, .menu a, .nav a')
            page_links = []

            for link in nav_links:
                href = link.get('href', '')
                if href:
                    # Convert relative URLs to absolute
                    if href.startswith('/'):
                        full_url = urljoin(base_url, href)
                    elif href.startswith('#'):
                        continue  # Skip anchor links
                    else:
                        full_url = href

                    # Only follow links within the same domain
                    base_domain = urlparse(base_url).netloc
                    link_domain = urlparse(full_url).netloc
                    if base_domain == link_domain:
                        page_links.append(full_url)

            # Limit the number of additional pages to avoid excessive requests
            page_links = page_links[:self.max_pages - 1]  # -1 because we already analyzed the main page

            for page_url in page_links:
                try:
                    # Apply rate limiting
                    self.rate_limiter.wait_if_needed()

                    response = self.http_client.get(page_url)
                    response.raise_for_status()

                    page_soup = BeautifulSoup(response.text, 'html.parser')

                    # Extract content based on the page URL or content
                    if 'project' in page_url.lower() or 'work' in page_url.lower():
                        projects = self._extract_projects(page_soup)
                        if projects:
                            additional_content["projects"].extend(projects)
                    elif 'about' in page_url.lower() or 'bio' in page_url.lower():
                        # Extract bio from about page
                        bio = self._extract_bio_about(page_soup)
                        if bio:
                            additional_content["bio_about"] = bio
                    elif 'skill' in page_url.lower() or 'tech' in page_url.lower():
                        skills = self._extract_skills(page_soup)
                        if skills:
                            additional_content["skills"].extend(skills)
                    elif 'experience' in page_url.lower() or 'work' in page_url.lower():
                        experience = self._extract_experience(page_soup)
                        if experience:
                            additional_content["experience"].extend(experience)
                    elif 'education' in page_url.lower() or 'school' in page_url.lower():
                        education = self._extract_education(page_soup)
                        if education:
                            additional_content["education"].extend(education)

                    additional_content["pages_analyzed"] += 1

                except Exception as e:
                    self.logger.warning(f"Error extracting content from {page_url}: {str(e)}")
                    continue  # Continue with next page

        except Exception as e:
            self.logger.warning(f"Error extracting additional pages: {str(e)}")

        return additional_content

    def _merge_content(self, main_content: Dict[str, Any], additional_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge main content with additional content from other pages.

        Args:
            main_content: Content from the main page
            additional_content: Content from additional pages

        Returns:
            Merged content dictionary
        """
        merged = main_content.copy()

        # Merge lists
        for key in ['projects', 'skills', 'experience', 'education']:
            if key in additional_content and additional_content[key]:
                if key in merged:
                    # Combine lists, avoiding duplicates
                    combined = merged[key] + additional_content[key]
                    # Remove duplicates while preserving order
                    merged[key] = list({item['name'] if isinstance(item, dict) and 'name' in item else str(item): item for item in combined}.values())
                else:
                    merged[key] = additional_content[key]

        # Update pages analyzed
        merged["pages_analyzed"] = main_content.get("pages_analyzed", 1) + additional_content.get("pages_analyzed", 0) - 1  # -1 because main page is counted in both

        # Update bio if found in additional content
        if "bio_about" in additional_content and additional_content["bio_about"]:
            merged["bio_about"] = additional_content["bio_about"]

        return merged

    def _extract_technologies_from_element(self, element) -> Optional[List[str]]:
        """Extract technologies from a specific element."""
        try:
            tech_list = []
            # Look for technology-related text in the element
            text = element.get_text()
            tech_keywords = [
                'Python', 'JavaScript', 'React', 'Node.js', 'Django', 'Flask',
                'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'SQL', 'MongoDB',
                'Java', 'C++', 'C#', 'Go', 'Rust', 'TypeScript', 'Vue', 'Angular',
                'HTML', 'CSS', 'SASS', 'Git', 'Linux', 'Machine Learning', 'AI'
            ]

            for keyword in tech_keywords:
                if keyword.lower() in text.lower():
                    if keyword not in tech_list:
                        tech_list.append(keyword)

            return tech_list if tech_list else None
        except Exception:
            return None

    def _get_link_from_element(self, element) -> Optional[str]:
        """Extract link from a project element."""
        try:
            link_element = element.select_one('a')
            if link_element and link_element.get('href'):
                href = link_element.get('href')
                # Validate URL security before returning
                is_valid, _ = validate_url_security(href)
                if is_valid:
                    return href
            return None
        except Exception:
            return None

    def _get_image_from_element(self, element) -> Optional[str]:
        """Extract image from a project element."""
        try:
            img_element = element.select_one('img')
            if img_element and img_element.get('src'):
                return img_element.get('src')
            return None
        except Exception:
            return None

    def _get_year_from_element(self, element) -> Optional[str]:
        """Extract year from a project element."""
        try:
            text = element.get_text()
            year_match = re.search(r'\b(19|20)\d{2}\b', text)
            return year_match.group(0) if year_match else None
        except Exception:
            return None

    def _get_text_from_selector(self, element, selector: str) -> Optional[str]:
        """Helper method to get text from a sub-selector."""
        try:
            sub_element = element.select_one(selector)
            if sub_element:
                return sub_element.get_text().strip()
            return None
        except Exception:
            return None

    def extract(self, url: str) -> Dict[str, Any]:
        """
        Extract profile data from a portfolio website URL (alias for extract_profile).

        Args:
            url: Portfolio website URL

        Returns:
            Dictionary with normalized profile data
        """
        return self.extract_profile(url)

    def validate_portfolio_url(self, url: str) -> bool:
        """
        Validate if a URL is a valid portfolio website URL.

        Args:
            url: URL to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            # Check if URL matches general website pattern
            is_valid, _ = validate_url_security(url)
            if not is_valid:
                return False

            # Check if it's a valid HTTP/HTTPS URL
            pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/?$'
            return bool(re.match(pattern, url))

        except Exception:
            return False