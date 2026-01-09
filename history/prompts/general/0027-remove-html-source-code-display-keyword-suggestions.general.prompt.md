---
id: "0027"
title: "Remove HTML Source Code Display in Keyword Suggestions"
stage: "general"
date_iso: "2026-01-09"
surface: "agent"
model: "Sonnet 4.5"
feature: "none"
branch: "master"
user: "user"
command: "sp.implement"
labels: ["keyword-suggestions", "ui", "display", "html", "source-code", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - E:\Paralyzer\src\ui\components\keyword_suggestions.py
tests_yaml: |
  - "Manual verification of keyword suggestions display without HTML source"
---

# Remove HTML Source Code Display in Keyword Suggestions

## User Input
Don't show these source code in suggestions: <div style="margin-bottom: 8px;"> <strong style="color: #495057;">Category:</strong> <span style="background-color: #e9ecef; padding: 2px 6px; border-radius: 4px; margin-left: 8px; font-size: 0.9em;"> Technical </span> </div> ... (user provided HTML code that was appearing in the UI)

## Response Text
Fixed the keyword suggestions display to prevent raw HTML source code from appearing in the UI. Previously, the implementation was showing raw HTML tags instead of properly rendered elements. I've updated the `_render_single_keyword_card` function to use a combination of Streamlit's native components and minimal HTML for styling only where necessary.

The changes include:
1. Restructured the card layout using Streamlit's container and column components
2. Used Streamlit's expander for implementation tips instead of HTML details/summary
3. Maintained visual appeal with minimal CSS styling applied via Streamlit's markdown function
4. Created a new helper function `_get_implementation_tips_list` that returns a list of strings instead of HTML
5. Removed the old `_get_implementation_tips_html` function

The UI now properly renders keyword suggestions with their relevance scores without exposing any HTML source code to the user, while maintaining the same visual quality and functionality.

## Technical Details
- Modified `_render_single_keyword_card` to use Streamlit components with minimal HTML styling
- Replaced HTML details/summary with Streamlit's expander component
- Changed implementation tips from HTML to a list-based approach
- Used Streamlit's columns for responsive layout
- Maintained color coding based on relevance scores
- Preserved all original functionality (keyword, score, category, role alignment, justification, tips)

## Follow-up Actions
- Test the keyword suggestions display to ensure no raw HTML appears
- Verify that the visual presentation remains clean and professional
- Confirm that all functionality is preserved

## Outcome
Keyword suggestions now display properly formatted content without exposing raw HTML source code, satisfying the user's requirement while maintaining the visual quality and functionality.