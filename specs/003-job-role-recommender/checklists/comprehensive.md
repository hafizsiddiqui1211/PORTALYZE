# Requirements Quality Checklist: Job Role Recommender

**Purpose**: Comprehensive requirements quality validation for spec author self-review
**Created**: 2025-12-28
**Feature**: 003-job-role-recommender
**Depth**: Standard (~35 items)
**Audience**: Spec Author

---

## Requirement Completeness

- [ ] CHK001 - Are all supported industries explicitly enumerated (AI/ML, Software Engineering, Data, FinTech, EdTech, etc.)? [Completeness, Spec §FR-001]
- [ ] CHK002 - Are sub-domain/specialization options defined for each industry? [Gap, Spec §FR-002]
- [ ] CHK003 - Are all Phase 1 and Phase 2 input signals explicitly enumerated (skills, experience, projects, etc.)? [Completeness, Spec §FR-004]
- [ ] CHK004 - Are role archetype definitions and structure specified for the knowledge base? [Gap, Spec §FR-005]
- [ ] CHK005 - Are requirements for role card/list UI layout fully specified (fields, ordering, visual hierarchy)? [Gap, Spec §FR-015]
- [ ] CHK006 - Are seniority detection criteria explicitly defined (years of experience thresholds, project complexity metrics)? [Completeness, Spec §FR-006]
- [ ] CHK007 - Are requirements for cross-session recommendation improvements specified? [Gap, Spec §SC-008]

## Requirement Clarity

- [ ] CHK008 - Is "role archetype" defined with specific structure and attributes? [Clarity, Spec §FR-005]
- [ ] CHK009 - Is "clear reasoning" for role recommendations quantified with specific elements (skill match, experience alignment)? [Clarity, Spec §FR-008]
- [ ] CHK010 - Is "high-level improvement suggestion" defined (what level of detail, what format)? [Ambiguity, Spec §FR-011]
- [ ] CHK011 - Is "meaningful skill gap" defined with specific criteria for identification? [Clarity, Spec §SC-007]
- [ ] CHK012 - Is "confidence level" for minimal profile scenarios quantified (High/Medium/Low thresholds)? [Clarity, Spec §SC-011]
- [ ] CHK013 - Is "meaningfully influences" recommendations defined with measurable criteria? [Ambiguity, Spec §SC-003]
- [ ] CHK014 - Are "project signals" explicitly defined (what project attributes are extracted and analyzed)? [Clarity, Spec §FR-005]

## Requirement Consistency

- [ ] CHK015 - Are accuracy percentages (85%, 90%, 80%) consistently defined with measurement methods? [Consistency, Spec §SC-001 through SC-004]
- [ ] CHK016 - Is the "2-5 roles" recommendation range consistently applied across all requirements? [Consistency, Spec §FR-007, SC-006]
- [ ] CHK017 - Are seniority levels (junior, mid, senior) consistently defined across FR-006 and SC-009? [Consistency, Spec §FR-006, SC-009]
- [ ] CHK018 - Are data retention requirements consistent between spec and clarifications (24-hour encrypted storage)? [Consistency, Spec §SC-008 vs Clarifications]

## Acceptance Criteria Quality

- [ ] CHK019 - Can "85% role alignment based on user validation" be objectively measured? Is survey methodology defined? [Measurability, Spec §SC-001]
- [ ] CHK020 - Can "90% recommendations include understandable justification" be objectively measured? [Measurability, Spec §SC-002]
- [ ] CHK021 - Can "80% industry relevance confirmation" be objectively measured? Is survey defined? [Measurability, Spec §SC-003]
- [ ] CHK022 - Can "users can articulate why this role fits" be objectively tested? [Measurability, Spec §SC-004]
- [ ] CHK023 - Are acceptance scenarios in User Stories testable without implementation knowledge? [Measurability, Spec §US-1, US-2, US-3]

## Scenario Coverage

- [ ] CHK024 - Are requirements defined for users who only completed Phase 1 (no portfolio/LinkedIn/GitHub data)? [Coverage, Gap]
- [ ] CHK025 - Are requirements defined for users who skip industry selection (default behavior)? [Coverage, Gap]
- [ ] CHK026 - Are requirements defined for industries with no matching role archetypes in knowledge base? [Coverage, Edge Case]
- [ ] CHK027 - Are requirements defined for profiles with no inferable seniority level? [Coverage, Edge Case]
- [ ] CHK028 - Are requirements defined for handling more than 5 industries selected simultaneously? [Gap, Coverage]

## Edge Case Coverage

- [ ] CHK029 - Is behavior specified for minimal or incomplete profile data (what minimum data is required)? [Edge Case, noted in §Edge Cases]
- [ ] CHK030 - Is behavior specified for conflicting profile signals across multiple domains? [Edge Case, noted in §Edge Cases]
- [ ] CHK031 - Is fallback behavior specified when AI service is unavailable during role inference? [Edge Case, noted in §Edge Cases]
- [ ] CHK032 - Is behavior specified for niche industries with very specific role requirements? [Edge Case, noted in §Edge Cases]
- [ ] CHK033 - Are retry limits and final failure behavior specified for role inference timeouts? [Edge Case, Gap]

## Non-Functional Requirements

- [ ] CHK034 - Is the 30-second performance requirement achievable with current architecture? [NFR, Spec §SC-006]
- [ ] CHK035 - Are encryption requirements specified for temporary profile data storage? [NFR, Spec §SC-008]
- [ ] CHK036 - Are accessibility requirements defined for role recommendation cards/UI? [Gap, NFR]
- [ ] CHK037 - Is concurrent user capacity for role inference defined? [Gap, NFR]
- [ ] CHK038 - Are logging/audit requirements for role recommendations specified? [Gap, NFR]
- [ ] CHK039 - Is knowledge base update mechanism and versioning specified (quarterly updates)? [NFR, Spec §SC-010]

## Dependencies & Assumptions

- [ ] CHK040 - Is the dependency on Phase 1 and Phase 2 completion explicitly documented (required vs optional)? [Dependency, Spec §FR-004]
- [ ] CHK041 - Is the assumption of always-available AI service explicitly stated and risk addressed? [Assumption, Gap]
- [ ] CHK042 - Are external knowledge base maintenance requirements documented (who updates, how often)? [Dependency, Spec §SC-010]
- [ ] CHK043 - Is the dependency on user consent for data storage documented with consent flow? [Dependency, Spec §SC-008]

## Ambiguities & Conflicts

- [ ] CHK044 - Is the conflict between "avoid detailed curriculum" (FR-012) and "improvement suggestions" (FR-011) clarified? [Conflict, Spec §FR-011, FR-012]
- [ ] CHK045 - Is "seamless integration" with Phases 1 and 2 defined with specific integration points? [Ambiguity, Spec §SC-005]
- [ ] CHK046 - Does "concise, scannable cards" have defined visual/interaction specifications? [Ambiguity, Spec §FR-015]
- [ ] CHK047 - Is the handling of conflicting signals fully resolved (three options given in clarifications)? [Ambiguity, Clarifications]

---

## Summary

| Category | Items | Key Gaps Identified |
|----------|-------|---------------------|
| Completeness | 7 | Sub-domain options, role archetype structure, UI layout |
| Clarity | 7 | Role archetype definition, confidence levels, project signals |
| Consistency | 4 | Accuracy measurement methods, seniority definitions |
| Measurability | 5 | Survey methodology, justification quality measurement |
| Scenario Coverage | 5 | Phase 1-only users, default industry behavior |
| Edge Cases | 5 | Minimal profile threshold, retry/timeout behavior |
| Non-Functional | 6 | Accessibility, concurrent capacity, logging |
| Dependencies | 4 | Phase 1/2 optionality, knowledge base maintenance |
| Ambiguities | 4 | Curriculum vs suggestions conflict, integration points |

**Total Items**: 47
