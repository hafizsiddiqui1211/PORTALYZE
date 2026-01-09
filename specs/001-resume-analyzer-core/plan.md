# Implementation Plan: Resume Analyzer Core

**Branch**: `001-resume-analyzer-core` | **Date**: 2025-12-28 | **Spec**: [link]
**Input**: Feature specification from `/specs/001-resume-analyzer-core/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Resume Analyzer Core is the Phase 1 MVP of the Smart Resume & Portfolio Analyzer. The feature enables users to upload resumes (PDF/DOCX), receive ATS scoring, structured AI feedback, keyword gap analysis, and export results as a professional PDF via a Streamlit dashboard. The implementation follows the core principles of accuracy, actionable feedback, user-centric clarity, AI-assisted intelligence, data privacy, and performance.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: Streamlit, PyPDF2/fitz (for PDF processing), python-docx (for DOCX processing), google-generativeai (for AI analysis), reportlab (for PDF generation)
**Storage**: In-memory processing with temporary encrypted file storage (24-hour auto-delete)
**Testing**: pytest for unit tests, Streamlit's testing utilities
**Target Platform**: Web application (multi-platform via browser)
**Project Type**: Single web application
**Performance Goals**: Analysis completes within 15 seconds, text extraction within 10 seconds, PDF generation within 5 seconds
**Constraints**: Files up to 10MB, 95% text extraction accuracy, 90% relevant keyword suggestions
**Scale/Scope**: Single-user session-based processing

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Accuracy**: ATS score computation follows industry-standard keyword matching and role-specific evaluation (SC-010)
- **Actionable Feedback**: Feedback is structured, specific, and actionable with at least 3 distinct improvement suggestions per analysis (SC-004)
- **User-Centric Clarity**: Dashboard is clean, intuitive, and color-coded by sections (SC-005)
- **AI-Assisted Intelligence**: Recommendations leverage AI reasoning, keyword extraction, and pattern analysis
- **Data Privacy**: Files handled in encrypted temporary storage with 24-hour auto-delete (SC-008)
- **Performance**: Analysis completes within 15 seconds (SC-002)

## Project Structure

### Documentation (this feature)

```text
specs/001-resume-analyzer/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── main.py              # Streamlit app entry point
├── models/
│   ├── resume.py        # Resume entity and processing
│   ├── analysis.py      # AnalysisResult entity
│   └── suggestions.py   # KeywordSuggestion entity
├── services/
│   ├── file_processor.py # PDF/DOCX processing service
│   ├── text_extractor.py # Text extraction service
│   ├── ats_analyzer.py  # ATS scoring service
│   ├── ai_service.py    # AI analysis integration
│   └── pdf_generator.py # PDF report generation
├── ui/
│   ├── components/      # Streamlit UI components
│   └── dashboard.py     # Dashboard UI logic
└── utils/
    ├── security.py      # Security and encryption utilities
    ├── validators.py    # Input validation utilities
    └── constants.py     # Application constants

tests/
├── unit/
│   ├── test_models/     # Model unit tests
│   ├── test_services/   # Service unit tests
│   └── test_ui/         # UI component tests
├── integration/
│   └── test_end_to_end.py # End-to-end tests
└── conftest.py          # Test configuration

data/
├── temp/                # Temporary file storage (encrypted)
└── templates/           # PDF report templates

requirements.txt          # Python dependencies
.streamlit/
└── config.toml          # Streamlit configuration
```

**Structure Decision**: Single project structure with clear separation of concerns following MVC-like pattern with models, services, and UI components.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |