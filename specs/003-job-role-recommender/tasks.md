# Tasks: Job Role Recommender

**Input**: Design documents from `/specs/003-job-role-recommender/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/api-contract.md, quickstart.md
**Phase 1 & 2 Dependency**: Extends Phases 1 & 2 - assumes resume analysis and profile analysis foundations are complete

**Tests**: Tests are included as this is a production-grade feature requiring reliability validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and Phase 3 dependencies setup

- [X] T001 Update requirements.txt with Phase 3 dependencies (pydantic, pyyaml, faker)
- [X] T002 [P] Update .env.example with Phase 3 environment variables (ROLE_INFERENCE_TIMEOUT, MAX_ROLES_PER_INDUSTRY, MIN_ROLES_PER_INDUSTRY, CONSENT_STORAGE_HOURS, KNOWLEDGE_BASE_PATH)
- [X] T003 [P] Extend src/utils/constants.py with Phase 3 constants (seniority levels, confidence thresholds, industry list)
- [X] T004 [P] Create src/knowledge/ directory structure with industries/ subdirectory

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create src/models/industry.py with IndustrySelection entity (selection_id, session_id, industries, specializations, selection_timestamp)
- [X] T006 [P] Create src/models/profile_signals.py with ProfileSignals entity (signals_id, resume_signals, profile_signals, aggregated_skills, experience_summary, project_highlights)
- [X] T007 [P] Create src/models/role_recommendation.py with RoleRecommendation and RecommendedRole entities (recommendation_id, roles, overall_confidence, confidence_factors)
- [X] T008 [P] Create src/models/gap_analysis.py with GapAnalysis and SkillGap entities (gap_id, missing_skills, improvement_suggestions, priority_areas)
- [X] T009 Create src/services/knowledge_base.py with RoleArchetype loader from YAML files
- [X] T010 [P] Create src/knowledge/archetypes.yaml with base role archetype schema definition
- [X] T011 [P] Create src/knowledge/industries/ai_ml.yaml with AI/ML role archetypes (ML Engineer, AI App Developer, etc.)
- [X] T012 [P] Create src/knowledge/industries/software_engineering.yaml with Software Engineering role archetypes
- [X] T013 [P] Create src/knowledge/industries/data.yaml with Data role archetypes (Data Scientist, Data Engineer, etc.)
- [X] T014 [P] Create src/knowledge/industries/fintech.yaml with FinTech role archetypes
- [X] T015 [P] Create src/knowledge/industries/edtech.yaml with EdTech role archetypes
- [X] T016 Create src/utils/anonymizer.py with PII removal utilities (names, emails, companies, locations)
- [X] T017 Create src/services/consent_manager.py with consent request, storage, and expiry logic
- [X] T018 Update tests/conftest.py with Phase 3 fixtures (mock signals, mock industry selections, mock role archetypes)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Industry Selection and Role Inference (Priority: P1) MVP

**Goal**: Enable users to select target industries and receive relevant role recommendations based on their profile data

**Independent Test**: Select one or more industries, provide profile data from Phases 1 & 2, and verify the system generates 2-5 relevant role recommendations with clear justifications per industry

### Tests for User Story 1

- [X] T019 [P] [US1] Create tests/unit/test_services/test_signal_aggregator.py with signal aggregation tests (resume + profile merging)
- [X] T020 [P] [US1] Create tests/unit/test_services/test_role_inferencer.py with role inference tests (mock Claude CLI responses)
- [X] T021 [P] [US1] Create tests/unit/test_models/test_industry.py with IndustrySelection entity validation tests

### Implementation for User Story 1

- [X] T022 [US1] Implement src/services/signal_aggregator.py with Phase 1 & 2 signal merging (resume + LinkedIn + GitHub + Portfolio)
- [X] T023 [US1] Add skill normalization and validation strength calculation in src/services/signal_aggregator.py
- [X] T024 [US1] Add experience summary extraction in src/services/signal_aggregator.py (years, domains, leadership indicators)
- [X] T025 [US1] Implement src/services/role_inferencer.py with Claude CLI integration for role inference
- [X] T026 [US1] Add industry-constrained role archetype loading in src/services/role_inferencer.py
- [X] T027 [US1] Add structured prompting for 2-5 role recommendations in src/services/role_inferencer.py
- [X] T028 [US1] Create src/ui/components/industry_selector.py with Streamlit multi-select for industries
- [X] T029 [US1] Add specialization sub-selector in src/ui/components/industry_selector.py for applicable industries
- [X] T030 [US1] Create src/ui/components/role_card.py with role recommendation display (title, industry, fit score)
- [X] T031 [US1] Update src/main.py to add "Role Recommendations" tab with industry selection flow
- [X] T032 [US1] Add timeout handling (30 seconds) for role inference in src/services/role_inferencer.py
- [X] T033 [US1] Add AI service unavailability handling with graceful error messaging

**Checkpoint**: User Story 1 complete - users can select industries and receive role recommendations

---

## Phase 4: User Story 2 - AI-Driven Role Mapping and Justification (Priority: P2)

**Goal**: Provide clear, understandable justification for each recommended role explaining skill alignment, project relevance, and technology match

**Independent Test**: Review role recommendations and verify each includes specific justification with skill alignment, project relevance, technology match, and experience alignment that users can articulate

### Tests for User Story 2

- [X] T034 [P] [US2] Create tests/unit/test_services/test_justification_generator.py with justification generation tests
- [X] T035 [P] [US2] Create tests/unit/test_services/test_seniority_detector.py with seniority detection tests (junior/mid/senior)

### Implementation for User Story 2

- [X] T036 [US2] Create src/services/seniority_detector.py with three-tier seniority detection (junior, mid, senior)
- [X] T037 [US2] Add experience-based seniority heuristics in src/services/seniority_detector.py (years, complexity, leadership)
- [X] T038 [US2] Add GitHub contribution pattern analysis for seniority in src/services/seniority_detector.py
- [X] T039 [US2] Extend src/services/role_inferencer.py with detailed justification generation (skill_alignment, project_relevance, technology_match, experience_alignment)
- [X] T040 [US2] Add justification summary generation (1-2 sentence overview) in src/services/role_inferencer.py
- [X] T041 [US2] Update src/ui/components/role_card.py to display justification bullets
- [X] T042 [US2] Create src/ui/components/justification_panel.py with expandable justification details
- [X] T043 [US2] Add seniority level badge display in src/ui/components/role_card.py (JUNIOR/MID/SENIOR)
- [X] T044 [US2] Add conflicting signal handling with multiple role paths in src/services/role_inferencer.py
- [X] T045 [US2] Display conflict explanations in src/ui/components/role_card.py when applicable

**Checkpoint**: User Story 2 complete - role recommendations include clear, understandable justifications

---

## Phase 5: User Story 3 - Gap Analysis and Role Alignment Insights (Priority: P3)

**Goal**: Provide lightweight gap analysis showing missing skills for recommended roles with high-level improvement suggestions

**Independent Test**: Analyze a profile against recommended roles and verify system identifies 2-4 missing skills per role with importance levels and brief improvement suggestions without detailed curriculum

### Tests for User Story 3

- [X] T046 [P] [US3] Create tests/unit/test_services/test_gap_analyzer.py with gap analysis tests (skill gaps, importance levels)
- [X] T047 [P] [US3] Create tests/unit/test_models/test_gap_analysis.py with GapAnalysis entity validation tests

### Implementation for User Story 3

- [X] T048 [US3] Implement src/services/gap_analyzer.py with skill comparison against role archetypes
- [X] T049 [US3] Add importance level assignment in src/services/gap_analyzer.py (CRITICAL, IMPORTANT, NICE_TO_HAVE)
- [X] T050 [US3] Add high-level improvement suggestions generation in src/services/gap_analyzer.py (no detailed curriculum)
- [X] T051 [US3] Add priority areas identification in src/services/gap_analyzer.py (most important gaps first)
- [X] T052 [US3] Create src/ui/components/gap_display.py with missing skills display (color-coded by importance)
- [X] T053 [US3] Add improvement suggestion display in src/ui/components/gap_display.py
- [X] T054 [US3] Update src/ui/components/role_card.py to include gap analysis section
- [X] T055 [US3] Integrate gap analysis with role inference output in src/services/role_inferencer.py

**Checkpoint**: User Story 3 complete - role recommendations include gap analysis with improvement suggestions

---

## Phase 6: Confidence and Consent Management (Cross-Story Feature)

**Goal**: Display confidence indicators for recommendations and manage user consent for temporary data storage

**Independent Test**: Generate recommendations with varying data completeness and verify appropriate confidence levels (High/Medium/Low) are displayed with explanations of confidence factors

### Tests for Confidence and Consent

- [X] T056 [P] Create tests/unit/test_services/test_consent_manager.py with consent flow and expiry tests
- [X] T057 [P] Create tests/unit/test_services/test_confidence_calculator.py with confidence level calculation tests

### Implementation for Confidence and Consent

- [X] T058 Create src/services/confidence_calculator.py with confidence level calculation (HIGH/MEDIUM/LOW based on data completeness)
- [X] T059 Add confidence factors explanation in src/services/confidence_calculator.py (what would improve confidence)
- [X] T060 Create src/ui/components/confidence_badge.py with confidence indicator display (color-coded badge)
- [X] T061 Add confidence factors tooltip/explanation in src/ui/components/confidence_badge.py
- [X] T062 Create src/ui/components/consent_dialog.py with consent request UI
- [X] T063 Add consent explanation in src/ui/components/consent_dialog.py (what's stored, why, how long)
- [X] T064 Integrate consent flow with signal aggregation in src/services/signal_aggregator.py
- [X] T065 Add anonymization before storage in src/utils/anonymizer.py integration with consent_manager.py
- [X] T066 Add 24-hour auto-deletion logic in src/services/consent_manager.py

**Checkpoint**: Confidence and consent management complete

---

## Phase 7: Dashboard Integration (Cross-Story Feature)

**Goal**: Integrate Phase 3 role recommendations with Phases 1 & 2 in unified dashboard

**Independent Test**: Complete resume + profile analysis + role recommendations and verify unified dashboard shows all insights with proper navigation between phases

### Tests for Dashboard Integration

- [X] T067 [P] Create tests/integration/test_role_recommendation_flow.py with end-to-end recommendation workflow tests

### Implementation for Dashboard Integration

- [X] T068 Update src/ui/dashboard.py to add Role Recommendations section alongside Resume and Profile Analysis
- [X] T069 Create src/ui/components/recommendation_summary.py with role recommendations overview
- [X] T070 Add tab navigation in src/ui/dashboard.py for Resume / Profiles / Role Recommendations / Combined View
- [X] T071 Create src/ui/components/combined_career_insights.py with cross-phase synthesis
- [X] T072 Update PDF report generation in src/services/pdf_generator.py to include role recommendations
- [X] T073 Add seamless data flow from Phase 1 & 2 to Phase 3 in src/main.py

**Checkpoint**: Dashboard integration complete - unified view across all three phases

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T074 [P] Add comprehensive logging in all services for debugging (inference attempts, confidence calculations, consent events)
- [X] T075 [P] Performance optimization for 30-second recommendation target (parallel archetype loading, caching)
- [X] T076 [P] Update quickstart.md with final Phase 3 setup and usage instructions
- [X] T077 Run quickstart.md validation to verify setup instructions work
- [X] T078 Security review for anonymization and consent handling
- [X] T079 [P] Add graceful degradation for minimal profile data (best-effort recommendations with low confidence)
- [X] T080 Edge case handling for conflicting signals across multiple domains
- [X] T081 Knowledge base validation utility for quarterly updates in src/services/knowledge_base.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Depends on Phases 1 & 2 (resume and profile analysis) being complete
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - industry selection and role inference
- **User Story 2 (Phase 4)**: Depends on US1 (needs role recommendations to add justifications)
- **User Story 3 (Phase 5)**: Depends on US2 (needs roles with justifications to add gap analysis)
- **Confidence/Consent (Phase 6)**: Depends on Foundational - can parallel with US1-US3
- **Dashboard Integration (Phase 7)**: Depends on US3 completion + Phases 1 & 2 integration
- **Polish (Phase 8)**: Depends on all user stories and integration being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - Core role inference
- **User Story 2 (P2)**: Depends on US1 (needs role recommendations as input)
- **User Story 3 (P3)**: Depends on US2 (needs roles with seniority for gap analysis)

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before UI components
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- T002, T003, T004 can run in parallel (Setup phase)
- T006, T007, T008 can run in parallel (Models in Foundational)
- T010, T011, T012, T013, T014, T015 can run in parallel (Knowledge base YAML files)
- T019, T020, T021 can run in parallel (US1 tests)
- T034, T035 can run in parallel (US2 tests)
- T046, T047 can run in parallel (US3 tests)
- T056, T057 can run in parallel (Confidence/Consent tests)
- T074, T075, T076, T079 can run in parallel (Polish phase)

---

## Parallel Example: Foundational Phase

```bash
# Launch all models in parallel:
Task: "Create src/models/profile_signals.py" [T006]
Task: "Create src/models/role_recommendation.py" [T007]
Task: "Create src/models/gap_analysis.py" [T008]

# Launch all knowledge base YAML files in parallel:
Task: "Create src/knowledge/industries/ai_ml.yaml" [T011]
Task: "Create src/knowledge/industries/software_engineering.yaml" [T012]
Task: "Create src/knowledge/industries/data.yaml" [T013]
Task: "Create src/knowledge/industries/fintech.yaml" [T014]
Task: "Create src/knowledge/industries/edtech.yaml" [T015]
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T018)
3. Complete Phase 3: User Story 1 (T019-T033)
4. **STOP and VALIDATE**: Test industry selection and role inference independently
5. Deploy/demo if ready - users can get basic role recommendations!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (basic recommendations MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo (with justifications)
4. Add User Story 3 → Test independently → Deploy/Demo (with gap analysis)
5. Add Confidence/Consent → Test independently → Deploy/Demo (production-ready)
6. Add Dashboard Integration → Test independently → Deploy/Demo (unified view)
7. Polish → Final validation → Production release

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Developer A works on knowledge base YAML files (can start early)
3. Once Foundational is done:
   - Developer A: User Story 1 (role inference)
   - Developer B: Confidence/Consent (can parallel)
4. After US1 complete:
   - Developer A: User Story 2 (justifications)
   - Developer B: Continue Confidence/Consent
5. After US2 complete:
   - Developer A: User Story 3 (gap analysis)
   - Developer B: Dashboard Integration preparation
6. Stories complete and integrate into unified dashboard

---

## Summary

| Phase | Tasks | Parallel Opportunities |
|-------|-------|----------------------|
| Setup | 4 (T001-T004) | 3 tasks parallelizable |
| Foundational | 14 (T005-T018) | 10 tasks parallelizable |
| US1 (MVP) | 15 (T019-T033) | 3 test tasks parallelizable |
| US2 (Justification) | 12 (T034-T045) | 2 test tasks parallelizable |
| US3 (Gap Analysis) | 10 (T046-T055) | 2 test tasks parallelizable |
| Confidence/Consent | 11 (T056-T066) | 2 test tasks parallelizable |
| Dashboard Integration | 7 (T067-T073) | 1 test task parallelizable |
| Polish | 8 (T074-T081) | 4 tasks parallelizable |

**Total Tasks**: 81
**MVP Scope**: 33 tasks (Phases 1-3)
**Full Feature**: 81 tasks (all phases)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Performance target: 30 seconds for role recommendations
- Seniority detection: Three-tier model (junior/mid/senior)
- Confidence levels: High/Medium/Low based on data completeness
- Consent required for temporary storage (24-hour auto-delete)
- Knowledge base: YAML files for quarterly updates
- No detailed learning paths/curriculum (future scope)
