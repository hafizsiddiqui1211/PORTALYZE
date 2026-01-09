# Data Model: Job Role Recommender

## Entities

### IndustrySelection
- **selection_id**: UUID, unique identifier
- **session_id**: string, session identifier
- **industries**: array of strings, selected industries (e.g., ["AI/ML", "Software Engineering"])
- **specializations**: array of strings (optional), sub-domains selected
- **selection_timestamp**: datetime, when selection was made

**Validation rules**:
- industries array must have at least 1 item
- industries must be from predefined list (AI/ML, Software Engineering, Data, FinTech, EdTech, etc.)
- specializations must be valid for selected industries

### ProfileSignals
- **signals_id**: UUID, unique identifier
- **session_id**: string, session identifier
- **resume_signals**: ResumeSignals object, from Phase 1
- **profile_signals**: ProfileSignalsSet object, from Phase 2
- **aggregated_skills**: array of SkillSignal objects
- **experience_summary**: ExperienceSummary object
- **project_highlights**: array of ProjectSignal objects
- **is_anonymized**: boolean, whether PII has been removed
- **consent_given**: boolean, whether user consented to storage
- **aggregation_timestamp**: datetime, when aggregation occurred

**ResumeSignals** (nested object):
- ats_score: float (0-100)
- extracted_skills: array of strings
- experience_years: number
- education_level: string
- key_achievements: array of strings

**ProfileSignalsSet** (nested object):
- linkedin_signals: object (headline, summary_keywords, experience_highlights)
- github_signals: object (top_languages, repo_count, total_stars, contribution_pattern)
- portfolio_signals: object (project_types, technologies_used, portfolio_quality_score)

**SkillSignal** (nested object):
- skill_name: string
- proficiency_indicator: enum (MENTIONED, DEMONSTRATED, EXPERT)
- sources: array of strings (e.g., ["resume", "github", "linkedin"])
- validation_strength: float (0-1)

**ExperienceSummary** (nested object):
- total_years: number
- domains: array of strings
- leadership_indicators: array of strings
- scale_indicators: array of strings (team size, project scope)

**ProjectSignal** (nested object):
- project_name: string
- technologies: array of strings
- complexity_level: enum (SIMPLE, MODERATE, COMPLEX)
- impact_description: string

### RoleRecommendation
- **recommendation_id**: UUID, unique identifier
- **session_id**: string, session identifier
- **industry_selection_id**: UUID, foreign key to IndustrySelection
- **signals_id**: UUID, foreign key to ProfileSignals
- **roles**: array of RecommendedRole objects (2-5 items)
- **overall_confidence**: enum (HIGH, MEDIUM, LOW)
- **confidence_factors**: array of strings, what affects confidence
- **recommendation_timestamp**: datetime, when generated

**RecommendedRole** (nested object):
- role_id: UUID
- role_title: string (e.g., "AI App Developer", "ML Engineer")
- industry: string
- seniority_level: enum (JUNIOR, MID, SENIOR)
- fit_score: float (0-100)
- justification: RoleJustification object
- gap_analysis: GapAnalysis object

**RoleJustification** (nested object):
- summary: string (1-2 sentence overview)
- skill_alignment: array of strings (matching skills)
- project_relevance: array of strings (relevant projects)
- technology_match: array of strings (matching technologies)
- experience_alignment: string (how experience fits)

### GapAnalysis
- **gap_id**: UUID, unique identifier
- **role_id**: UUID, foreign key to RecommendedRole
- **missing_skills**: array of SkillGap objects (2-4 items)
- **improvement_suggestions**: array of strings (high-level, no curriculum)
- **priority_areas**: array of strings (most important gaps)

**SkillGap** (nested object):
- skill_name: string
- importance_level: enum (CRITICAL, IMPORTANT, NICE_TO_HAVE)
- current_level: string (optional, if partially present)
- target_level: string
- brief_suggestion: string (1 sentence improvement hint)

### RoleArchetype (Knowledge Base)
- **archetype_id**: string, unique identifier
- **role_title**: string
- **industry**: string
- **description**: string
- **required_skills**: array of SkillRequirement objects
- **experience_markers**: ExperienceMarkers object
- **seniority_indicators**: SeniorityIndicators object
- **typical_titles**: array of strings (variations of role title)

**SkillRequirement** (nested object):
- skill_name: string
- importance: enum (CORE, PREFERRED, BONUS)
- alternatives: array of strings (equivalent skills)

**SeniorityIndicators** (nested object):
- junior_markers: array of strings
- mid_markers: array of strings
- senior_markers: array of strings

## Relationships

```
IndustrySelection (1) → (1) RoleRecommendation
ProfileSignals (1) → (1) RoleRecommendation
RoleRecommendation (1) → (2..*) RecommendedRole
RecommendedRole (1) → (1) GapAnalysis
RoleArchetype (reference) → (0..*) RecommendedRole
```

## State Transitions

### ProfileSignals States
```
PENDING → AGGREGATING → AGGREGATED → ANONYMIZED (if consented)
```

### RoleRecommendation States
```
PENDING → INFERRING → COMPLETED → DISPLAYED
```

### Consent States
```
NOT_REQUESTED → REQUESTED → GRANTED/DENIED
GRANTED → STORED → AUTO_DELETED (after 24h)
```