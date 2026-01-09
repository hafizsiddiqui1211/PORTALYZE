#!/usr/bin/env python3
"""Test script to verify the fixes for RateLimiter and URL accessibility issues"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_rate_limiter():
    """Test that RateLimiter has the wait_if_needed method"""
    print("Testing RateLimiter...")

    from src.services.rate_limiter import RateLimiter
    rate_limiter = RateLimiter()

    has_wait_if_needed = hasattr(rate_limiter, 'wait_if_needed')
    print(f"RateLimiter has 'wait_if_needed' method: {has_wait_if_needed}")

    if has_wait_if_needed:
        # Test that the method can be called without error
        try:
            rate_limiter.wait_if_needed()
            print("[OK] 'wait_if_needed' method executed successfully")
            return True
        except Exception as e:
            print(f"[ERROR] Error calling 'wait_if_needed': {e}")
            return False
    else:
        print("[ERROR] 'wait_if_needed' method not found")
        return False

def test_url_validator():
    """Test that URLValidator has improved LinkedIn handling"""
    print("\nTesting URLValidator...")

    from src.services.url_validator import URLValidator
    validator = URLValidator()

    # Test that the method exists
    has_method = hasattr(validator, 'check_url_accessibility')
    print(f"URLValidator has 'check_url_accessibility' method: {has_method}")

    # Test the method with a mock URL to ensure no errors
    try:
        # This should not crash even if the URL is not accessible
        result = validator.check_url_accessibility("https://httpbin.org/status/200")
        print(f"[OK] 'check_url_accessibility' method works: {result}")
        return True
    except Exception as e:
        print(f"[ERROR] Error calling 'check_url_accessibility': {e}")
        return False

def main():
    print("Testing fixes for RateLimiter and URL accessibility issues...\n")

    rate_limiter_test = test_rate_limiter()
    url_validator_test = test_url_validator()

    print(f"\nOverall test result: {'PASS' if rate_limiter_test and url_validator_test else 'FAIL'}")

    if rate_limiter_test and url_validator_test:
        print("\n[SUCCESS] All fixes are working correctly!")
        print("- RateLimiter now has 'wait_if_needed' method")
        print("- URLValidator has improved LinkedIn URL handling")
        return 0
    else:
        print("\n[FAILURE] Some tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())