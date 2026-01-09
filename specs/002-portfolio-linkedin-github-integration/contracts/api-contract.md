# API Contract: Portfolio + LinkedIn / GitHub Integration

## Overview
This document defines the API contracts for the Portfolio + LinkedIn / GitHub Integration feature. Since this is a Streamlit application, the "API" consists of the functional endpoints and data flows within the application.

## Endpoints

### URL Validation
**Endpoint**: Internal function triggered by "Validate URLs" button
**Purpose**: Validate and check accessibility of profile URLs

**Input**:
```json
{
  "urls": [
    {
      "url": "string",
      "profile_type": "LINKEDIN | GITHUB | PORTFOLIO | AUTO"
    }
  ],
  "session_id": "string"
}
```

**Output**:
```json
{
  "results": [
    {
      "url_id": "UUID",
      "url": "string",
      "profile_type": "LINKEDIN | GITHUB | PORTFOLIO",
      "is_valid": "boolean",
      "is_accessible": "boolean",
      "error_message": "string | null",
      "validation_timestamp": "ISO8601"
    }
  ]
}
```

### Profile Extraction
**Endpoint**: Internal function triggered by "Analyze Profiles" button
**Purpose**: Extract and normalize profile data from validated URLs

**Input**:
```json
{
  "url_ids": ["UUID"],
  "session_id": "string"
}
```

**Output**:
```json
{
  "profiles": [
    {
      "profile_id": "UUID",
      "url_id": "UUID",
      "profile_type": "LINKEDIN | GITHUB | PORTFOLIO",
      "extraction_status": "SUCCESS | PARTIAL | FAILED",
      "normalized_content": {
        // Type-specific content (see Data Model)
      },
      "limitations": ["string"],
      "extraction_timestamp": "ISO8601"
    }
  ]
}
```

### Profile Analysis
**Endpoint**: Internal function triggered after extraction
**Purpose**: Generate AI-driven analysis and suggestions

**Input**:
```json
{
  "profile_ids": ["UUID"],
  "resume_id": "UUID | null",
  "session_id": "string"
}
```

**Output**:
```json
{
  "analysis_id": "UUID",
  "profile_analyses": [
    {
      "profile_analysis_id": "UUID",
      "profile_id": "UUID",
      "profile_type": "LINKEDIN | GITHUB | PORTFOLIO",
      "strengths": ["string"],
      "weaknesses": ["string"],
      "suggestions": [
        {
          "suggestion_id": "UUID",
          "category": "CONTENT | FORMATTING | VISIBILITY | ALIGNMENT | TECHNICAL",
          "priority": "HIGH | MEDIUM | LOW",
          "suggestion_text": "string",
          "rationale": "string",
          "example": "string | null",
          "affected_section": "string"
        }
      ],
      "clarity_score": "number (0-100)",
      "impact_score": "number (0-100)"
    }
  ],
  "alignment_score": "number (0-100) | null",
  "alignment_details": {
    "skill_alignment": {},
    "experience_alignment": {},
    "project_alignment": {},
    "discrepancies": ["string"],
    "recommendations": ["string"]
  },
  "overall_suggestions": ["string"],
  "confidence_level": "number (0-1)",
  "analysis_timestamp": "ISO8601"
}
```

## Error Handling

### Standard Error Format
```json
{
  "error_code": "string",
  "message": "string",
  "details": "string | null",
  "retry_after": "number | null"
}
```

### Error Codes
| Code | Description |
|------|-------------|
| `INVALID_URL_FORMAT` | URL format is not valid |
| `URL_INACCESSIBLE` | URL could not be accessed |
| `PROFILE_NOT_PUBLIC` | Profile requires authentication |
| `RATE_LIMITED` | Platform rate limit exceeded |
| `EXTRACTION_FAILED` | Content extraction failed |
| `EXTRACTION_PARTIAL` | Only partial content extracted |
| `AI_SERVICE_UNAVAILABLE` | Gemini API not accessible |
| `ANALYSIS_TIMEOUT` | Analysis exceeded 20s limit |
| `SESSION_EXPIRED` | Session data no longer available |

## Rate Limiting

### Retry Behavior
```json
{
  "retry_strategy": "exponential_backoff",
  "base_delay_seconds": 1,
  "max_delay_seconds": 32,
  "max_retries": 5,
  "jitter": true
}
```

### Platform Limits
| Platform | Unauthenticated Limit | Authenticated Limit |
|----------|----------------------|---------------------|
| GitHub | 60 requests/hour | 5000 requests/hour |
| LinkedIn | Best effort (public) | N/A |
| Portfolio | Per-site limits | N/A |

## Security Considerations

- All extracted data stored encrypted at rest
- Session-based isolation prevents cross-user data access
- Automatic deletion after 24 hours
- No authentication credentials stored
- Public data only - no authenticated scraping
- Rate limiting respects platform ToS