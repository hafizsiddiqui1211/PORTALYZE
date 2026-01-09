# API Contract: Job Role Recommender

## Overview
This document defines the API contracts for the Job Role Recommender feature. Since this is a Streamlit application, the "API" consists of the functional endpoints and data flows within the application.

## Endpoints

### Industry Selection
**Endpoint**: Internal function triggered by industry selector UI
**Purpose**: Capture user's target industries and specializations

**Input**:
```json
{
  "industries": ["string"],
  "specializations": ["string"] | null,
  "session_id": "string"
}
```

**Output**:
```json
{
  "selection_id": "UUID",
  "industries": ["string"],
  "specializations": ["string"] | null,
  "available_roles_count": "number",
  "selection_timestamp": "ISO8601"
}
```

### Signal Aggregation
**Endpoint**: Internal function triggered before role inference
**Purpose**: Aggregate signals from Phase 1 and Phase 2 analyses

**Input**:
```json
{
  "session_id": "string",
  "resume_analysis_id": "UUID",
  "profile_analysis_ids": ["UUID"]
}
```

**Output**:
```json
{
  "signals_id": "UUID",
  "aggregated_skills": [
    {
      "skill_name": "string",
      "proficiency_indicator": "MENTIONED | DEMONSTRATED | EXPERT",
      "sources": ["string"],
      "validation_strength": "number (0-1)"
    }
  ],
  "experience_summary": {
    "total_years": "number",
    "domains": ["string"],
    "leadership_indicators": ["string"],
    "scale_indicators": ["string"]
  },
  "project_highlights": [
    {
      "project_name": "string",
      "technologies": ["string"],
      "complexity_level": "SIMPLE | MODERATE | COMPLEX",
      "impact_description": "string"
    }
  ],
  "data_completeness": {
    "has_resume": "boolean",
    "has_linkedin": "boolean",
    "has_github": "boolean",
    "has_portfolio": "boolean"
  },
  "aggregation_timestamp": "ISO8601"
}
```

### Role Inference
**Endpoint**: Internal function triggered by "Get Role Recommendations" button
**Purpose**: Generate AI-driven role recommendations

**Input**:
```json
{
  "signals_id": "UUID",
  "selection_id": "UUID",
  "session_id": "string"
}
```

**Output**:
```json
{
  "recommendation_id": "UUID",
  "roles": [
    {
      "role_id": "UUID",
      "role_title": "string",
      "industry": "string",
      "seniority_level": "JUNIOR | MID | SENIOR",
      "fit_score": "number (0-100)",
      "justification": {
        "summary": "string",
        "skill_alignment": ["string"],
        "project_relevance": ["string"],
        "technology_match": ["string"],
        "experience_alignment": "string"
      },
      "gap_analysis": {
        "missing_skills": [
          {
            "skill_name": "string",
            "importance_level": "CRITICAL | IMPORTANT | NICE_TO_HAVE",
            "brief_suggestion": "string"
          }
        ],
        "improvement_suggestions": ["string"],
        "priority_areas": ["string"]
      }
    }
  ],
  "overall_confidence": "HIGH | MEDIUM | LOW",
  "confidence_factors": ["string"],
  "recommendation_timestamp": "ISO8601"
}
```

### Consent Management
**Endpoint**: Internal function triggered by consent dialog
**Purpose**: Manage user consent for temporary data storage

**Input**:
```json
{
  "session_id": "string",
  "consent_given": "boolean",
  "consent_scope": "ROLE_RECOMMENDATIONS"
}
```

**Output**:
```json
{
  "consent_id": "UUID",
  "consent_status": "GRANTED | DENIED",
  "expiry_timestamp": "ISO8601 | null",
  "storage_enabled": "boolean"
}
```

## Error Handling

### Standard Error Format
```json
{
  "error_code": "string",
  "message": "string",
  "details": "string | null",
  "retry_available": "boolean"
}
```

### Error Codes
| Code | Description |
|------|-------------|
| `INSUFFICIENT_DATA` | Not enough profile data to generate recommendations |
| `INVALID_INDUSTRY` | Selected industry not in supported list |
| `AGGREGATION_FAILED` | Failed to aggregate signals from phases |
| `INFERENCE_TIMEOUT` | Role inference exceeded 30 second limit |
| `AI_SERVICE_UNAVAILABLE` | Claude API not accessible |
| `KNOWLEDGE_BASE_ERROR` | Failed to load role archetypes |
| `SESSION_EXPIRED` | Session data no longer available |
| `CONSENT_REQUIRED` | Storage requires user consent |

## Confidence Calculation

### Confidence Factors
```json
{
  "HIGH": {
    "requirements": [
      "All phases complete (resume + profiles)",
      "Signal consistency > 80%",
      "Experience data present",
      "Skills validated across sources"
    ]
  },
  "MEDIUM": {
    "requirements": [
      "Resume + at least one profile",
      "Signal consistency > 50%",
      "Some experience indicators",
      "Key skills present"
    ]
  },
  "LOW": {
    "requirements": [
      "Resume only OR profiles only",
      "Signal consistency < 50%",
      "Limited experience data",
      "Sparse skill information"
    ]
  }
}
```

## Knowledge Base Schema

### Industry File Structure
```yaml
industry: "string"
specializations:
  - name: "string"
    description: "string"
roles:
  - title: "string"
    description: "string"
    typical_titles: ["string"]
    required_skills:
      - name: "string"
        importance: "CORE | PREFERRED | BONUS"
        alternatives: ["string"]
    experience_markers:
      min_years: "number"
      key_experiences: ["string"]
    seniority_indicators:
      junior: ["string"]
      mid: ["string"]
      senior: ["string"]
```

## Security & Privacy

### Anonymization Rules
- Remove all PII (names, emails, phone numbers)
- Replace specific company names with generic labels
- Generalize location data to region level
- Preserve skill and experience patterns

### Storage Rules
- Consent required before any storage
- Maximum retention: 24 hours
- Session-scoped access only
- Automatic deletion on expiry
- No cross-session data sharing without consent