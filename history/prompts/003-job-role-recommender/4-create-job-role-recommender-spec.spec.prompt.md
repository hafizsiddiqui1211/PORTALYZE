---
id: 4
title: Create job role recommender spec
stage: spec
date: 2025-12-28
surface: agent
model: Claude Sonnet 4.5
feature: 003-job-role-recommender
branch: 003-job-role-recommender
user: User
command: /sp.specify
labels:
  - specification
  - job-role-recommender
  - career-advice
links:
  spec: specs/003-job-role-recommender/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-job-role-recommender/spec.md
  - specs/003-job-role-recommender/checklists/requirements.md
tests: []
---

# Prompt

```
/sp.specify

## Spec-3: Phase 3 – Job Role Recommender

### Target Audience
- Job seekers exploring role alignment across industries
- Early- to mid-career professionals planning career transitions
- AI, software, and data professionals refining career direction
- Freelancers identifying high-fit roles for positioning and outreach

### Focus
- Industry-based job role recommendation
- AI-driven mapping between resume/portfolio signals and role requirements
- Clear justification for each suggested role
- Career-alignment insights rather than job listings

### Functional Scope
1. **Industry Selection**
   - User selects one or more industries (e.g., AI/ML, Software Engineering, Data, FinTech, EdTech)
   - Optional sub-domain or specialization selection (if applicable)
   - Industry choice used as a contextual constraint for role inference

2. **AI Role Inference Engine**
   - Analyze inputs from:
     - Resume analysis (Phase 1)
     - Portfolio / LinkedIn / GitHub insights (Phase 2)
   - Map skills, experience, and project signals to role archetypes
   - Identify seniority level indicators (junior, mid, senior where inferable)

3. **Role Recommendations**
   - Suggest 2–5 relevant job roles per industry
   - Provide short, clear reasoning for each role, such as:
     - Skill alignment
     - Project relevance
     - Tooling and technology match
   - Example output:
     - “AI App Developer – strong alignment with Streamlit, FastAPI, and applied AI projects”
     - “Streamlit Engineer – multiple dashboard-based AI tools demonstrated”

4. **Gap Analysis (Lightweight)**
   - Highlight missing or weak skills for each recommended role
   - Provide high-level suggestions (e.g., “Add production deployment experience”)
   - Avoid deep curriculum or learning-path generation (future scope)

5. **Results Presentation**
   - Display recommended roles in Streamlit dashboard
   - Group roles by industry
   - Use concise, scannable cards or lists with justification bullets

### Success Criteria
- Recommended roles are clearly aligned with user skills and experience
- Each role includes understandable justification
- Industry context meaningfully influences recommendations
- Users can articulate “why this role fits me” after viewing results
- Output complements and builds upon Phases 1 and 2

### Constraints
- Tech stack:
```

# Response

Successfully created the feature specification for Job Role Recommender at specs/003-job-role-recommender/spec.md.

The specification includes:
- Three user stories prioritized as P1 (Industry Selection and Role Inference), P2 (AI-Driven Role Mapping and Justification), and P3 (Gap Analysis and Role Alignment Insights)
- Functional requirements covering industry selection, AI analysis, role recommendations, gap analysis, and presentation
- Success criteria with measurable outcomes for alignment, justification, relevance, and integration
- Edge cases for minimal data, conflicting signals, and service availability
- Key entities: IndustrySelection, ProfileSignals, RoleRecommendation, and GapAnalysis

The specification follows the template structure and maintains focus on user value without implementation details. A quality checklist was also created to validate the specification completeness.