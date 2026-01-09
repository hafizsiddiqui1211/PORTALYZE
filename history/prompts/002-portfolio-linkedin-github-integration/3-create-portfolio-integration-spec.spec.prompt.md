---
id: 3
title: Create portfolio integration spec
stage: spec
date: 2025-12-28
surface: agent
model: Claude Sonnet 4.5
feature: 002-portfolio-linkedin-github-integration
branch: 002-portfolio-linkedin-github-integration
user: User
command: /sp.specify
labels:
  - specification
  - portfolio-integration
  - linkedin-github
links:
  spec: specs/002-portfolio-linkedin-github-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-portfolio-linkedin-github-integration/spec.md
  - specs/002-portfolio-linkedin-github-integration/checklists/requirements.md
tests: []
---

# Prompt

```
/sp.specify

## Spec-2: Phase 2 – Portfolio + LinkedIn / GitHub Integration

### Target Audience
- Professionals with online portfolios (personal websites)
- LinkedIn users seeking profile optimization
- GitHub users showcasing technical projects and repositories
- Freelancers and AI engineers improving professional visibility

### Focus
- External profile ingestion via URLs
- AI-driven analysis of professional presence
- Actionable improvement suggestions for portfolios, LinkedIn profiles, and GitHub repositories
- Alignment of online profiles with resume and ATS expectations

### Functional Scope
1. **Profile URL Input**
   - Accept Portfolio website URL
   - Accept LinkedIn profile URL and/or GitHub profile URL
   - Validate URL format and accessibility
   - Session-based handling without permanent scraping storage by default

2. **Profile Data Extraction**
   - Pull and summarize:
     - LinkedIn: headline, summary/about section, experience highlights
     - GitHub: repositories, README content, stars, forks, recent activity
     - Portfolio website: bio/about section, projects, skills, contact visibility
   - Normalize extracted data into structured text blocks for AI analysis

3. **AI Portfolio Analyzer**
   - Evaluate clarity and impact of profile summaries
   - Identify missing or weak elements (metrics, outcomes, role clarity)
   - Analyze GitHub repositories for:
     - Relevance
     - Visibility (stars, README quality)
     - Project signaling strength
   - Cross-check alignment between resume (Phase 1) and online presence

4. **Improvement Suggestions**
   - Portfolio recommendations (e.g., “Add measurable results to projects”)
   - LinkedIn optimization tips (e.g., “Rewrite headline with role + impact”)
   - GitHub suggestions (e.g., “Highlight top-starred repositories”, “Improve README clarity”)
   - Prioritized, actionable, and role-aware guidance

5. **Results Presentation**
   - Display insights within Streamlit dashboard
   - Separate sections for Portfolio, LinkedIn, and GitHub
   - Clear improvement checklist format

### Success Criteria
- URLs are correctly validated and parsed
- AI-generated summaries accurately reflect profile content
- Suggestions are specific, actionable, and professionally relevant
- GitHub insights correctly identify high-signal repositories
- Feedback clearly improves profile credibility and hiring appeal
- Output integrates smoothly with Phase 1 resume analysis

### Constraints
- Tech stack:
  - Frontend: Streamlit
  - Backend: Python
  - AI analysis: Claude CLI via SpeckitPlus
- Must not require user login to external platforms
- Respect platform access limits and public data boundaries
- Analysis runtime per profile: ≤ 20 seconds
- Output internally structured as Markdown, rendered via Streamlit

### Not Building (Out of Scope)
- Automated posting or editing of LinkedIn/GitHub profiles
- Private or authenticated data access
- Real-time social metrics tracking
- Job role recommendation logic (handled in Phase 3)
- Monetization features or subscription gating
- Public shareable profile analysis links
```

# Response

Successfully created the feature specification for Portfolio + LinkedIn / GitHub Integration at specs/002-portfolio-linkedin-github-integration/spec.md.

The specification includes:
- Three user stories prioritized as P1 (Profile URL Input and Validation), P2 (Profile Data Extraction and Normalization), and P3 (AI-Driven Profile Analysis and Suggestions)
- Functional requirements covering URL validation, data extraction from LinkedIn/GitHub/portfolio sites, AI analysis, and improvement suggestions
- Success criteria with measurable outcomes for accuracy, performance, relevance, and integration
- Edge cases for privacy settings, complex layouts, and service availability
- Key entities: ProfileURL, ProfileData, AnalysisResult, and ImprovementSuggestion

The specification follows the template structure and maintains focus on user value without implementation details. A quality checklist was also created to validate the specification completeness.