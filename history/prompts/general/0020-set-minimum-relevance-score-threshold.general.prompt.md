---
id: "0020"
title: "Set Minimum Relevance Score Threshold"
stage: "general"
date_iso: "2026-01-09"
surface: "agent"
model: "Sonnet 4.5"
feature: "none"
branch: "master"
user: "user"
command: "sp.implement"
labels: ["keyword-suggestions", "relevance", "threshold", "enhancement"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - E:\Paralyzer\src\services\keyword_analyzer.py
tests_yaml: |
  - "Manual verification of keyword suggestions relevance threshold"
---

# Set Minimum Relevance Score Threshold

## User Input
Show only those keywords in suggestions who are minimum some relevance score

## Response Text
Implemented a minimum relevance score threshold in the keyword suggestions algorithm. The changes ensure that only keywords with a relevance score within the range of 0.2 to 0.7 are included in suggestions. This ensures:

1. Keywords have a minimum relevance score (>= 0.2) to ensure they are meaningful
2. Keywords are still missing or underrepresented in the resume (< 0.7) to be worth suggesting
3. Irrelevant keywords with very low scores are filtered out
4. Only truly relevant keywords that would improve the resume are suggested

## Technical Details
- Modified the `generate_keyword_suggestions` method in `KeywordAnalyzer` class
- Added condition `relevance_score >= 0.2` to ensure minimum relevance
- Maintained the existing condition `relevance_score < 0.7` for missing/underrepresented keywords
- Combined both conditions with `and` operator: `if relevance_score < 0.7 and relevance_score >= 0.2`
- Preserved all other functionality including role-specific filtering and duplicate removal

## Follow-up Actions
- Test keyword suggestions with various resumes to ensure appropriate relevance filtering
- Verify that suggestions contain only appropriately relevant keywords

## Outcome
Keyword suggestions now only include keywords that meet the minimum relevance score threshold, ensuring higher quality and more meaningful suggestions.