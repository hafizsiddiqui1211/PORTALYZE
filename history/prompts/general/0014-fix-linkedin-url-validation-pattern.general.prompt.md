---
id: "0014"
title: "Fix LinkedIn URL Validation Pattern"
stage: "general"
date_iso: "2026-01-09"
surface: "agent"
model: "Sonnet 4.5"
feature: "none"
branch: "master"
user: "user"
command: "sp.implement"
labels: ["url-validation", "linkedin", "regex", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - E:\Paralyzer\src\utils\constants.py
tests_yaml: |
  - "Regex pattern validation tests"
  - "URL validation with query parameters"
---

# Fix LinkedIn URL Validation Pattern

## User Input
Resolve this issue: Invalid Linkedin URL: Invalid LinkedIn URL format. Expected pattern: ^https?://(www.)?linkedin.com/in/[^/]+$

## Response Text
Fixed the LinkedIn URL validation regex pattern to accept URLs with query parameters. The original pattern `^https?://(www\.)?linkedin\.com/in/[^/]+$` was too restrictive and didn't allow for query parameters like `?trk=public_profile` that are commonly found in LinkedIn profile URLs.

The pattern has been updated to `^https?://(www\.)?linkedin\.com/in/[^/]+(\?.*)?$` which allows for optional query parameters after the username.

## Technical Details
- Changed LINKEDIN_URL_PATTERN in src/utils/constants.py from `^https?://(www\.)?linkedin\.com/in/[^/]+$` to `^https?://(www\.)?linkedin\.com/in/[^/]+(\?.*)?$`
- The new pattern allows URLs like:
  - `https://www.linkedin.com/in/username`
  - `https://www.linkedin.com/in/username?trk=public_profile`
  - `https://www.linkedin.com/in/username?utm_source=share&utm_medium=member_desktop`
- The pattern still rejects invalid URLs appropriately

## Follow-up Actions
- Test with various LinkedIn profile URL formats
- Verify that other URL validation patterns remain unaffected

## Outcome
LinkedIn profile URLs with query parameters are now properly validated, resolving the validation error.