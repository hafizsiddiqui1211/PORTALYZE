# Data Model: Resume Analyzer Core

## Entities

### Resume
- **resume_id**: UUID, unique identifier for the resume session
- **original_filename**: string, name of uploaded file
- **file_type**: enum (PDF, DOCX), type of uploaded document
- **file_path**: string, temporary encrypted storage path
- **text_content**: string, extracted text from the resume
- **metadata**: object, extracted metadata (creation date, author, etc.)
- **upload_timestamp**: datetime, when the file was uploaded
- **session_id**: string, session identifier for cleanup

**Validation rules**:
- file_type must be PDF or DOCX
- file_path must exist and be readable
- text_content must not be empty after extraction
- file size must be ≤ 10MB

### AnalysisResult
- **analysis_id**: UUID, unique identifier for the analysis
- **resume_id**: UUID, foreign key to Resume
- **ats_score**: float (0-100), ATS compatibility percentage
- **strengths**: array of strings, identified strengths in the resume
- **weaknesses**: array of strings, identified weaknesses in the resume
- **section_feedback**: object, feedback organized by resume sections
- **overall_feedback**: string, summary feedback
- **analysis_timestamp**: datetime, when analysis was completed
- **confidence_level**: float (0-1), confidence in the analysis

**Validation rules**:
- ats_score must be between 0 and 100
- strengths array must have at least 1 item
- weaknesses array must have at least 1 item
- section_feedback must include at least 'experience', 'skills', 'education' keys

### KeywordSuggestion
- **suggestion_id**: UUID, unique identifier for the suggestion
- **analysis_id**: UUID, foreign key to AnalysisResult
- **keyword**: string, suggested keyword
- **relevance_score**: float (0-1), how relevant the keyword is
- **category**: enum (Technical, SoftSkill, IndustrySpecific), type of keyword
- **justification**: string, why this keyword is suggested
- **role_alignment**: string, which roles this keyword aligns with

**Validation rules**:
- keyword must be non-empty
- relevance_score must be between 0 and 1
- category must be one of the defined enums
- justification must be non-empty

## Relationships
- Resume (1) → (0..1) AnalysisResult (one resume can have one analysis result)
- AnalysisResult (1) → (0..*) KeywordSuggestion (one analysis can have multiple keyword suggestions)

## State Transitions
- Resume: UPLOADING → EXTRACTED → ANALYZED → ARCHIVED/DELETED
- AnalysisResult: PENDING → IN_PROGRESS → COMPLETED → EXPORTED