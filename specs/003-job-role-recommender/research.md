# Research: Job Role Recommender

## Decision: Role Archetype Knowledge Base Structure
**Rationale**: Use YAML files organized by industry for role archetypes, required skills, experience indicators, and seniority markers. YAML provides human-readable format for quarterly updates and easy AI context injection. Each industry file contains role definitions with skill requirements, project indicators, and seniority expectations.
**Alternatives considered**: JSON (less readable), SQL database (overkill for read-heavy use case), hardcoded dictionaries (maintenance burden)

## Decision: Signal Aggregation Approach
**Rationale**: Create a unified ProfileSignals object that normalizes and merges data from Phase 1 (resume) and Phase 2 (portfolio/LinkedIn/GitHub). Use weighted scoring where resume skills are primary, validated by online presence signals. Handle missing Phase 2 data gracefully with reduced confidence.
**Alternatives considered**: Separate analysis per source (loses correlation value), simple concatenation (no normalization)

## Decision: Seniority Detection Heuristics
**Rationale**: Use a three-tier model (junior/mid/senior) based on:
- Years of experience (from resume timeline)
- Project complexity indicators (leadership, scale, architecture decisions)
- Skill depth (breadth vs. specialization patterns)
- GitHub contribution patterns (maintainer vs. contributor)
AI synthesizes these signals with industry-specific calibration.
**Alternatives considered**: Five-tier model (too granular, harder to infer), percentage-based (confusing to users)

## Decision: Role Inference Strategy
**Rationale**: Use Claude CLI with structured prompting that includes:
1. Industry-constrained role archetypes from knowledge base
2. Normalized ProfileSignals
3. Explicit instruction to provide 2-5 roles with justification
4. Conflict-aware reasoning when signals point to multiple paths
Output is structured JSON for reliable parsing.
**Alternatives considered**: Rule-based matching (too rigid), embedding similarity (less explainable)

## Decision: Gap Analysis Depth
**Rationale**: Provide lightweight gap analysis identifying 2-4 key missing skills per role without detailed learning paths. Focus on actionable gaps that are:
- Directly relevant to the recommended role
- Achievable improvements (not career pivots)
- Specific enough to guide next steps
**Alternatives considered**: Comprehensive skill gap inventory (scope creep), no gap analysis (less actionable)

## Decision: Conflicting Signal Handling
**Rationale**: When profile signals suggest multiple career directions (e.g., technical + management), present parallel role paths with clear explanation of how different aspects of the profile align. Use explicit language like "Your technical depth suggests X, while your leadership experience points to Y."
**Alternatives considered**: Force single path (loses information), weighted average (loses nuance)

## Decision: Confidence Indicator Implementation
**Rationale**: Display confidence level (High/Medium/Low) based on:
- Data completeness (all phases vs. partial)
- Signal consistency (aligned vs. conflicting)
- Profile strength (rich detail vs. sparse)
Explicitly communicate what would improve confidence when low.
**Alternatives considered**: Numeric confidence score (less intuitive), no indicator (hides uncertainty)

## Decision: Consent and Anonymization
**Rationale**: Implement opt-in consent for temporary storage with:
- Clear explanation of what's stored and why
- Automatic anonymization (remove PII before storage)
- 24-hour automatic deletion
- Session-scoped access only
**Alternatives considered**: No storage (loses cross-session benefits), implicit consent (privacy concern)