# Implementation Plan: Portfolio + LinkedIn / GitHub Integration

**Branch**: `002-portfolio-linkedin-github-integration` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-portfolio-linkedin-github-integration/spec.md`

## Summary

Portfolio + LinkedIn / GitHub Integration is Phase 2 of the Smart Resume & Portfolio Analyzer. This feature enables users to submit Portfolio, LinkedIn, and GitHub URLs, extract and normalize public profile data, and generate AI-driven, actionable improvement suggestions. The implementation strengthens professional presence analysis and complements the resume insights from Phase 1.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: Streamlit, requests, BeautifulSoup4, PyGithub (GitHub API), httpx (async HTTP), google-generativeai (for Gemini API analysis)
**Storage**: In-memory processing with temporary encrypted file storage (24-hour auto-delete)
**Testing**: pytest for unit tests, Streamlit's testing utilities, responses/httpretty for mocking HTTP
**Target Platform**: Web application (multi-platform via browser)
**Project Type**: Single web application (extension of Phase 1)
**Performance Goals**: Analysis completes within 20 seconds per profile, URL validation within 2 seconds
**Constraints**: Public data only, no authenticated scraping, respect platform rate limits, main page + linked projects only for portfolios
**Scale/Scope**: Single-user session-based processing, integrated with Phase 1 dashboard

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status |
|-----------|-------------|--------|
| **Accuracy** | Profile insights must reflect actual public content | PASS |
| **Actionable Feedback** | Suggestions must be practical, specific, and measurable | PASS |
| **User-Centric Clarity** | Feedback presented in concise, visually structured manner | PASS |
| **AI-Assisted Intelligence** | Recommendations leverage AI reasoning and pattern analysis | PASS |
| **Data Privacy** | Secure handling, no permanent storage without consent | PASS |
| **Performance** | Analysis within reasonable time (20 seconds) | PASS |

## Project Structure

### Documentation (this feature)

```text
specs/002-portfolio-linkedin-github-integration/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/
├── main.py              # Streamlit app entry point (extended)
├── models/
│   ├── profile_url.py   # ProfileURL entity (NEW)
│   ├── profile_data.py  # ProfileData entity (NEW)
│   └── improvement.py   # ImprovementSuggestion entity (NEW)
├── services/
│   ├── url_validator.py     # URL validation service (NEW)
│   ├── profile_extractor.py # Base profile extraction (NEW)
│   ├── linkedin_extractor.py # LinkedIn data extraction (NEW)
│   ├── github_extractor.py  # GitHub data extraction (NEW)
│   ├── portfolio_extractor.py # Portfolio site extraction (NEW)
│   ├── alignment_analyzer.py # Resume-profile alignment (NEW)
│   └── rate_limiter.py      # Rate limiting with backoff (NEW)
├── ui/
│   ├── components/
│   │   ├── url_input.py     # URL input components (NEW)
│   │   ├── profile_display.py # Profile data display (NEW)
│   │   └── alignment_view.py # Alignment score display (NEW)
│   └── dashboard.py         # Dashboard UI logic (extended)
└── utils/
    ├── http_client.py       # HTTP client with retry logic (NEW)
    └── constants.py         # Application constants (extended)

tests/
├── unit/
│   └── test_services/
│       ├── test_url_validator.py
│       ├── test_linkedin_extractor.py
│       ├── test_github_extractor.py
│       ├── test_portfolio_extractor.py
│       └── test_alignment_analyzer.py
├── integration/
│   └── test_profile_flow.py
└── conftest.py
```

**Structure Decision**: Extension of Phase 1 single project structure with new extractors for each profile type and alignment analysis service.

## Execution Phases

### Phase A: Research
- Public data availability and access limits for LinkedIn, GitHub, and websites
- Best practices for portfolio and GitHub signaling in hiring
- Rate limiting patterns and retry strategies
- Normalization strategies for heterogeneous web content

### Phase B: Foundation
- Streamlit URL input and validation UI
- Accessibility checks and error handling
- Secure, encrypted temporary storage setup
- Base extraction pipelines for each profile type

### Phase C: Analysis
- Integrate Gemini API for profile evaluation
- Implement GitHub repository scoring heuristics
- Resume-profile alignment logic
- Graceful degradation for partial or minimal data
- AI unavailability handling with user messaging

### Phase D: Synthesis
- Dashboard integration with Phase 1 results
- Sectioned, scannable presentation of insights
- Performance optimization for 20s analysis target
- Final UX polish and edge-case handling

## Architecture Decisions

### Decision 1: Profile Data Scope
- **Chosen**: Option B - Limit to main page + key sections
- **Rationale**: Predictable performance, manageable complexity, aligns with 20-second target
- **Alternatives Rejected**: Full site crawling (performance risk, noise)

### Decision 2: Rate Limiting Strategy
- **Chosen**: Option B - Retry with exponential backoff + notify user
- **Rationale**: Resilient, transparent UX, handles transient failures
- **Alternatives Rejected**: Fail fast (poor user experience)

### Decision 3: Resume Alignment Depth
- **Chosen**: Option B - Skills + project + experience comparison
- **Rationale**: High value insights, meaningful alignment scoring
- **Alternatives Rejected**: Keyword-only (shallow, less actionable)

## Testing Strategy

### Validation Checks
- Valid URLs accepted and processed
- Invalid URL formats rejected with clear messaging
- Inaccessible URLs handled gracefully with explanation
- Extracted data matches visible public content
- GitHub high-signal repos correctly identified
- Suggestions are specific, actionable, and role-aware
- Resume alignment scores generated correctly
- Analysis completes ≤20 seconds for 90% of cases
- Rate limits trigger retries and user notification
- Encrypted profile data auto-deleted after 24 hours
- Dashboard integrates seamlessly with Phase 1 output

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | All constitution checks pass | N/A |