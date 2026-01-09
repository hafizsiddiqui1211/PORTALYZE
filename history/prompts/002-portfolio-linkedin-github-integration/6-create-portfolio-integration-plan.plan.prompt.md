---
id: 6
title: Create portfolio integration plan
stage: plan
date: 2025-12-28
surface: agent
model: Claude Sonnet 4.5
feature: 002-portfolio-linkedin-github-integration
branch: 002-portfolio-linkedin-github-integration
user: User
command: /sp.plan
labels:
  - planning
  - architecture
  - portfolio-integration
  - linkedin
  - github
links:
  spec: specs/002-portfolio-linkedin-github-integration/spec.md
  plan: specs/002-portfolio-linkedin-github-integration/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-portfolio-linkedin-github-integration/plan.md
  - specs/002-portfolio-linkedin-github-integration/research.md
  - specs/002-portfolio-linkedin-github-integration/data-model.md
  - specs/002-portfolio-linkedin-github-integration/quickstart.md
  - specs/002-portfolio-linkedin-github-integration/contracts/api-contract.md
tests: []
---

# Prompt

```
/sp.plan

## Feature
**Portfolio + LinkedIn / GitHub Integration (Spec-2 – Phase 2)**
Feature Branch: `002-portfolio-linkedin-github-integration`

---

## Objective
Plan and execute Phase 2 of the Smart Resume & Portfolio Analyzer by enabling users to submit Portfolio, LinkedIn, and GitHub URLs, extract and normalize public profile data, and generate AI-driven, actionable improvement suggestions. This phase strengthens professional presence analysis and complements the resume insights from Phase 1.

---

## Plan Structure

### 1. Architecture Sketch
- **UI Layer**
  - Streamlit input components for URLs (Portfolio, LinkedIn, GitHub)
  - Validation feedback and error messaging
  - Dashboard sections for each profile type
  - Integrated view alongside Phase 1 resume insights

- **Processing Layer**
  - URL validation and accessibility checks
  - Rate-limit aware fetch layer with retry and backoff
  - Content extraction services for LinkedIn, GitHub, Portfolio

---

## Decisions
- Decision 1: Profile Data Scope - Chosen Option B (main page + key sections)
- Decision 2: Rate Limiting Strategy - Chosen Option B (retry with exponential backoff)
- Decision 3: Resume Alignment Depth - Chosen Option B (skills + project + experience comparison)
```

# Response

Successfully created the implementation plan for Portfolio + LinkedIn / GitHub Integration. The following artifacts were generated:

1. **plan.md** - Complete implementation plan with technical context, constitution check, project structure, and execution phases
2. **research.md** - Research findings with technology decisions for LinkedIn/GitHub/Portfolio extraction, rate limiting, and alignment analysis
3. **data-model.md** - Detailed data model with ProfileURL, ProfileData, ProfileAnalysis, ImprovementSuggestion, and AlignmentResult entities
4. **quickstart.md** - Setup and usage instructions including new dependencies and configuration
5. **contracts/api-contract.md** - API contracts for URL validation, profile extraction, and analysis endpoints

Key architecture decisions:
- BeautifulSoup4 for LinkedIn/Portfolio scraping
- PyGithub for GitHub API integration
- Exponential backoff with tenacity for rate limiting
- Semantic similarity for resume-profile alignment
- Graceful degradation for partial extraction

The plan extends Phase 1 structure with new extractors for each profile type and integrates seamlessly with the existing dashboard.