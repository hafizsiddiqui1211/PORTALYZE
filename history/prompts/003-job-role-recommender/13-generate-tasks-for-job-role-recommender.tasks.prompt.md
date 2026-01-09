---
id: 13
title: Generate tasks for job role recommender
stage: tasks
date: 2025-12-28
surface: agent
model: Claude Sonnet 4.5
feature: 003-job-role-recommender
branch: 003-job-role-recommender
user: User
command: /sp.tasks
labels:
  - tasks
  - implementation
  - job-role-recommender
  - career-advice
  - dependency-ordered
links:
  spec: specs/003-job-role-recommender/spec.md
  plan: specs/003-job-role-recommender/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-job-role-recommender/tasks.md
tests: []
---

# Prompt

```
/sp.tasks Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts for 003-job-role-recommender
```

# Response

Successfully generated dependency-ordered tasks.md for Job Role Recommender at `specs/003-job-role-recommender/tasks.md`.

**Task Summary:**
- **Total Tasks**: 81 tasks across 8 phases
- **MVP Scope**: 33 tasks (Phases 1-3)
- **Full Feature**: 81 tasks (all phases)

**Phase Breakdown:**

| Phase | Description | Tasks | Parallel Opportunities |
|-------|-------------|-------|------------------------|
| Phase 1 | Setup | 4 (T001-T004) | 3 parallelizable |
| Phase 2 | Foundational | 14 (T005-T018) | 10 parallelizable |
| Phase 3 | US1 - Industry Selection/Role Inference (MVP) | 15 (T019-T033) | 3 parallelizable |
| Phase 4 | US2 - Role Mapping/Justification | 12 (T034-T045) | 2 parallelizable |
| Phase 5 | US3 - Gap Analysis | 10 (T046-T055) | 2 parallelizable |
| Phase 6 | Confidence/Consent Management | 11 (T056-T066) | 2 parallelizable |
| Phase 7 | Dashboard Integration | 7 (T067-T073) | 1 parallelizable |
| Phase 8 | Polish & Cross-Cutting | 8 (T074-T081) | 4 parallelizable |

**Key Features:**
- Tasks organized by user story for independent implementation
- YAML-based knowledge base with 5 industry files (AI/ML, Software Engineering, Data, FinTech, EdTech)
- Signal aggregation from Phases 1 & 2 (resume + profiles)
- Three-tier seniority detection (junior/mid/senior)
- Confidence indicators (High/Medium/Low) with explanations
- Consent-based anonymized storage with 24-hour auto-delete

**User Story Independence:**
- US1 (P1): Industry selection and role inference - delivers immediate value
- US2 (P2): Role justifications - depends on US1 for recommendations
- US3 (P3): Gap analysis - depends on US2 for roles with seniority

**Technical Decisions Incorporated:**
- Claude CLI with structured prompting for role inference
- YAML knowledge base for quarterly updates
- Weighted signal aggregation (resume primary, profiles validation)
- Conflicting signal handling with multiple role paths

# Outcome

- Impact: Implementation roadmap with 81 actionable tasks ready for execution
- Tests: Test tasks included for each user story and cross-cutting features
- Files: specs/003-job-role-recommender/tasks.md created
- Next prompts: `/sp.implement` to begin task execution, or `/sp.taskstoissues` to create GitHub issues
- Reflection: Tasks properly handle Phases 1 & 2 dependency and complex knowledge base setup

# Evaluation notes (flywheel)

- Failure modes observed: None - all design documents loaded successfully
- Graders run and results: Format validation PASS (all tasks have checkbox, ID, labels, file paths)
- Prompt variant: Standard /sp.tasks with feature context
- Next experiment: Consider adding knowledge base content validation tasks
