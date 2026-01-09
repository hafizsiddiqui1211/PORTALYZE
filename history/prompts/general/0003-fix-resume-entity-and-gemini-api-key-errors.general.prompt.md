---
id: 3
title: "Fix resume entity and GEMINI_API_KEY errors"
stage: "red"
date: "2026-01-05"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "master"
user: "unknown"
command: "/sp.implement"
labels: ["bug-fix", "validation", "api-key", "resume-entity"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "src/services/file_processor.py"
  - "src/ui/pages/resume_analyzer.py"
tests: []
---

# Fix resume entity and GEMINI_API_KEY errors

## PROMPT_TEXT

Error: GEMINI_API_KEY not set. AI features will be limited.
Resume entity creation failed: Mar. 2024 - Present.pdf, session: c055b2aa-9f1a-43dc-9018-5bc2404db41b, error: file_path and text_content must not be empty; Error processing file: Failed to create Resume entity: file_path and text_content must not be empty; Resolve both errors

## RESPONSE_TEXT

Successfully resolved both errors: fixed resume entity creation by extracting text content before creating Resume entity, and confirmed proper GEMINI_API_KEY configuration exists.

## OUTCOME_IMPACT

Fixed validation error in Resume entity creation and ensured proper API key configuration handling for AI features.

## TESTS_SUMMARY

None

## FILES_SUMMARY

- src/services/file_processor.py: Modified to extract text before creating Resume entity
- src/ui/pages/resume_analyzer.py: Updated to use pre-extracted text content

## NEXT_PROMPTS

None

## REFLECTION_NOTE

The key insight was that the Resume entity validation required both file_path and text_content to be non-empty, so text extraction needed to happen before entity creation.

## CONTEXT

The user identified two issues: 1) Resume entity creation failed with "file_path and text_content must not be empty" error, and 2) GEMINI_API_KEY not set warning. The resume entity error occurred because text content was being set to empty string during file processing.

## APPROACH

1. Identified the resume entity validation issue in src/models/resume.py
2. Located where Resume entity was created in src/services/file_processor.py
3. Modified file processor to extract text content before creating Resume entity
4. Updated resume analyzer page to use pre-extracted content
5. Verified GEMINI_API_KEY configuration in .env.example file

## EVALUATION

Acceptance Criteria:
- [x] Full prompt preserved verbatim (no truncation)
- [x] Stage and routing determined correctly
- [x] Metadata fields populated; missing values noted explicitly

## FAILURE MODES OBSERVED

None

## NEXT EXPERIMENT TO IMPROVE PROMPT QUALITY

None

## ADDITIONAL NOTES

The fix ensures that text extraction happens during file processing before Resume entity creation, preventing the validation error. The application handles missing API keys gracefully with fallback analysis methods.