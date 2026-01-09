# Quickstart: Portfolio + LinkedIn / GitHub Integration

## Prerequisites

- Python 3.11+
- pip package manager
- Phase 1 (Resume Analyzer Core) installed and configured
- Google AI SDK configured with GEMINI_API_KEY

## Installation

### 1. Install Additional Dependencies

```bash
pip install -r requirements.txt
```

New dependencies for Phase 2:
```txt
# Web scraping and HTTP
beautifulsoup4>=4.12.0
httpx>=0.25.0
lxml>=4.9.0

# GitHub API
PyGithub>=2.1.0

# Rate limiting
tenacity>=8.2.0

# URL validation
validators>=0.22.0
```

### 2. Environment Configuration

Add to your `.env` file:
```env
# Phase 2 Configuration
GEMINI_API_KEY=your_gemini_api_key  # Required: Google AI API key
GITHUB_TOKEN=your_github_token      # Optional: increases rate limit to 5000/hour
HTTP_TIMEOUT=10                      # Seconds
MAX_RETRIES=5
RETRY_BASE_DELAY=1                  # Seconds
MAX_PORTFOLIO_PAGES=5               # Max pages to analyze per portfolio
```

## Running the Application

### Development Mode
```bash
streamlit run src/main.py
```

The application will be available at `http://localhost:8501`

## Usage

### 1. Enter Profile URLs
Navigate to the "Profile Analysis" tab and enter one or more URLs:
- **LinkedIn**: `https://linkedin.com/in/your-profile`
- **GitHub**: `https://github.com/your-username`
- **Portfolio**: `https://your-portfolio-site.com`

### 2. Validate and Analyze
- Click "Validate URLs" to check accessibility
- Click "Analyze Profiles" to extract and analyze data
- View results in the sectioned dashboard

### 3. View Results
- **Profile Overview**: Summary of each profile
- **Strengths & Weaknesses**: Color-coded insights
- **Improvement Suggestions**: Actionable recommendations
- **Resume Alignment**: Comparison with Phase 1 resume analysis

### 4. Export Report
- Click "Download Full Report" for combined PDF
- Includes Phase 1 resume analysis + Phase 2 profile insights

## API Usage Examples

### URL Validation
```python
from src.services.url_validator import URLValidator

validator = URLValidator()
result = validator.validate("https://github.com/username")
print(result.is_valid, result.profile_type)
```

### Profile Extraction
```python
from src.services.github_extractor import GitHubExtractor

extractor = GitHubExtractor()
profile_data = extractor.extract("https://github.com/username")
print(profile_data.normalized_content)
```

### AI Analysis with Gemini
```python
from src.services.ai_analyzer import AIAnalyzer

ai_analyzer = AIAnalyzer()
analysis = ai_analyzer.analyze_profile(profile_data, "GITHUB")
print(analysis.strengths, analysis.weaknesses)
```

### Alignment Analysis
```python
from src.services.alignment_analyzer import AlignmentAnalyzer

analyzer = AlignmentAnalyzer()
alignment = analyzer.analyze(resume_data, profile_data_list)
print(alignment.overall_score)
```

## Testing

### Run Unit Tests
```bash
pytest tests/unit/test_services/test_url_validator.py
pytest tests/unit/test_services/test_github_extractor.py
pytest tests/unit/test_services/test_linkedin_extractor.py
pytest tests/unit/test_services/test_portfolio_extractor.py
```

### Run Integration Tests
```bash
pytest tests/integration/test_profile_flow.py
```

### Run All Tests
```bash
pytest tests/ -v
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| LinkedIn extraction fails | Check if profile is public; some profiles restrict access |
| GitHub rate limit exceeded | Add `GITHUB_TOKEN` to `.env` for higher limits |
| Portfolio timeout | Increase `HTTP_TIMEOUT`; site may be slow |
| Analysis takes too long | Check network; reduce `MAX_PORTFOLIO_PAGES` |

### Rate Limiting

The system implements exponential backoff:
- Initial delay: 1 second
- Maximum delay: 32 seconds
- Maximum retries: 5
- User is notified of delays via progress indicator

### Graceful Degradation

If extraction fails partially:
- System extracts available content
- Limitations are displayed to user
- Partial analysis is provided with confidence indicators