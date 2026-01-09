#!/usr/bin/env python3
"""Test script to verify the fixes for profile analyzer issues"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_extractor_methods():
    """Test that extractors have the extract method"""
    print("Testing extractor methods...")

    # Test LinkedIn extractor
    from src.services.linkedin_extractor import LinkedInExtractor
    linkedin_extractor = LinkedInExtractor()
    has_extract = hasattr(linkedin_extractor, 'extract')
    has_extract_profile = hasattr(linkedin_extractor, 'extract_profile')
    print(f"LinkedInExtractor has 'extract' method: {has_extract}")
    print(f"LinkedInExtractor has 'extract_profile' method: {has_extract_profile}")

    # Test GitHub extractor
    from src.services.github_extractor import GitHubExtractor
    github_extractor = GitHubExtractor()
    has_extract = hasattr(github_extractor, 'extract')
    has_extract_profile = hasattr(github_extractor, 'extract_profile')
    print(f"GitHubExtractor has 'extract' method: {has_extract}")
    print(f"GitHubExtractor has 'extract_profile' method: {has_extract_profile}")

    # Test Portfolio extractor
    from src.services.portfolio_extractor import PortfolioExtractor
    portfolio_extractor = PortfolioExtractor()
    has_extract = hasattr(portfolio_extractor, 'extract')
    has_extract_profile = hasattr(portfolio_extractor, 'extract_profile')
    print(f"PortfolioExtractor has 'extract' method: {has_extract}")
    print(f"PortfolioExtractor has 'extract_profile' method: {has_extract_profile}")

    return has_extract and has_extract_profile

def test_regex_patterns():
    """Test the LinkedIn URL regex pattern"""
    print("\nTesting LinkedIn URL regex pattern...")

    import re
    from src.utils.constants import LINKEDIN_URL_PATTERN

    test_urls = [
        # Valid URLs
        "https://www.linkedin.com/in/username",
        "https://linkedin.com/in/username",
        "http://www.linkedin.com/in/username",
        "https://www.linkedin.com/in/username?trk=public_profile",
        "https://www.linkedin.com/in/username-with-hyphens",
        "https://www.linkedin.com/in/username123",

        # Invalid URLs
        "https://www.linkedin.com/feed/",  # Wrong path
        "https://www.google.com/in/username",  # Wrong domain
        "https://www.linkedin.com/in/",  # No username
    ]

    print(f"Pattern: {LINKEDIN_URL_PATTERN}")
    all_passed = True
    for url in test_urls:
        match = re.match(LINKEDIN_URL_PATTERN, url.lower())
        is_valid = match is not None

        # Determine expected result
        if url in [
            "https://www.linkedin.com/in/username",
            "https://linkedin.com/in/username",
            "http://www.linkedin.com/in/username",
            "https://www.linkedin.com/in/username?trk=public_profile",
            "https://www.linkedin.com/in/username-with-hyphens",
            "https://www.linkedin.com/in/username123",
        ]:
            expected = True
            status = "should pass"
        else:
            expected = False
            status = "should fail"

        result = "PASS" if is_valid == expected else "FAIL"
        if is_valid != expected:
            all_passed = False
        print(f"  {result} {url} - {status}")

    return all_passed

def main():
    print("Testing fixes for profile analyzer issues...\n")

    method_test = test_extractor_methods()
    regex_test = test_regex_patterns()

    print(f"\nOverall test result: {'PASS' if method_test and regex_test else 'FAIL'}")

    if method_test and regex_test:
        print("\n[SUCCESS] All fixes are working correctly!")
        print("- Extractor classes now have 'extract' method as alias to 'extract_profile'")
        print("- LinkedIn URL regex pattern accepts URLs with query parameters")
        return 0
    else:
        print("\n[FAILURE] Some tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())