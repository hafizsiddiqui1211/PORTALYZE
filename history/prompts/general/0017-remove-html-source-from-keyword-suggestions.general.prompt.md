---
id: "0017"
title: "Remove HTML Source from Keyword Suggestions"
stage: "general"
date_iso: "2026-01-09"
surface: "agent"
model: "Sonnet 4.5"
feature: "none"
branch: "master"
user: "user"
command: "sp.implement"
labels: ["keyword-suggestions", "ui", "html", "clean-display", "enhancement"]
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

# Remove HTML Source from Keyword Suggestions

## User Input
I don't want these type of source code display in keyword suggestions like this: <div style="margin-bottom: 8px;">
    <strong>Category:</strong>
    <span style="background-color: #e9ecef; padding: 2px 6px; border-radius: 4px; font-size: 0.9em;">
        Technical
    </span>
</div>

<div style="margin-bottom: 8px;">
    <strong>Role Alignment:</strong> Software Engineer
</div>

<div>
    <strong>Justification:</strong> JavaScript is essential for modern web development and Software Engineer positions
</div>

## Response Text
Completely removed all HTML/CSS source code from the keyword suggestions display. The implementation now uses only Streamlit's native components (st.subheader, st.metric, st.write, st.divider) instead of raw HTML strings. This provides a cleaner UI without exposing any HTML source code to the user while maintaining the same functionality and visual presentation.

## Technical Details
- Replaced the HTML-based card rendering in `_render_single_keyword_card` function
- Changed from using `st.markdown(card_html, unsafe_allow_html=True)` with HTML strings
- Now uses Streamlit's native components: `st.subheader`, `st.metric`, `st.write`, and `st.divider`
- Maintained the same information display (keyword, relevance score, category, role alignment, justification)
- Removed all inline CSS and HTML div elements

## Follow-up Actions
- Test the keyword suggestions display to ensure it renders properly
- Verify that no HTML source code is visible to the user

## Outcome
Keyword suggestions now display using Streamlit's native components without exposing any HTML source code, providing a cleaner and more appropriate user interface.