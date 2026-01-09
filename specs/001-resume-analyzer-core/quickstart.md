# Quickstart: Resume Analyzer Core

## Setup

### Prerequisites
- Python 3.11+
- pip package manager
- Git (for version control)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install SpeckitPlus for Gemini API integration:
   ```bash
   pip install speckitplus
   ```

## Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key
TEMP_DIR=data/temp
MAX_FILE_SIZE=10485760  # 10MB in bytes
SESSION_TIMEOUT=86400    # 24 hours in seconds
```

### Gemini API Setup
1. Ensure Gemini API is properly configured with your API key
2. Verify SpeckitPlus is working by running:
   ```bash
   python -c "import speckitplus; print('SpeckitPlus OK')"
   ```

## Running the Application

### Development Mode
```bash
streamlit run src/main.py
```

The application will be available at `http://localhost:8501`

### Production Mode
```bash
streamlit run src/main.py --server.port 8080 --server.address 0.0.0.0
```

## Usage

### 1. Upload Resume
- Navigate to the application in your browser
- Click "Choose File" to select a PDF or DOCX resume
- Click "Analyze" to start the analysis process

### 2. View Results
- ATS score will be displayed prominently
- Color-coded sections show strengths (green) and weaknesses (red)
- Detailed feedback is organized by resume sections

### 3. Download Report
- Click "Download PDF Report" to save the analysis
- The report includes all feedback and suggestions

## Testing

### Run Unit Tests
```bash
pytest tests/unit/
```

### Run Integration Tests
```bash
pytest tests/integration/
```

### Run All Tests
```bash
pytest tests/
```

## Key Endpoints/Commands
- File upload: `POST /upload` (handled by Streamlit)
- Analysis: Triggered by the "Analyze" button
- PDF export: Triggered by the "Download" button

## Troubleshooting

### Common Issues
- **File upload fails**: Check file type (PDF/DOCX) and size (<10MB)
- **Analysis takes too long**: Verify Gemini API connectivity
- **PDF generation fails**: Check report template permissions
- **Session timeout**: Files are automatically cleaned up after 24 hours