---
id: 1
title: Update project constitution for Smart Resume Analyzer
stage: constitution
date: 2025-12-28
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: User
command: /sp.constitution
labels:
  - constitution
  - project-setup
  - smart-resume-analyzer
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests: []
---

# Prompt

```
/sp.constitution

## Project
**Smart Resume & Portfolio Analyzer (AI-powered)**

## Core Principles
- **Accuracy:** All resume/portfolio insights must reflect the actual content and ATS standards.
- **Actionable feedback:** Suggestions must be practical, specific, and measurable (e.g., "Add quantifiable metrics to your projects").
- **User-centric clarity:** Feedback must be presented in a concise, visually structured manner suitable for non-technical users.
- **AI-assisted intelligence:** Recommendations must leverage AI reasoning, keyword extraction, and pattern analysis.
- **Tech stack compliance:** Streamlit frontend, Python backend, OpenAI Agents SDK/GPT for AI analysis, SQL for data storage.
- **Report export:** Must support PDF generation of analysis.
- **Performance:** Analysis for a single resume must complete within 10–15 seconds.

## Success Criteria
- ATS score correctly calculated and justified.
- Feedback actionable and clearly categorized (strengths, weaknesses, suggested improvements).
- Job role recommendations are relevant and aligned with skills/experience.
- Dashboard is clean, intuitive, and color-coded by sections.
- Optional AI bio is coherent, professional, and enhances candidate profile.
- Data privacy ensured with optional user history storage.

## Key Standards
- Resume/portfolio parsing must extract text reliably from PDF/DOCX/LinkedIn/GitHub.
- ATS score computation must follow industry-standard keyword matching and role-specific evaluation.
- Job role suggestions must align with the candidate's experience, skills, and industry selection.
- Recommendations for content, formatting, and portfolio improvements must be context-aware.
- Optional AI-generated bio must be personalized, concise, and relevant to the candidate's profile.

## Constraints
- **Phase-wise delivery:** MVP ( score correctly calculated and justified.
- Feedback actionable and clearly categorized (strengths, weaknesses, suggested improvements).
- Job role recommendations are relevant and aligned with skills/experience.
- Dashboard is clean, intuitive, and color-coded by sections.
- Optional AI bio is coherent, professional, and enhances candidate profile.
- Data privacy ensured with optional user history storage.
```

# Response

The project constitution for the Smart Resume & Portfolio Analyzer has been successfully created/updated at `.specify/memory/constitution.md`.

## New Constitution Content

# Smart Resume & Portfolio Analyzer Constitution

## Core Principles

### Accuracy
All resume/portfolio insights must reflect the actual content and ATS standards. ATS score computation must follow industry-standard keyword matching and role-specific evaluation.

### Actionable Feedback
Suggestions must be practical, specific, and measurable (e.g., 'Add quantifiable metrics to your projects'). Feedback must be actionable and clearly categorized (strengths, weaknesses, suggested improvements).

### User-Centric Clarity
Feedback must be presented in a concise, visually structured manner suitable for non-technical users. Dashboard is clean, intuitive, and color-coded by sections.

### AI-Assisted Intelligence
Recommendations must leverage AI reasoning, keyword extraction, and pattern analysis. Job role suggestions must align with the candidate's experience, skills, and industry selection.

### Data Privacy
All uploaded files and profile data must be securely handled; no permanent storage without user consent. Data privacy ensured with optional user history storage.

### Performance
Analysis for a single resume must complete within 10–15 seconds. Tech stack compliance: Streamlit frontend, Python backend, OpenAI Agents SDK/GPT for AI analysis, SQL for data storage.

## Key Standards
Resume/portfolio parsing must extract text reliably from PDF/DOCX/LinkedIn/GitHub. Report export must support PDF generation of analysis. Recommendations for content, formatting, and portfolio improvements must be context-aware. Optional AI-generated bio must be personalized, concise, and relevant to the candidate's profile.

## Development Workflow
Phase-wise delivery: MVP must have ATS score correctly calculated and justified. Optional AI bio must be coherent, professional, and enhance candidate profile.

## Governance
All implementations must comply with these principles. Success criteria include: job role recommendations are relevant and aligned with skills/experience, and optional AI bio is coherent, professional, and enhances candidate profile.

**Version**: 1.0.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-28

## Summary
- New constitution version: 1.0.0 (initial version)
- File updated: `.specify/memory/constitution.md`
- No files flagged for manual follow-up
- Commit message: `docs: create constitution for Smart Resume & Portfolio Analyzer v1.0.0`