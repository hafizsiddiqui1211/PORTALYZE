#!/usr/bin/env python3
"""Test script to verify LinkedIn URL pattern fix"""

import re

# The new pattern from constants.py
LINKEDIN_URL_PATTERN = r'^https?://(www\.)?linkedin\.com/in/[^/]+(\?.*)?$'

# Test URLs
test_urls = [
    # Valid URLs that should pass
    "https://www.linkedin.com/in/username",
    "https://linkedin.com/in/username",
    "http://www.linkedin.com/in/username",
    "http://linkedin.com/in/username",
    "https://www.linkedin.com/in/username?trk=public_profile",
    "https://www.linkedin.com/in/username?utm_source=share&utm_medium=member_desktop",
    "https://www.linkedin.com/in/username-with-hyphens",
    "https://www.linkedin.com/in/username123",
    "https://www.linkedin.com/in/username_underscore",

    # Invalid URLs that should fail
    "https://www.linkedin.com/in/",  # No username
    "https://www.linkedin.com/feed/",  # Not in/ path
    "https://www.google.com/in/username",  # Wrong domain
    "ftp://www.linkedin.com/in/username",  # Wrong protocol
    "https://www.linkedin.com/in/username/extra",  # Extra path segment
]

print("Testing LinkedIn URL pattern:")
print(f"Pattern: {LINKEDIN_URL_PATTERN}")
print()

for url in test_urls:
    match = re.match(LINKEDIN_URL_PATTERN, url.lower())
    result = "PASS" if match else "FAIL"
    expected = "should pass" if url.startswith(("https://", "http://")) and "/in/" in url and not url.endswith("/extra") and not url.endswith("/in/") else "should fail"

    # More specific expected results
    if url in [
        "https://www.linkedin.com/in/username",
        "https://linkedin.com/in/username",
        "http://www.linkedin.com/in/username",
        "http://linkedin.com/in/username",
        "https://www.linkedin.com/in/username?trk=public_profile",
        "https://www.linkedin.com/in/username?utm_source=share&utm_medium=member_desktop",
        "https://www.linkedin.com/in/username-with-hyphens",
        "https://www.linkedin.com/in/username123",
        "https://www.linkedin.com/in/username_underscore",
    ]:
        expected = "should pass"
    else:
        expected = "should fail"

    status = "CORRECT" if (match is not None) == (expected == "should pass") else "INCORRECT"
    print(f"[{result}] {url} - {expected} [{status}]")

print("\nTest completed!")