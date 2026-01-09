#!/usr/bin/env python3
"""Test script to verify .env file loading"""

import os
from dotenv import load_dotenv

def test_env_loading():
    print("Testing .env file loading...")

    # Load environment variables from .env file
    load_dotenv()

    print(f"Current working directory: {os.getcwd()}")
    print(f".env file exists: {os.path.exists('.env')}")

    gemini_key = os.getenv('GEMINI_API_KEY')
    print(f"GEMINI_API_KEY from environment: {gemini_key}")

    if gemini_key:
        if gemini_key.startswith("AIzaSy"):
            print("[OK] GEMINI_API_KEY is loaded (appears to be a placeholder)")
        else:
            print("[OK] GEMINI_API_KEY is loaded (appears to be a real key)")
    else:
        print("[ERROR] GEMINI_API_KEY is not loaded")

    return bool(gemini_key)

if __name__ == "__main__":
    test_env_loading()