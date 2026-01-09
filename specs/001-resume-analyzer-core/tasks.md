# Tasks: Resume Analyzer Core

**Input**: Design documents from `/specs/001-resume-analyzer-core/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/api-contract.md, quickstart.md

**Tests**: Tests are included as this is a production-grade feature requiring reliability validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project directory structure per plan.md (src/models/, src/services/, src/ui/, src/utils/, tests/, data/)
- [ ] T002 Initialize Python 3.11 project with requirements.txt (streamlit, PyMuPDF, python-docx, reportlab, pytest)
- [ ] T003 [P] Create .streamlit/config.toml with Streamlit configuration
- [ ] T004 [P] Create .env.example with environment variables template (GEMINI_API_KEY, TEMP_DIR, MAX_FILE_SIZE, SESSION_TIMEOUT)
- [ ] T005 [P] Create src/utils/constants.py with application constants (file size limits, supported formats, timeout values)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 Create src/models/resume.py with Resume entity (resume_id, original_filename, file_type, file_path, text_content, metadata, upload_timestamp, session_id)
- [ ] T007 [P] Create src/models/analysis.py with AnalysisResult entity (analysis_id, resume_id, ats_score, strengths, weaknesses, section_feedback, overall_feedback, confidence_level)
- [ ] T008 [P] Create src/models/suggestions.py with KeywordSuggestion entity (suggestion_id, analysis_id, keyword, relevance_score, category, justification, role_alignment)
- [ ] T009 Create src/utils/security.py with encryption utilities for temporary file storage
- [ ] T010 [P] Create src/utils/validators.py with file type and size validation functions
- [ ] T011 Create src/services/file_processor.py with file handling base class and validation logic
- [ ] T012 Create data/temp/.gitkeep and data/templates/.gitkeep directories for temporary storage
- [ ] T013 Create tests/conftest.py with pytest fixtures for testing

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Resume Upload and Analysis (Priority: P1) MVP

**Goal**: Enable users to upload PDF/DOCX resumes and receive ATS compatibility analysis with actionable feedback

**Independent Test**: Upload a resume file and verify the system processes it, extracts text, calculates ATS score, and provides structured feedback with strengths, weaknesses, and keyword suggestions

### Tests for User Story 1

- [ ] T014 [P] [US1] Create tests/unit/test_services/test_text_extractor.py with PDF and DOCX extraction tests
- [ ] T015 [P] [US1] Create tests/unit/test_services/test_ats_analyzer.py with ATS scoring algorithm tests
- [ ] T016 [P] [US1] Create tests/unit/test_models/test_resume.py with Resume entity validation tests

### Implementation for User Story 1

- [ ] T017 [US1] Implement src/services/text_extractor.py with PyMuPDF (PDF) and python-docx (DOCX) extraction
- [ ] T018 [US1] Implement src/services/ats_analyzer.py with weighted scoring (keyword 40%, formatting 30%, section completeness 30%)
- [ ] T019 [US1] Implement src/services/ai_service.py with Claude CLI integration for AI-powered analysis
- [ ] T020 [US1] Create src/ui/components/file_uploader.py with Streamlit file upload widget (PDF/DOCX, 10MB limit)
- [ ] T021 [US1] Create src/ui/components/analysis_display.py with basic analysis results display
- [ ] T022 [US1] Create src/main.py with Streamlit app entry point integrating upload and analysis flow
- [ ] T023 [US1] Add error handling for unsupported file types and file size violations in src/services/file_processor.py
- [ ] T024 [US1] Add error handling for AI service unavailability with retry logic in src/services/ai_service.py

**Checkpoint**: User Story 1 complete - users can upload resumes and receive ATS analysis

---

## Phase 4: User Story 2 - Dashboard Visualization (Priority: P2)

**Goal**: Display analysis results in a clean, intuitive dashboard with color-coded feedback sections

**Independent Test**: Load an existing analysis and verify the dashboard displays ATS score prominently with color-coded strengths (green), weaknesses (red), and organized section feedback

### Tests for User Story 2

- [ ] T025 [P] [US2] Create tests/unit/test_ui/test_dashboard.py with dashboard component rendering tests
- [ ] T026 [P] [US2] Create tests/unit/test_ui/test_components.py with individual UI component tests

### Implementation for User Story 2

- [ ] T027 [US2] Create src/ui/components/score_display.py with prominent ATS score visualization (0-100 scale, color gradient)
- [ ] T028 [US2] Create src/ui/components/strengths_panel.py with green-themed strengths section
- [ ] T029 [US2] Create src/ui/components/weaknesses_panel.py with red-themed weaknesses section
- [ ] T030 [US2] Create src/ui/components/section_feedback.py with expandable section-by-section feedback (experience, skills, education, projects)
- [ ] T031 [US2] Create src/ui/dashboard.py integrating all dashboard components with layout
- [ ] T032 [US2] Update src/main.py to use dashboard.py for results display
- [ ] T033 [US2] Add CSS styling via .streamlit/config.toml for consistent visual design

**Checkpoint**: User Story 2 complete - results displayed in intuitive color-coded dashboard

---

## Phase 5: User Story 3 - Keyword Gap Analysis (Priority: P3)

**Goal**: Provide specific keyword suggestions relevant to AI/tech roles with explanations

**Independent Test**: Analyze a resume and verify keyword suggestions include relevant AI/tech terms (Python, Streamlit, FastAPI, etc.) with category, relevance score, and justification

### Tests for User Story 3

- [ ] T034 [P] [US3] Create tests/unit/test_services/test_keyword_analyzer.py with keyword suggestion tests
- [ ] T035 [P] [US3] Create tests/unit/test_models/test_suggestions.py with KeywordSuggestion entity tests

### Implementation for User Story 3

- [ ] T036 [US3] Create src/services/keyword_analyzer.py with AI/tech role keyword database and gap analysis logic
- [ ] T037 [US3] Create src/ui/components/keyword_suggestions.py with keyword display cards (keyword, relevance, category, justification)
- [ ] T038 [US3] Update src/services/ai_service.py to include keyword suggestions in analysis prompt
- [ ] T039 [US3] Update src/ui/dashboard.py to include keyword suggestions section
- [ ] T040 [US3] Create data/templates/keywords.json with curated AI/tech role keyword database

**Checkpoint**: User Story 3 complete - keyword gap analysis with actionable suggestions

---

## Phase 6: PDF Export (Cross-Story Feature)

**Goal**: Generate downloadable PDF reports with all analysis results

**Independent Test**: Complete an analysis and verify PDF download contains ATS score, strengths, weaknesses, section feedback, and keyword suggestions with professional formatting

### Tests for PDF Export

- [ ] T041 [P] Create tests/unit/test_services/test_pdf_generator.py with PDF generation and content tests

### Implementation for PDF Export

- [ ] T042 Implement src/services/pdf_generator.py with ReportLab for professional PDF generation
- [ ] T043 Create data/templates/report_template.py with PDF report layout and styling
- [ ] T044 Create src/ui/components/download_button.py with Streamlit download button for PDF export
- [ ] T045 Update src/ui/dashboard.py to include PDF download functionality
- [ ] T046 Add PDF generation performance optimization (target: 5 seconds)

**Checkpoint**: PDF export complete - users can download professional analysis reports

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T047 [P] Create tests/integration/test_end_to_end.py with full workflow integration tests
- [ ] T048 [P] Add session cleanup logic in src/utils/security.py for 24-hour auto-delete
- [ ] T049 Add comprehensive logging in src/utils/logger.py for all services
- [ ] T050 Performance optimization for text extraction (target: 10 seconds)
- [ ] T051 Performance optimization for analysis (target: 15 seconds total)
- [ ] T052 [P] Update quickstart.md with final setup and usage instructions
- [ ] T053 Run quickstart.md validation to verify setup instructions work
- [ ] T054 Security hardening review for file handling and temporary storage

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - core upload/analysis flow
- **User Story 2 (Phase 4)**: Depends on Foundational - can parallel with US1 if separate developers
- **User Story 3 (Phase 5)**: Depends on Foundational - can parallel with US1/US2 if separate developers
- **PDF Export (Phase 6)**: Depends on US1 completion (needs analysis data to export)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1 for display but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Integrates with US1 analysis but independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before UI components
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- T003, T004, T005 can run in parallel (Setup phase)
- T007, T008 can run in parallel with T006 (Models)
- T009, T010 can run in parallel (Utilities)
- T014, T015, T016 can run in parallel (US1 tests)
- T025, T026 can run in parallel (US2 tests)
- T034, T035 can run in parallel (US3 tests)
- User stories can be developed in parallel by different team members after Foundational phase

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Create tests/unit/test_services/test_text_extractor.py" [T014]
Task: "Create tests/unit/test_services/test_ats_analyzer.py" [T015]
Task: "Create tests/unit/test_models/test_resume.py" [T016]

# After tests written, models are already done in Foundational, proceed to services:
Task: "Implement src/services/text_extractor.py" [T017]
# Then sequential: T018 → T019 → T020 → T021 → T022
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T013)
3. Complete Phase 3: User Story 1 (T014-T024)
4. **STOP and VALIDATE**: Test upload and analysis independently
5. Deploy/demo if ready - users can already get value!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo (better UX)
4. Add User Story 3 → Test independently → Deploy/Demo (keyword insights)
5. Add PDF Export → Test independently → Deploy/Demo (shareable reports)
6. Polish → Final validation → Production release

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (upload/analysis)
   - Developer B: User Story 2 (dashboard UI)
   - Developer C: User Story 3 (keyword analysis)
3. Stories complete and integrate independently
4. PDF Export after US1 complete
5. Polish phase together

---

## Summary

| Phase | Tasks | Parallel Opportunities |
|-------|-------|----------------------|
| Setup | 5 (T001-T005) | 3 tasks parallelizable |
| Foundational | 8 (T006-T013) | 4 tasks parallelizable |
| US1 (MVP) | 11 (T014-T024) | 3 test tasks parallelizable |
| US2 (Dashboard) | 9 (T025-T033) | 2 test tasks parallelizable |
| US3 (Keywords) | 7 (T034-T040) | 2 test tasks parallelizable |
| PDF Export | 6 (T041-T046) | 1 test task parallelizable |
| Polish | 8 (T047-T054) | 3 tasks parallelizable |

**Total Tasks**: 54
**MVP Scope**: Phases 1-3 (24 tasks)
**Full Feature**: All phases (54 tasks)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Performance targets: Text extraction 10s, Analysis 15s, PDF generation 5s
- File size limit: 10MB
- Temporary storage: Encrypted, 24-hour auto-delete
