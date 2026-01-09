# Resume & Profile Analyzer

A comprehensive tool that analyzes resumes and online profiles (LinkedIn, GitHub, portfolio websites) to provide ATS compatibility scores, profile insights, and personalized job role recommendations.

## Features

- **Resume Analysis**: Upload and analyze your resume for ATS compatibility
- **Profile Analysis**: Analyze LinkedIn, GitHub, and portfolio websites
- **Role Recommendations**: Get personalized job role suggestions based on your profile
- **Gap Analysis**: Identify skill gaps and improvement opportunities
- **Confidence Scoring**: Get confidence levels for recommendations
- **Privacy Compliance**: PII anonymization and consent management
- **Theme Support**: Choose between light, dark, and system themes

## Prerequisites

- Python 3.11 or higher
- Google AI API key (for Claude CLI integration)

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your API key:
```
GEMINI_API_KEY=your_google_ai_api_key_here
```

## Configuration

1. Copy `.env.example` to `.env` and update with your API key:
```bash
cp .env.example .env
```

2. Update `src/utils/constants.py` with your configuration as needed.

## Running Locally

### Method 1: Using Streamlit CLI (Recommended)
```bash
streamlit run src/main.py
```

### Theme Configuration
The application supports three themes:
- **System**: Follows your operating system's theme preference
- **Light**: Light color scheme
- **Dark**: Dark color scheme

You can change the theme in the sidebar under the "🎨 Theme" section.

### Method 2: Using Python with PYTHONPATH
```bash
# On Windows:
set PYTHONPATH=%PYTHONPATH%;.
python -m src.main

# On macOS/Linux:
export PYTHONPATH=$PYTHONPATH:.
python -m src.main
```

### Method 3: Using pip install in development mode
```bash
pip install -e .
streamlit run src/main.py
```

The application will be available at `http://localhost:8501`

## Project Structure

```
Paralyzer/
├── .env.example          # Example environment variables
├── .gitignore           # Git ignore patterns
├── requirements.txt     # Python dependencies
├── specs/              # Feature specifications
│   └── 003-job-role-recommender/
│       ├── spec.md     # Feature specification
│       ├── plan.md     # Technical implementation plan
│       ├── tasks.md    # Implementation tasks
│       └── quickstart_validation.py  # Validation script
├── src/                # Source code
│   ├── main.py         # Main Streamlit application
│   ├── models/         # Pydantic data models
│   ├── services/       # Core services
│   ├── ui/            # User interface components
│   ├── utils/         # Utility functions
│   └── knowledge/     # Knowledge base files
├── tests/             # Test files
├── data/              # Data files (if any)
└── history/           # Prompt History Records and ADRs
```

## Key Components

### Models
- `industry.py`: Industry selection data models
- `profile_signals.py`: Profile signals aggregation
- `role_recommendation.py`: Role recommendation models
- `gap_analysis.py`: Skill gap analysis models

### Services
- `knowledge_base.py`: Role archetype knowledge loader
- `signal_aggregator.py`: Signal aggregation from multiple sources
- `role_inferencer.py`: Role recommendation engine with Claude integration
- `seniority_detector.py`: Seniority level detection
- `gap_analyzer.py`: Gap analysis service
- `confidence_calculator.py`: Confidence scoring for recommendations
- `anonymizer.py`: PII anonymization
- `consent_manager.py`: Consent management

### UI Components
- `industry_selector.py`: Industry selection interface
- `role_card.py`: Role recommendation display cards
- `recommendation_summary.py`: Summary of recommendations
- `combined_career_insights.py`: Cross-phase insights

## Environment Variables

- `GEMINI_API_KEY`: Your Google AI API key for Claude integration
- `ROLE_INFERENCE_TIMEOUT`: Timeout for role inference operations (default: 30 seconds)
- `MAX_ROLES_PER_INDUSTRY`: Maximum roles to recommend per industry (default: 5)
- `MIN_ROLES_PER_INDUSTRY`: Minimum roles to recommend per industry (default: 2)

## Pushing to GitHub

1. Initialize git repository (if not already done):
```bash
git init
git add .
git commit -m "Initial commit"
```

2. Add your remote repository:
```bash
git remote add origin <your-github-repository-url>
git branch -M main
git push -u origin main
```

3. For subsequent commits:
```bash
git add .
git commit -m "Descriptive commit message"
git push
```

## Deploying to Streamlit Cloud

1. Create a GitHub repository with your code

2. Go to [Streamlit Cloud](https://streamlit.io/cloud)

3. Sign in and click "New app"

4. Select your GitHub repository

5. Configure the deployment:
   - Main file path: `src/main.py`
   - Python version: 3.11+
   - Set environment variables in the Secrets section (click the lock icon):
   ```
   [secrets]
   GEMINI_API_KEY = "your_google_ai_api_key"
   ROLE_INFERENCE_TIMEOUT = "30"
   MAX_ROLES_PER_INDUSTRY = "5"
   MIN_ROLES_PER_INDUSTRY = "2"
   ```

6. Click "Deploy"

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`
**Solution**: Make sure you're running from the project root with PYTHONPATH set or use streamlit run command:
```bash
streamlit run src/main.py
```

**Issue**: API key errors
**Solution**: Ensure your `.env` file is properly configured with a valid GEMINI_API_KEY

**Issue**: Import errors
**Solution**: Make sure all dependencies are installed with `pip install -r requirements.txt`

### Running Tests

To validate the setup, run:
```bash
python specs/003-job-role-recommender/quickstart_validation.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.