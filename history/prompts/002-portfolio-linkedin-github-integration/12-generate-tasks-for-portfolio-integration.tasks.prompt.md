---
id: 12
title: Generate tasks for portfolio integration
stage: tasks
date: 2025-12-28
surface: agent
model: Claude Sonnet 4.5
feature: 002-portfolio-linkedin-github-integration
branch: 002-portfolio-linkedin-github-integration
user: User
command: /sp.tasks
labels:
  - tasks
  - implementation
  - portfolio-integration
  - linkedin
  - github
  - dependency-ordered
links:
  spec: specs/002-portfolio-linkedin-github-integration/spec.md
  plan: specs/002-portfolio-linkedin-github-integration/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-portfolio-linkedin-github-integration/tasks.md
tests: []
---

# Prompt

```
/sp.tasks Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts for 002-portfolio-linkedin-github-integration
```

# Response

Successfully generated dependency-ordered tasks.md for Portfolio + LinkedIn / GitHub Integration at `specs/002-portfolio-linkedin-github-integration/tasks.md`.

**Task Summary:**
- **Total Tasks**: 64 tasks across 7 phases
- **MVP Scope**: 22 tasks (Phases 1-3)
- **Full Feature**: 64 tasks (all phases)

**Phase Breakdown:**

| Phase | Description | Tasks | Parallel Opportunities |
|-------|-------------|-------|------------------------|
| Phase 1 | Setup | 4 (T001-T004) | 3 parallelizable |
| Phase 2 | Foundational | 8 (T005-T012) | 5 parallelizable |
| Phase 3 | US1 - URL Input/Validation (MVP) | 10 (T013-T022) | 2 parallelizable |
| Phase 4 | US2 - Profile Extraction | 13 (T023-T035) | 4 parallelizable |
| Phase 5 | US3 - AI Analysis | 14 (T036-T049) | 3 parallelizable |
| Phase 6 | Dashboard Integration | 7 (T050-T056) | 1 parallelizable |
| Phase 7 | Polish & Cross-Cutting | 8 (T057-T064) | 4 parallelizable |

**Key Features:**
- Tasks organized by user story for independent implementation
- Three platform extractors: LinkedIn (BeautifulSoup4), GitHub (PyGithub), Portfolio (BeautifulSoup4)
- Rate limiting with exponential backoff (tenacity library)
- Resume-profile alignment scoring and discrepancy detection
- Integration with Phase 1 resume analysis in unified dashboard

**User Story Independence:**
- US1 (P1): URL input and validation - delivers immediate value
- US2 (P2): Profile data extraction - depends on US1 for validated URLs
- US3 (P3): AI-driven analysis - depends on US2 for extracted data

**Technical Decisions Incorporated:**
- LinkedIn: Public profile scraping via BeautifulSoup4
- GitHub: PyGithub library with REST API
- Portfolio: BeautifulSoup4 with main page + linked pages only
- Rate limiting: 1s base delay, 32s max, 5 retries with jitter

# Outcome

- Impact: Implementation roadmap with 64 actionable tasks ready for execution
- Tests: Test tasks included for each user story (T013-T014, T023-T026, T036-T038, T050)
- Files: specs/002-portfolio-linkedin-github-integration/tasks.md created
- Next prompts: `/sp.implement` to begin task execution, or `/sp.taskstoissues` to create GitHub issues
- Reflection: Tasks properly handle Phase 1 dependency and three different extraction pipelines

# Evaluation notes (flywheel)

- Failure modes observed: None - all design documents loaded successfully
- Graders run and results: Format validation PASS (all tasks have checkbox, ID, labels, file paths)
- Prompt variant: Standard /sp.tasks with feature context
- Next experiment: Consider adding mock data fixtures for HTTP response testing
