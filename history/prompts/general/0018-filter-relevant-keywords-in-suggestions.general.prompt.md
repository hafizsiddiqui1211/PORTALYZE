---
id: "0018"
title: "Filter Relevant Keywords in Suggestions"
stage: "general"
date_iso: "2026-01-09"
surface: "agent"
model: "Sonnet 4.5"
feature: "none"
branch: "master"
user: "user"
command: "sp.implement"
labels: ["keyword-suggestions", "filtering", "relevance", "enhancement"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - E:\Paralyzer\src\services\keyword_analyzer.py
tests_yaml: |
  - "Manual verification of keyword suggestions filtering"
---

# Filter Relevant Keywords in Suggestions

## User Input
only show relevant keywords after analysis in keyword suggestions

## Response Text
Modified the keyword suggestions generation to only show truly relevant keywords by implementing stricter filtering. The changes ensure that:

1. Only keywords with relevance score < 0.7 are suggested (meaning they're missing or underrepresented in the resume)
2. Additional validation that keywords are truly relevant to the target role by checking against role-specific keywords
3. Proper sorting to show the most needed keywords first

This ensures that keyword suggestions are more targeted and relevant to improving the resume for the specific target role.

## Technical Details
- Modified `generate_keyword_suggestions` method in `KeywordAnalyzer` class
- Changed relevance threshold from < 0.5 to < 0.7 for more inclusive filtering
- Added additional validation to ensure keywords are in the role-specific keywords list
- Adjusted sorting to show most needed keywords first (by ascending relevance score)
- Maintained the limit of top 10 suggestions

## Follow-up Actions
- Test the keyword suggestions with various resumes to ensure relevancy
- Verify that only truly relevant and missing keywords are suggested

## Outcome
Keyword suggestions now only show relevant keywords that are missing or underrepresented in the resume, specifically tailored to the target role.