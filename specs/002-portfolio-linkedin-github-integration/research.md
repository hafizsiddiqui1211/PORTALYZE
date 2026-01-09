# Research: Portfolio + LinkedIn / GitHub Integration

## Decision: LinkedIn Data Extraction Approach
**Rationale**: Use public profile scraping via BeautifulSoup4 for accessible LinkedIn profiles. LinkedIn's public profiles expose headline, summary, and experience sections without authentication. This respects platform boundaries while providing valuable data.
**Alternatives considered**: LinkedIn API (requires OAuth, not suitable for quick analysis), Selenium automation (complex, slower, detection risk), third-party scraping services (cost, privacy concerns)

## Decision: GitHub Data Extraction Approach
**Rationale**: Use PyGithub library with GitHub's public REST API for repository data extraction. This provides structured access to repositories, README content, stars, forks, and activity without authentication for public profiles. Rate limits are generous for public data (60 requests/hour unauthenticated).
**Alternatives considered**: Direct REST API calls (more boilerplate), GraphQL API (requires authentication), web scraping (less reliable than API)

## Decision: Portfolio Website Extraction Approach
**Rationale**: Use BeautifulSoup4 with requests/httpx for HTML parsing. Focus on main page and linked project pages only to maintain performance. Extract bio/about sections, project descriptions, skills lists, and contact visibility using semantic HTML patterns.
**Alternatives considered**: Playwright/Selenium for JavaScript-heavy sites (slower, complex), full site crawling (performance risk), screenshot-based analysis (inaccurate)

## Decision: Rate Limiting Implementation
**Rationale**: Implement exponential backoff with jitter using tenacity library. Start with 1-second delay, double on each retry up to 32 seconds, maximum 5 retries. Notify user of delays via Streamlit progress indicators.
**Alternatives considered**: Fixed delay retries (less adaptive), circuit breaker pattern (overkill for single-user), fail-fast (poor UX)

## Decision: Resume-Profile Alignment Algorithm
**Rationale**: Use semantic similarity comparison for skills, experience, and projects. Compare extracted profile elements against Phase 1 resume analysis results. Generate alignment score (0-100%) based on keyword overlap, skill matching, and project relevance. Highlight discrepancies for user attention.
**Alternatives considered**: Simple keyword matching (shallow), LLM-based comparison only (slower, costlier), manual rule-based matching (inflexible)

## Decision: Content Normalization Strategy
**Rationale**: Normalize all extracted content into structured ProfileData objects with consistent fields (summary, skills, projects, experience). Use AI (Gemini API) to clean and structure raw HTML content into analyzable text blocks.
**Alternatives considered**: Raw text storage (inconsistent), fixed templates (inflexible), manual formatting rules (maintenance burden)

## Decision: Graceful Degradation Approach
**Rationale**: When parsing fails or content is minimal, extract whatever is available and clearly indicate limitations to the user. Provide partial analysis with confidence indicators rather than failing entirely.
**Alternatives considered**: Strict validation (fails too often), silent fallback (confuses users), mock data filling (inaccurate)