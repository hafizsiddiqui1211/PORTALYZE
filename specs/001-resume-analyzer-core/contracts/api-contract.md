# API Contract: Resume Analyzer Core

## Overview
This document defines the API contracts for the Resume Analyzer Core feature. Since this is a Streamlit application, the "API" consists of the functional endpoints and data flows within the application.

## Endpoints

### File Upload
**Endpoint**: `/upload` (handled internally by Streamlit)
**Method**: POST (via Streamlit file_uploader)
**Purpose**: Upload resume files for analysis

**Request**:
- File attachment (PDF or DOCX format)
- File size must be ≤ 10MB
- Form field name: "resume_file"

**Response**:
- Success: File uploaded and validated
- Error: Appropriate error message displayed in UI

### Resume Analysis
**Endpoint**: Internal processing function
**Method**: Internal call when "Analyze" button is clicked
**Purpose**: Process uploaded resume and generate analysis

**Input**:
- Resume file path (from upload)
- Session context

**Output**:
- AnalysisResult object with:
  - ATS score (0-100)
  - Strengths array
  - Weaknesses array
  - Section feedback
  - Keyword suggestions

### PDF Report Generation
**Endpoint**: `/download` (handled internally by Streamlit)
**Method**: GET (via Streamlit download_button)
**Purpose**: Generate and provide downloadable PDF report

**Request**:
- AnalysisResult ID
- Session context

**Response**:
- PDF file with analysis results
- Content-Type: application/pdf

## Data Contracts

### Resume Upload Validation
```
{
  "file_type": "enum(PDF, DOCX)",
  "file_size": "number <= 10485760",  // 10MB
  "file_name": "string with valid extension"
}
```

### Analysis Request
```
{
  "resume_id": "UUID",
  "file_path": "string",
  "session_id": "string"
}
```

### Analysis Result Response
```
{
  "analysis_id": "UUID",
  "ats_score": "number(0-100)",
  "strengths": "string[]",
  "weaknesses": "string[]",
  "section_feedback": {
    "experience": "string",
    "skills": "string",
    "education": "string",
    "projects": "string"
  },
  "overall_feedback": "string",
  "keyword_suggestions": [
    {
      "keyword": "string",
      "relevance_score": "number(0-1)",
      "category": "enum(Technical, SoftSkill, IndustrySpecific)",
      "justification": "string"
    }
  ],
  "confidence_level": "number(0-1)"
}
```

### PDF Generation Request
```
{
  "analysis_id": "UUID",
  "session_id": "string"
}
```

## Error Handling

### Standard Error Format
```
{
  "error_code": "string",
  "message": "string",
  "details": "string (optional)"
}
```

### Common Error Codes
- `INVALID_FILE_TYPE`: File is not PDF or DOCX
- `FILE_TOO_LARGE`: File exceeds 10MB limit
- `FILE_PROCESSING_ERROR`: Error during text extraction
- `AI_SERVICE_UNAVAILABLE`: Claude API is not accessible
- `ANALYSIS_FAILED`: General analysis failure
- `PDF_GENERATION_ERROR`: Error generating PDF report

## Security Considerations
- Files are stored temporarily and encrypted
- Session-based access control
- File type validation on upload
- Input sanitization for all text processing
- Automatic cleanup of temporary files after 24 hours