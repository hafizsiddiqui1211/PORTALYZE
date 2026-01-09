# Implementation Plan: Job Role Recommender

**Branch**: `003-job-role-recommender` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-job-role-recommender/spec.md`

## Summary

Job Role Recommender is Phase 3 of the Smart Resume & Portfolio Analyzer. This feature synthesizes insights from resume analysis (Phase 1) and portfolio/LinkedIn/GitHub analysis (Phase 2) to suggest high-fit roles, provide clear justification, detect seniority, and highlight skill gaps—helping users confidently position themselves in the job market.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: Streamlit, SpeckitPlus/Claude CLI (for AI analysis), pydantic (data validation), yaml (knowledge base)
**Storage**: In-memory processing with temporary anonymized storage (24-hour auto-delete, consent-based)
**Testing**: pytest for unit tests, Streamlit's testing utilities
**Target Platform**: Web application (multi-platform via browser)
**Project Type**: Single web application (extension of Phases 1 & 2)
**Performance Goals**: Role recommendations generated within 30 seconds, 2-5 roles per industry
**Constraints**: No job listings/salary data, no detailed learning paths, public data synthesis only
**Scale/Scope**: Single-user session-based processing, integrated with Phases 1 & 2 dashboard

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status |
|-----------|-------------|--------|
| **Accuracy** | Role recommendations reflect actual skills and experience | PASS |
| **Actionable Feedback** | Clear justification and gap analysis for each role | PASS |
| **User-Centric Clarity** | Scannable role cards with understandable reasoning | PASS |
| **AI-Assisted Intelligence** | Claude CLI for role inference and seniority detection | PASS |
| **Data Privacy** | Anonymized temporary storage with consent, 24h auto-delete | PASS |
| **Performance** | Recommendations within 30 seconds | PASS |

## Project Structure

### Documentation (this feature)

```text
specs/003-job-role-recommender/
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
│   ├── industry.py          # IndustrySelection entity (NEW)
│   ├── profile_signals.py   # ProfileSignals aggregation (NEW)
│   ├── role_recommendation.py # RoleRecommendation entity (NEW)
│   └── gap_analysis.py      # GapAnalysis entity (NEW)
├── services/
│   ├── signal_aggregator.py   # Aggregate Phase 1 & 2 signals (NEW)
│   ├── role_inferencer.py     # AI-driven role inference (NEW)
│   ├── seniority_detector.py  # Seniority level detection (NEW)
│   ├── gap_analyzer.py        # Skill gap analysis (NEW)
│   ├── knowledge_base.py      # Role archetype knowledge (NEW)
│   └── consent_manager.py     # Consent and anonymization (NEW)
├── ui/
│   ├── components/
│   │   ├── industry_selector.py  # Industry selection UI (NEW)
│   │   ├── role_card.py          # Role recommendation card (NEW)
│   │   ├── gap_display.py        # Gap analysis display (NEW)
│   │   └── confidence_badge.py   # Confidence indicators (NEW)
│   └── dashboard.py              # Dashboard UI logic (extended)
├── knowledge/
│   ├── industries/               # Industry-specific role data (NEW)
│   │   ├── ai_ml.yaml
│   │   ├── software_engineering.yaml
│   │   ├── data.yaml
│   │   ├── fintech.yaml
│   │   └── edtech.yaml
│   └── archetypes.yaml          # Role archetype definitions (NEW)
└── utils/
    ├── anonymizer.py            # Data anonymization utilities (NEW)
    └── constants.py             # Application constants (extended)

tests/
├── unit/
│   └── test_services/
│       ├── test_signal_aggregator.py
│       ├── test_role_inferencer.py
│       ├── test_seniority_detector.py
│       └── test_gap_analyzer.py
├── integration/
│   └── test_role_recommendation_flow.py
└── conftest.py
```

**Structure Decision**: Extension of Phases 1 & 2 structure with new role inference services and a knowledge base layer for industry-specific role archetypes.

## Execution Phases

### Phase A: Research
- Industry role archetypes and common expectations
- Signals mapping between skills/projects and roles
- Seniority inference heuristics
- Handling ambiguous or conflicting profile data
- Best practices for explaining AI recommendations to users

### Phase B: Foundation
- Streamlit industry and specialization selectors
- ProfileSignals aggregation from Phases 1 and 2
- Temporary anonymized storage with consent handling
- Base role archetype knowledge structure

### Phase C: Analysis
- Integrate Claude CLI for role inference
- Industry-constrained role recommendation logic
- Justification generation (skills, projects, tools)
- Seniority detection implementation
- Gap analysis and high-level improvement suggestions
- Graceful handling of minimal or conflicting data
- AI unavailability handling with retry and messaging

### Phase D: Synthesis
- Dashboard presentation and UX refinement
- Grouping and scannability of role cards
- Confidence indicators for recommendations
- Performance optimization (≤30 seconds)
- Seamless integration with Phase 1 & 2 outputs

## Architecture Decisions

### Decision 1: Role Recommendation Scope
- **Chosen**: Option B - Multiple roles (2-5) with justification
- **Rationale**: Reflects real-world ambiguity, provides higher value by showing range of options
- **Alternatives Rejected**: Single best-fit role (ignores multidimensional profiles)

### Decision 2: Handling Conflicting Profile Signals
- **Chosen**: Option B - Present multiple role paths with explanation
- **Rationale**: Transparent, user-empowering, acknowledges career flexibility
- **Alternatives Rejected**: Prioritize strongest signal only (loses alternative paths)

### Decision 3: Seniority Detection
- **Chosen**: Option B - AI-inferred seniority from experience depth
- **Rationale**: Objective assessment based on actual profile data, adds value
- **Alternatives Rejected**: User-declared seniority (inconsistent accuracy)

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | All constitution checks pass | N/A |