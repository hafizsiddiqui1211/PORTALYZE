---
id: 5
title: Create implementation plan
stage: plan
date: 2025-12-28
surface: agent
model: Claude Sonnet 4.5
feature: 001-resume-analyzer-core
branch: 001-resume-analyzer-core
user: User
command: /sp.plan
labels:
  - planning
  - architecture
  - resume-analyzer
links:
  spec: specs/001-resume-analyzer-core/spec.md
  plan: specs/001-resume-analyzer-core/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-resume-analyzer-core/plan.md
  - specs/001-resume-analyzer-core/research.md
  - specs/001-resume-analyzer-core/data-model.md
  - specs/001-resume-analyzer-core/quickstart.md
  - specs/001-resume-analyzer-core/contracts/api-contract.md
tests: []
---

# Prompt

```
/sp.plan

## Feature
**Resume Analyzer Core (Spec-1 – Phase 1 MVP)**
Feature Branch: `001-resume-analyzer-core`

---

## Objective
Plan and execute the Phase 1 MVP of the Smart Resume & Portfolio Analyzer, enabling users to upload resumes (PDF/DOCX), receive ATS scoring, structured AI feedback, keyword gap analysis, and export results as a professional PDF via a Streamlit dashboard.

---

## Plan Structure

### 1. Architecture Sketch
- **UI Layer**
  - Streamlit app
  - File upload component (PDF/DOCX, max 10MB)
  - Dashboard components (score display, color-coded sections)
  - Download button for PDF export

- **Processing Layer**
  ## Phase B: Foundation
- Streamlit UI scaffolding
- File upload validation and error handling
- Secure session-based file handling
- Text extraction pipeline implementation

#### Phase C: Analysis
- Integrate Claude CLI via SpeckitPlus
- Implement ATS scoring logic
- Generate structured feedback and keyword suggestions
- Handle AI unavailability gracefully

#### Phase D: Synthesis
- Assemble dashboard views
- Implement color-coded visualization
- Generate downloadable PDF reports
- Finalize performance optimizations

---

## Decisions Needing Documentation

### Decision 1: ATS Scoring Method
- **Option A**: Pure keyword frequency matching
  - Pros: Simple, fast
  - Cons: Less realistic ATS simulation
- **Option B**: Weighted scoring (keywords + formatting + sections)
  - Pros: More realistic, better user trust
  - Cons: Slightly higher complexity
**Chosen**: Option B

### Decision 2: File Storage Strategy
- **Option A**: In-memory only
  - Pros: Maximum privacy
  - Cons: Harder debugging
- **Option B**: Encrypted temporary storage (24h)
  - Pros: Debugging support, controlled risk
  - Cons: Requires cleanup mechanism
**Chosen**: Option B

### Decision 3: PDF Generation
- **Option A**: HTML-to-PDF rendering
  - Pros: Visual parity with dashboard
  - Cons: Styling inconsistencies
- **Option B**: Dedicated PDF layout engine
  - Pros: Professional, predictable formatting
  - Cons: Extra implementation effort
**Chosen**: Option B

---

## Testing Strategy

### Validation Checks (Based on Acceptance Criteria)

- Upload valid PDF/DOCX → analysis completes within 15 seconds
- Upload unsupported format → clear error message
- Upload file >10MB → rejection with explanation
- Extracted text accuracy ≥ 95%
- ATS score returned as percentage (0–100%) with explanation
- At least 3 actionable suggestions per resume
- Keyword suggestions relevant to AI/tech roles
- Dashboard renders:
  - ATS score prominently
  - Color-coded strengths and weaknesses
- PDF export:
  - Matches on-screen analysis
  - Generated within 5 seconds
- AI service unavailable → graceful error + retry option

---

## Quality Validation
- Cross-check extracted text vs original resume samples
- Manual review of ATS scoring logic against known resumes
- User scenario walkthroughs for P1, P2, P3 stories
- Performance testing for extraction and PDF generation
- Privacy validation: auto-delete encrypted files after 24h
```

# Response

Successfully created the implementation plan for Resume Analyzer Core. The following artifacts were generated:

1. **plan.md** - Complete implementation plan with technical context, constitution check, and project structure
2. **research.md** - Research findings with technology decisions and rationale
3. **data-model.md** - Detailed data model with entities, validation rules, and relationships
4. **quickstart.md** - Setup and usage instructions for developers
5. **contracts/api-contract.md** - API contracts defining endpoints and data flows

The plan addresses all specified requirements including:
- Streamlit-based UI with file upload and dashboard
- PDF/DOCX processing with 10MB size limit
- ATS scoring with weighted algorithm (keyword matching, formatting, sections)
- Claude CLI integration via SpeckitPlus for AI analysis
- Encrypted temporary file storage with 24-hour auto-delete
- PDF report generation with professional formatting
- Performance targets (15s analysis, 10s text extraction, 5s PDF generation)
- Error handling for various failure scenarios

The architecture follows the specified phases and incorporates all constitution principles: accuracy, actionable feedback, user-centric clarity, AI-assisted intelligence, data privacy, and performance.