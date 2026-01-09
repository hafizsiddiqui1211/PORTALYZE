"""Application constants for Resume Analyzer Core"""

# File processing
SUPPORTED_FILE_TYPES = [".pdf", ".docx"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes
FILE_SIZE_LIMIT_MB = 10

# Analysis
ATS_KEYWORD_WEIGHT = 0.4
ATS_FORMATTING_WEIGHT = 0.3
ATS_SECTION_WEIGHT = 0.3

# Performance targets
TEXT_EXTRACTION_TIMEOUT = 10  # seconds
ANALYSIS_TIMEOUT = 15  # seconds
PDF_GENERATION_TIMEOUT = 5  # seconds

# Session management
SESSION_TIMEOUT = 24 * 60 * 60  # 24 hours in seconds
TEMP_FILE_RETENTION_HOURS = 24

# UI/Display
COLOR_STRENGTHS = "#2ECC71"  # Green
COLOR_WEAKNESSES = "#E74C3C"  # Red
COLOR_NEUTRAL = "#3498DB"     # Blue

# Error messages
ERROR_FILE_TYPE = "Please upload a PDF or DOCX file."
ERROR_FILE_SIZE = f"File size exceeds {FILE_SIZE_LIMIT_MB}MB limit."
ERROR_EXTRACTION_FAILED = "Failed to extract text from the uploaded file."

# Phase 2: Portfolio + LinkedIn / GitHub Integration constants
# URL validation patterns
LINKEDIN_URL_PATTERN = r'^https?://(www\.)?linkedin\.com/in/[^/]+(\?.*)?$'
GITHUB_URL_PATTERN = r'^https?://(www\.)?github\.com/[a-zA-Z0-9_-]+/?$'
PORTFOLIO_URL_PATTERN = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/?$'

# Profile types
PROFILE_TYPE_LINKEDIN = "LINKEDIN"
PROFILE_TYPE_GITHUB = "GITHUB"
PROFILE_TYPE_PORTFOLIO = "PORTFOLIO"
SUPPORTED_PROFILE_TYPES = [PROFILE_TYPE_LINKEDIN, PROFILE_TYPE_GITHUB, PROFILE_TYPE_PORTFOLIO]

# HTTP client configuration
HTTP_TIMEOUT_DEFAULT = 10  # seconds
HTTP_MAX_RETRIES = 5
HTTP_RETRY_BASE_DELAY = 1  # seconds
HTTP_RETRY_MAX_DELAY = 32  # seconds

# Portfolio extraction
MAX_PORTFOLIO_PAGES_DEFAULT = 5  # Max pages to analyze per portfolio

# Rate limiting
RATE_LIMIT_BASE_DELAY = 1  # seconds
RATE_LIMIT_MAX_DELAY = 32  # seconds
RATE_LIMIT_MAX_RETRIES = 5

# Profile analysis
PROFILE_ANALYSIS_TIMEOUT = 20  # seconds per profile

# Phase 3: Job Role Recommender constants
# Seniority levels
SENIORITY_JUNIOR = "JUNIOR"
SENIORITY_MID = "MID"
SENIORITY_SENIOR = "SENIOR"
SENIORITY_LEVELS = [SENIORITY_JUNIOR, SENIORITY_MID, SENIORITY_SENIOR]

# Confidence thresholds
CONFIDENCE_HIGH = 0.8
CONFIDENCE_MEDIUM = 0.5
CONFIDENCE_LOW = 0.3

# Industry list
INDUSTRY_AI_ML = "AI/ML"
INDUSTRY_SOFTWARE_ENGINEERING = "Software Engineering"
INDUSTRY_DATA = "Data"
INDUSTRY_FINTECH = "FinTech"
INDUSTRY_EDTECH = "EdTech"
INDUSTRY_CLOUD = "Cloud"
INDUSTRY_CYBERSECURITY = "Cybersecurity"
INDUSTRY_DEVOPS = "DevOps"
SUPPORTED_INDUSTRIES = [
    INDUSTRY_AI_ML,
    INDUSTRY_SOFTWARE_ENGINEERING,
    INDUSTRY_DATA,
    INDUSTRY_FINTECH,
    INDUSTRY_EDTECH,
    INDUSTRY_CLOUD,
    INDUSTRY_CYBERSECURITY,
    INDUSTRY_DEVOPS
]

# Role recommendation settings
MIN_ROLES_PER_INDUSTRY = 2
MAX_ROLES_PER_INDUSTRY = 5
ROLE_INFERENCE_TIMEOUT = 30  # seconds

# Consent and data retention
CONSENT_STORAGE_HOURS = 24  # hours to store anonymized data