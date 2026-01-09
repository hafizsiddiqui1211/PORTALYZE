# Data Model: Portfolio + LinkedIn / GitHub Integration

## Entities

### ProfileURL
- **url_id**: UUID, unique identifier for the URL record
- **url**: string, the validated URL
- **profile_type**: enum (LINKEDIN, GITHUB, PORTFOLIO), type of profile
- **is_valid**: boolean, whether URL format is valid
- **is_accessible**: boolean, whether URL is accessible
- **validation_timestamp**: datetime, when validation was performed
- **session_id**: string, session identifier for cleanup
- **error_message**: string (optional), validation error details

**Validation rules**:
- url must be a valid URL format
- profile_type must be one of the defined enums
- LinkedIn URLs must match pattern `linkedin.com/in/*`
- GitHub URLs must match pattern `github.com/*`
- Portfolio URLs must be valid HTTP/HTTPS URLs

### ProfileData
- **profile_id**: UUID, unique identifier for the profile data
- **url_id**: UUID, foreign key to ProfileURL
- **profile_type**: enum (LINKEDIN, GITHUB, PORTFOLIO), type of profile
- **raw_content**: string, raw extracted HTML/text content
- **normalized_content**: object, structured extracted data
- **extraction_timestamp**: datetime, when extraction was performed
- **extraction_status**: enum (SUCCESS, PARTIAL, FAILED), extraction result
- **limitations**: array of strings, any parsing limitations encountered

**LinkedIn-specific fields** (in normalized_content):
- headline: string
- summary: string
- experience_highlights: array of objects
- skills: array of strings

**GitHub-specific fields** (in normalized_content):
- username: string
- bio: string
- repositories: array of objects (name, description, stars, forks, language, readme_snippet)
- total_stars: number
- recent_activity: array of strings
- top_languages: array of strings

**Portfolio-specific fields** (in normalized_content):
- site_title: string
- bio_about: string
- projects: array of objects (name, description, technologies, links)
- skills: array of strings
- contact_visible: boolean
- pages_analyzed: number

**Validation rules**:
- profile_type must match parent ProfileURL type
- normalized_content must contain required fields for profile type
- extraction_status must be one of the defined enums

### AnalysisResult (Extended from Phase 1)
- **analysis_id**: UUID, unique identifier for the analysis
- **session_id**: string, session identifier
- **profile_analyses**: array of ProfileAnalysis objects
- **alignment_score**: float (0-100), resume-profile alignment percentage
- **alignment_details**: object, detailed alignment breakdown
- **overall_suggestions**: array of strings, cross-platform suggestions
- **analysis_timestamp**: datetime, when analysis was completed
- **confidence_level**: float (0-1), confidence in the analysis

### ProfileAnalysis
- **profile_analysis_id**: UUID, unique identifier
- **profile_id**: UUID, foreign key to ProfileData
- **profile_type**: enum (LINKEDIN, GITHUB, PORTFOLIO)
- **strengths**: array of strings, identified strengths
- **weaknesses**: array of strings, identified weaknesses
- **suggestions**: array of ImprovementSuggestion objects
- **clarity_score**: float (0-100), profile clarity rating
- **impact_score**: float (0-100), profile impact rating

### ImprovementSuggestion
- **suggestion_id**: UUID, unique identifier
- **profile_analysis_id**: UUID, foreign key to ProfileAnalysis
- **category**: enum (CONTENT, FORMATTING, VISIBILITY, ALIGNMENT, TECHNICAL)
- **priority**: enum (HIGH, MEDIUM, LOW)
- **suggestion_text**: string, the actionable suggestion
- **rationale**: string, why this suggestion matters
- **example**: string (optional), example of improvement
- **affected_section**: string, which profile section this affects

**Validation rules**:
- category must be one of the defined enums
- priority must be one of the defined enums
- suggestion_text must be non-empty
- rationale must be non-empty

### AlignmentResult
- **alignment_id**: UUID, unique identifier
- **analysis_id**: UUID, foreign key to AnalysisResult
- **resume_id**: UUID (optional), foreign key to Phase 1 Resume
- **overall_score**: float (0-100), overall alignment percentage
- **skill_alignment**: object, skill-by-skill comparison
- **experience_alignment**: object, experience comparison
- **project_alignment**: object, project comparison
- **discrepancies**: array of strings, notable differences
- **recommendations**: array of strings, alignment improvement suggestions

## Relationships

```
ProfileURL (1) → (0..1) ProfileData
ProfileData (1) → (0..1) ProfileAnalysis
AnalysisResult (1) → (0..*) ProfileAnalysis
AnalysisResult (1) → (0..1) AlignmentResult
ProfileAnalysis (1) → (0..*) ImprovementSuggestion
```

## State Transitions

### ProfileURL States
```
PENDING → VALIDATING → VALID/INVALID
VALID → ACCESSIBLE/INACCESSIBLE
```

### ProfileData States
```
PENDING → EXTRACTING → SUCCESS/PARTIAL/FAILED
```

### AnalysisResult States
```
PENDING → IN_PROGRESS → COMPLETED → EXPORTED/ARCHIVED
```