---
id: 7
title: Create job role recommender plan
stage: plan
date: 2025-12-28
surface: agent
model: Claude Sonnet 4.5
feature: 003-job-role-recommender
branch: 003-job-role-recommender
user: User
command: /sp.plan
labels:
  - planning
  - architecture
  - job-role-recommender
  - career-advice
links:
  spec: specs/003-job-role-recommender/spec.md
  plan: specs/003-job-role-recommender/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-job-role-recommender/plan.md
  - specs/003-job-role-recommender/research.md
  - specs/003-job-role-recommender/data-model.md
  - specs/003-job-role-recommender/quickstart.md
  - specs/003-job-role-recommender/contracts/api-contract.md
tests: []
---

# Prompt

```
/sp.plan

## Feature
**Job Role Recommender (Spec-3 – Phase 3)**
Feature Branch: `003-job-role-recommender`

---

## Objective
Plan and execute Phase 3 of the Smart Resume & Portfolio Analyzer by enabling industry-driven job role recommendations. This feature synthesizes insights from resume analysis (Phase 1) and portfolio/LinkedIn/GitHub analysis (Phase 2) to suggest high-fit roles, provide clear justification, detect seniority, and highlight skill gaps—helping users confidently position themselves in the job market.

---

## Plan Structure

### 1. Architecture Sketch
- UI Layer: Industry selection, role cards, confidence indicators
- Context Aggregation Layer: Merge Phase 1 & 2 signals
- AI Role Inference Layer: Claude CLI for role mapping
- Knowledge Base Layer: Industry role archetypes

## Decisions
- Decision 1: Role Recommendation Scope - Chosen Option B (2-5 roles with justification)
- Decision 2: Handling Conflicting Signals - Chosen Option B (present multiple role paths)
- Decision 3: Seniority Detection - Chosen Option B (AI-inferred from experience)
```

# Response

Successfully created the implementation plan for Job Role Recommender. The following artifacts were generated:

1. **plan.md** - Complete implementation plan with technical context, constitution check, project structure, and execution phases
2. **research.md** - Research findings with technology decisions for knowledge base structure, signal aggregation, seniority detection, and role inference
3. **data-model.md** - Detailed data model with IndustrySelection, ProfileSignals, RoleRecommendation, GapAnalysis, and RoleArchetype entities
4. **quickstart.md** - Setup and usage instructions including knowledge base initialization
5. **contracts/api-contract.md** - API contracts for industry selection, signal aggregation, role inference, and consent management

Key architecture decisions:
- YAML-based knowledge base for industry role archetypes (quarterly updates)
- Unified ProfileSignals aggregation from Phases 1 & 2
- Three-tier seniority model (junior/mid/senior) with AI inference
- Structured Claude CLI prompting for role recommendations
- Consent-based anonymized storage with 24-hour auto-delete
- Confidence indicators (High/Medium/Low) based on data completeness

The plan integrates seamlessly with Phases 1 & 2, synthesizing resume and profile signals to deliver actionable career guidance.