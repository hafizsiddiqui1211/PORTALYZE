---
id: 2
title: Create resume analyzer core spec
stage: spec
date: 2025-12-28
surface: agent
model: Claude Sonnet 4.5
feature: 001-resume-analyzer-core
branch: 001-resume-analyzer-core
user: User
command: /sp.specify
labels:
  - specification
  - resume-analyzer
  - mvp
links:
  spec: specs/001-resume-analyzer-core/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-resume-analyzer-core/spec.md
  - specs/001-resume-analyzer-core/checklists/requirements.md
tests: []
---

# Prompt

```
/sp.specify

## Spec-1: Phase 1 – MVP (Resume Analyzer Core)

### Target Audience
- Individual job seekers and early-career to mid-level professionals
- Freelancers and AI/tech professionals showcasing portfolios
- Recruiter-facing demo users (portfolio credibility)

### Focus
- Resume file ingestion and parsing (PDF/DOCX)
- ATS-oriented resume evaluation
- Actionable, structured AI feedback
- Clean visualization of results via Streamlit dashboard
- Exportable analysis report (PDF)

### Functional Scope
1. **Resume Upload**
   - Accept PDF and DOCX formats
   - Validate file type and size
   - Secure, session-based handling of uploaded files

2. **AI Analyzer Pipeline**
   - Text extraction from resume
   - ATS match percentage calculation based on keyword relevance and role-agnostic standards
   - Keyword gap analysis with suggested improvements (e.g., Python, Streamlit, FastAPI)
   - Structured feedback generation, including:
     - Strengths
     - Weaknesses
     - Section-level critiques (e.g., projects, experience, skills)

3. **Results Presentation**
   - Streamlit dashboard with:
     - Color-coded sections (strengths, risks, suggestions)
     - Clear headings and readable summaries
     - ATS score visualization (percentage or gauge-style)

4. **Report Export**
   - Generate a downloadable PDF report
   - Include ATS score, feedback, and keyword suggestions
   - Maintain professional formatting suitable for sharing

### Success Criteria
- Resume text is accurately extracted from both PDF and DOCX formats
- ATS score is computed and clearly explained to the user
- Keyword suggestions are relevant to modern AI/tech roles
- Feedback is structured, specific, and actionable
- Dashboard is intuitive, visually clean, and responsive
- PDF export faithfully reflects on-screen analysis

### Constraints
- Tech stack:
  - Frontend: Streamlit
  - Backend logic: Python
  - AI analysis: Claude CLI via SpeckitPlus (aligned with project constitution)
```

# Response

Successfully created the feature specification for Resume Analyzer Core at specs/001-resume-analyzer-core/spec.md.

The specification includes:
- Three user stories prioritized as P1 (Resume Upload and Analysis), P2 (Dashboard Visualization), and P3 (Keyword Gap Analysis)
- Functional requirements covering file upload, text extraction, ATS scoring, feedback generation, dashboard display, and PDF export
- Success criteria with measurable outcomes for accuracy, performance, relevance, and usability
- Edge cases for file format validation, large files, and service availability
- Key entities: Resume, AnalysisResult, and KeywordSuggestion

The specification follows the template structure and maintains focus on user value without implementation details. A quality checklist was also created to validate the specification completeness.