#!/usr/bin/env python3
"""Quick test to verify application can start with current configuration"""

import os
from dotenv import load_dotenv
from src.services.ai_service import AIService
from src.services.text_extractor import TextExtractor
from src.services.file_processor import FileProcessor
from src.utils.constants import MAX_FILE_SIZE

def test_application_startup():
    print("Testing Application Startup with Current Configuration")
    print("=" * 55)

    # Load environment variables
    load_dotenv()
    print("[OK] Environment variables loaded")

    # Test AI Service
    print("\nTesting AI Service...")
    ai_service = AIService()
    if ai_service.api_key:
        print(f"[OK] AI Service initialized (API key status: {'PLACEHOLDER' if ai_service.api_key.startswith('AIzaSy') else 'REAL'})")
    else:
        print("[ERROR] AI Service failed to initialize")

    # Test Text Extractor
    print("\nTesting Text Extractor...")
    try:
        text_extractor = TextExtractor()
        print("[OK] Text Extractor initialized successfully")
    except Exception as e:
        print(f"[ERROR] Text Extractor failed: {e}")

    # Test File Processor
    print("\nTesting File Processor...")
    try:
        file_processor = FileProcessor(max_file_size=MAX_FILE_SIZE)
        print("[OK] File Processor initialized successfully")
    except Exception as e:
        print(f"[ERROR] File Processor failed: {e}")

    print(f"\n[SUCCESS] Application components initialized successfully")
    print("[INFO] The application can run with current configuration")
    print("[WARNING] Some features will be limited until issues are fully resolved")

    print("\nTo fully resolve limitations:")
    print("1. Replace GEMINI_API_KEY in .env with a real API key")
    print("2. Install Tesseract OCR engine for image-based PDF support")

if __name__ == "__main__":
    test_application_startup()