# Tasks: Portfolio + LinkedIn / GitHub Integration

**Input**: Design documents from `/specs/002-portfolio-linkedin-github-integration/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/api-contract.md, quickstart.md
**Phase 1 Dependency**: Extends Phase 1 (001-resume-analyzer-core) - assumes Phase 1 foundation is complete

**Tests**: Tests are included as this is a production-grade feature requiring reliability validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and Phase 2 dependencies setup

- [ ] T001 Update requirements.txt with Phase 2 dependencies (beautifulsoup4, httpx, lxml, PyGithub, tenacity, validators)
- [ ] T002 [P] Update .env.example with Phase 2 environment variables (GITHUB_TOKEN, HTTP_TIMEOUT, MAX_RETRIES, RETRY_BASE_DELAY, MAX_PORTFOLIO_PAGES)
- [ ] T003 [P] Extend src/utils/constants.py with Phase 2 constants (URL patterns, rate limit configs, timeout values)
- [ ] T004 [P] Create src/utils/http_client.py with async HTTP client, retry logic, and timeout handling

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Create src/models/profile_url.py with ProfileURL entity (url_id, url, profile_type, is_valid, is_accessible, validation_timestamp, session_id, error_message)
- [ ] T006 [P] Create src/models/profile_data.py with ProfileData entity (profile_id, url_id, profile_type, raw_content, normalized_content, extraction_timestamp, extraction_status, limitations)
- [ ] T007 [P] Create src/models/improvement.py with ImprovementSuggestion entity (suggestion_id, category, priority, suggestion_text, rationale, example, affected_section)
- [ ] T008 [P] Create src/models/profile_analysis.py with ProfileAnalysis entity (profile_analysis_id, profile_id, profile_type, strengths, weaknesses, suggestions, clarity_score, impact_score)
- [ ] T009 [P] Create src/models/alignment.py with AlignmentResult entity (alignment_id, overall_score, skill_alignment, experience_alignment, project_alignment, discrepancies, recommendations)
- [ ] T010 Create src/services/rate_limiter.py with exponential backoff using tenacity (1s base, 32s max, 5 retries, jitter)
- [ ] T011 Create src/services/profile_extractor.py with base ProfileExtractor class defining extraction interface
- [ ] T012 Update tests/conftest.py with Phase 2 fixtures (mock URLs, mock HTTP responses, mock profile data)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Profile URL Input and Validation (Priority: P1) MVP

**Goal**: Enable users to input and validate Portfolio, LinkedIn, and GitHub URLs with clear feedback on format and accessibility

**Independent Test**: Enter valid/invalid URLs and verify the system correctly validates format, detects profile type (LinkedIn/GitHub/Portfolio), and checks accessibility with clear error messages for failures

### Tests for User Story 1

- [ ] T013 [P] [US1] Create tests/unit/test_services/test_url_validator.py with URL format validation tests (valid LinkedIn, GitHub, Portfolio patterns)
- [ ] T014 [P] [US1] Create tests/unit/test_models/test_profile_url.py with ProfileURL entity validation tests

### Implementation for User Story 1

- [ ] T015 [US1] Implement src/services/url_validator.py with URL format validation (LinkedIn pattern, GitHub pattern, generic HTTP/HTTPS)
- [ ] T016 [US1] Add accessibility checking in src/services/url_validator.py using httpx with timeout handling
- [ ] T017 [US1] Add profile type auto-detection in src/services/url_validator.py based on URL patterns
- [ ] T018 [US1] Create src/ui/components/url_input.py with Streamlit multi-URL input fields (LinkedIn, GitHub, Portfolio)
- [ ] T019 [US1] Add URL validation UI feedback in src/ui/components/url_input.py (valid/invalid/checking states)
- [ ] T020 [US1] Create src/ui/components/validation_status.py with validation result display (checkmarks, errors, accessibility status)
- [ ] T021 [US1] Update src/main.py to add "Profile Analysis" tab with URL input flow
- [ ] T022 [US1] Add error handling for invalid URL formats with clear user messaging

**Checkpoint**: User Story 1 complete - users can input and validate profile URLs

---

## Phase 4: User Story 2 - Profile Data Extraction and Normalization (Priority: P2)

**Goal**: Extract public profile data from validated URLs and normalize into structured format for AI analysis

**Independent Test**: Provide valid profile URLs and verify system extracts relevant data elements (LinkedIn headline/summary/experience, GitHub repos/README/stars, Portfolio bio/projects/skills) and normalizes into structured ProfileData objects

### Tests for User Story 2

- [ ] T023 [P] [US2] Create tests/unit/test_services/test_linkedin_extractor.py with LinkedIn extraction tests (mock HTML responses)
- [ ] T024 [P] [US2] Create tests/unit/test_services/test_github_extractor.py with GitHub extraction tests (mock API responses)
- [ ] T025 [P] [US2] Create tests/unit/test_services/test_portfolio_extractor.py with Portfolio extraction tests (mock HTML responses)
- [ ] T026 [P] [US2] Create tests/unit/test_models/test_profile_data.py with ProfileData entity validation tests

### Implementation for User Story 2

- [ ] T027 [US2] Implement src/services/linkedin_extractor.py with BeautifulSoup4 extraction (headline, summary, experience highlights, skills)
- [ ] T028 [US2] Implement src/services/github_extractor.py with PyGithub extraction (repos, README, stars, forks, languages, activity)
- [ ] T029 [US2] Implement src/services/portfolio_extractor.py with BeautifulSoup4 extraction (bio/about, projects, skills, contact visibility)
- [ ] T030 [US2] Add graceful degradation in all extractors for partial extraction scenarios
- [ ] T031 [US2] Add page limit handling in src/services/portfolio_extractor.py (main page + MAX_PORTFOLIO_PAGES linked pages)
- [ ] T032 [US2] Create src/ui/components/extraction_progress.py with Streamlit progress indicator during extraction
- [ ] T033 [US2] Create src/ui/components/profile_display.py with extracted data preview for each profile type
- [ ] T034 [US2] Integrate extractors with rate limiter in src/services/profile_extractor.py
- [ ] T035 [US2] Add extraction status reporting (SUCCESS/PARTIAL/FAILED) with limitations display

**Checkpoint**: User Story 2 complete - profile data extracted and normalized for all three profile types

---

## Phase 5: User Story 3 - AI-Driven Profile Analysis and Suggestions (Priority: P3)

**Goal**: Generate AI-powered analysis with specific, actionable improvement suggestions for each profile

**Independent Test**: Analyze extracted profile data and verify AI generates strengths, weaknesses, clarity/impact scores, and actionable suggestions with categories (CONTENT, FORMATTING, VISIBILITY, ALIGNMENT, TECHNICAL) and priorities

### Tests for User Story 3

- [ ] T036 [P] [US3] Create tests/unit/test_services/test_profile_analyzer.py with AI analysis tests (mock Gemini API responses)
- [ ] T037 [P] [US3] Create tests/unit/test_services/test_alignment_analyzer.py with resume-profile alignment tests
- [ ] T038 [P] [US3] Create tests/unit/test_models/test_improvement.py with ImprovementSuggestion entity validation tests

### Implementation for User Story 3

- [ ] T039 [US3] Create src/services/profile_analyzer.py with Gemini API integration for profile analysis
- [ ] T040 [US3] Implement LinkedIn-specific analysis prompts in src/services/profile_analyzer.py (headline clarity, summary impact, experience highlights)
- [ ] T041 [US3] Implement GitHub-specific analysis prompts in src/services/profile_analyzer.py (repo quality, README evaluation, project signaling)
- [ ] T042 [US3] Implement Portfolio-specific analysis prompts in src/services/profile_analyzer.py (bio clarity, project presentation, skills visibility)
- [ ] T043 [US3] Implement src/services/alignment_analyzer.py with resume-profile comparison (skills, experience, projects alignment scoring)
- [ ] T044 [US3] Add discrepancy detection in src/services/alignment_analyzer.py for resume-profile mismatches
- [ ] T045 [US3] Create src/ui/components/analysis_results.py with strengths/weaknesses display (color-coded panels)
- [ ] T046 [US3] Create src/ui/components/suggestions_panel.py with prioritized improvement suggestions display
- [ ] T047 [US3] Create src/ui/components/alignment_view.py with alignment score visualization and discrepancy highlights
- [ ] T048 [US3] Add AI service unavailability handling with graceful error messaging
- [ ] T049 [US3] Add analysis timeout handling (20 seconds max per profile)

**Checkpoint**: User Story 3 complete - AI analysis with actionable suggestions for all profile types

---

## Phase 6: Dashboard Integration (Cross-Story Feature)

**Goal**: Integrate Phase 2 profile analysis with Phase 1 resume analysis in unified dashboard

**Independent Test**: Complete resume + profile analysis and verify unified dashboard shows resume insights, profile insights per platform, alignment scores, and combined recommendations

### Tests for Dashboard Integration

- [ ] T050 [P] Create tests/integration/test_profile_flow.py with end-to-end profile analysis workflow tests

### Implementation for Dashboard Integration

- [ ] T051 Update src/ui/dashboard.py to add Profile Analysis section alongside Resume Analysis
- [ ] T052 Create src/ui/components/combined_insights.py with cross-platform insights summary
- [ ] T053 Update src/main.py to integrate Phase 2 flows with Phase 1 dashboard
- [ ] T054 Add tab navigation in src/ui/dashboard.py for Resume Analysis / Profile Analysis / Combined View
- [ ] T055 Update PDF report generation in src/services/pdf_generator.py to include profile analysis results
- [ ] T056 Add combined recommendations section in src/ui/components/combined_insights.py

**Checkpoint**: Dashboard integration complete - unified view of resume and profile analysis

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T057 [P] Add comprehensive logging in all extractors for debugging (extraction attempts, failures, rate limits)
- [ ] T058 [P] Add encrypted temporary storage for profile data with 24-hour auto-delete in src/utils/security.py
- [ ] T059 Performance optimization for 20-second analysis target (parallel extraction, caching)
- [ ] T060 [P] Update quickstart.md with final Phase 2 setup and usage instructions
- [ ] T061 Run quickstart.md validation to verify setup instructions work
- [ ] T062 Security review for profile data handling and temporary storage
- [ ] T063 [P] Add user notification system for rate limiting delays in src/ui/components/extraction_progress.py
- [ ] T064 Edge case handling for profiles with privacy restrictions or minimal content

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Depends on Phase 1 (001-resume-analyzer-core) being complete
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - URL validation flow
- **User Story 2 (Phase 4)**: Depends on Foundational + US1 (needs validated URLs)
- **User Story 3 (Phase 5)**: Depends on Foundational + US2 (needs extracted data)
- **Dashboard Integration (Phase 6)**: Depends on US3 completion + Phase 1 resume analysis
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other Phase 2 stories
- **User Story 2 (P2)**: Depends on US1 (needs validated URLs) - Can parallel models/tests early
- **User Story 3 (P3)**: Depends on US2 (needs extracted data) - Can parallel tests early

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before UI components
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- T002, T003, T004 can run in parallel (Setup phase)
- T006, T007, T008, T009 can run in parallel (Models in Foundational)
- T013, T014 can run in parallel (US1 tests)
- T023, T024, T025, T026 can run in parallel (US2 tests)
- T036, T037, T038 can run in parallel (US3 tests)
- T057, T058, T060, T063 can run in parallel (Polish phase)

---

## Parallel Example: User Story 2

```bash
# Launch all tests for User Story 2 together:
Task: "Create tests/unit/test_services/test_linkedin_extractor.py" [T023]
Task: "Create tests/unit/test_services/test_github_extractor.py" [T024]
Task: "Create tests/unit/test_services/test_portfolio_extractor.py" [T025]
Task: "Create tests/unit/test_models/test_profile_data.py" [T026]

# After tests written, implement extractors (can be parallelized by different developers):
Task: "Implement src/services/linkedin_extractor.py" [T027]
Task: "Implement src/services/github_extractor.py" [T028]
Task: "Implement src/services/portfolio_extractor.py" [T029]
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T012)
3. Complete Phase 3: User Story 1 (T013-T022)
4. **STOP and VALIDATE**: Test URL input and validation independently
5. Deploy/demo if ready - users can validate their profile URLs!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (URL validation MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo (profile extraction)
4. Add User Story 3 → Test independently → Deploy/Demo (AI analysis)
5. Add Dashboard Integration → Test independently → Deploy/Demo (unified view)
6. Polish → Final validation → Production release

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (URL validation)
   - Developer B: User Story 2 models + tests (preparation)
3. After US1 complete:
   - Developer A: User Story 2 implementation
   - Developer B: User Story 3 models + tests (preparation)
4. After US2 complete:
   - Developer A: User Story 3 implementation
   - Developer B: Dashboard Integration preparation
5. Stories complete and integrate into unified dashboard

---

## Summary

| Phase | Tasks | Parallel Opportunities |
|-------|-------|----------------------|
| Setup | 4 (T001-T004) | 3 tasks parallelizable |
| Foundational | 8 (T005-T012) | 5 tasks parallelizable |
| US1 (MVP) | 10 (T013-T022) | 2 test tasks parallelizable |
| US2 (Extraction) | 13 (T023-T035) | 4 test tasks parallelizable |
| US3 (Analysis) | 14 (T036-T049) | 3 test tasks parallelizable |
| Dashboard Integration | 7 (T050-T056) | 1 test task parallelizable |
| Polish | 8 (T057-T064) | 4 tasks parallelizable |

**Total Tasks**: 64
**MVP Scope**: 22 tasks (Phases 1-3)
**Full Feature**: 64 tasks (all phases)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Performance target: 20 seconds per profile analysis
- Rate limiting: exponential backoff (1s base, 32s max, 5 retries)
- Temporary storage: Encrypted, 24-hour auto-delete
- Platform limits: GitHub 60 req/hour (unauthenticated), LinkedIn best-effort public
