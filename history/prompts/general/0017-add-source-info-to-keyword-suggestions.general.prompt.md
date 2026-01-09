---
id: "0017"
title: "Add Source Info to Keyword Suggestions"
stage: "general"
date_iso: "2026-01-09"
surface: "agent"
model: "Sonnet 4.5"
feature: "none"
branch: "master"
user: "user"
command: "sp.implement"
labels: ["keyword-suggestions", "ui", "source-information", "enhancement"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - E:\Paralyzer\src\ui\components\keyword_suggestions.py
tests_yaml: |
  - "Manual verification of keyword suggestion display"
---

# Add Source Info to Keyword Suggestions

## User Input
In keyword suggestions of resume analyzer only shows keywords don't show their source code

## Response Text
Enhanced the keyword suggestions display to include source information about where the suggestions originate from. Added a collapsible "Source Information" section to each keyword suggestion card that shows:
- Analysis ID that generated the suggestion
- Service that generated the suggestion (KeywordAnalyzer)
- Data source (keyword_mappings.json template)

This addresses the user's concern about seeing where the keyword suggestions come from by providing transparency about the source of each suggestion.

## Technical Details
- Modified the `_render_single_keyword_card` function in `src/ui/components/keyword_suggestions.py`
- Added a `<details>` HTML element to show source information in a collapsible section
- Included relevant metadata like Analysis ID, generating service, and data source
- Maintained the existing visual design while adding the source information section

## Follow-up Actions
- Test the keyword suggestions display to ensure source information is visible
- Verify that the collapsible section works properly in the UI

## Outcome
Keyword suggestions now display source information in addition to the keyword, relevance score, category, and justification, providing users with more transparency about where the suggestions originate from.