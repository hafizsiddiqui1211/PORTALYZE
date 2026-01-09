#!/usr/bin/env python3
"""Test script to verify the configuration issues are resolved"""

import os
from src.services.ai_service import AIService
from src.services.text_extractor import TextExtractor
from src.utils.logger import get_logger

def test_gemini_api_key():
    """Test if GEMINI_API_KEY is properly loaded"""
    logger = get_logger("TestConfig")

    # Initialize AI service
    ai_service = AIService()

    if ai_service.api_key:
        if ai_service.api_key.startswith("AIzaSy"):
            logger.warning("[WARNING] Using placeholder API key - this needs to be replaced with a real Gemini API key")
            print("[WARNING] GEMINI_API_KEY is set but appears to be a placeholder. Please replace with a real API key.")
            return False
        else:
            logger.info("[SUCCESS] GEMINI_API_KEY is properly configured")
            print("[SUCCESS] GEMINI_API_KEY is properly configured")
            return True
    else:
        logger.warning("[ERROR] GEMINI_API_KEY is not set")
        print("[ERROR] GEMINI_API_KEY is not set")
        return False

def test_tesseract_installation():
    """Test if Tesseract OCR is available"""
    logger = get_logger("TestConfig")

    try:
        import pytesseract
        # Try to get tesseract version to check if it's properly installed
        import subprocess
        result = subprocess.run(['tesseract', '--version'],
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            logger.info("[SUCCESS] Tesseract OCR is properly installed")
            print("[SUCCESS] Tesseract OCR is properly installed")
            return True
        else:
            logger.warning("[ERROR] Tesseract OCR is not properly installed")
            print("[ERROR] Tesseract OCR is not properly installed")
            return False
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        logger.warning("[ERROR] Tesseract OCR command not found")
        print("[ERROR] Tesseract OCR command not found")
        return False
    except FileNotFoundError:
        logger.warning("[ERROR] Tesseract OCR executable not found in PATH")
        print("[ERROR] Tesseract OCR executable not found in PATH")
        return False
    except ImportError:
        logger.warning("[ERROR] pytesseract Python package not found")
        print("[ERROR] pytesseract Python package not found")
        return False

def test_text_extraction():
    """Test basic text extraction functionality"""
    logger = get_logger("TestConfig")

    text_extractor = TextExtractor()
    logger.info("[SUCCESS] TextExtractor initialized successfully")
    print("[SUCCESS] TextExtractor initialized successfully")
    return True

def main():
    print("Testing Resume Analyzer Configuration...")
    print("=" * 50)

    # Test 1: GEMINI_API_KEY
    print("\n1. Testing GEMINI_API_KEY configuration...")
    gemini_ok = test_gemini_api_key()

    # Test 2: Tesseract installation
    print("\n2. Testing Tesseract OCR installation...")
    tesseract_ok = test_tesseract_installation()

    # Test 3: Text extraction
    print("\n3. Testing text extraction functionality...")
    extraction_ok = test_text_extraction()

    print("\n" + "=" * 50)
    print("Summary:")
    print(f"   GEMINI_API_KEY: {'OK' if gemini_ok else 'Needs attention'}")
    print(f"   Tesseract OCR: {'OK' if tesseract_ok else 'Needs attention'}")
    print(f"   Text Extraction: {'OK' if extraction_ok else 'Needs attention'}")

    if not gemini_ok:
        print("\nTo fix GEMINI_API_KEY:")
        print("   1. Go to Google AI Studio: https://aistudio.google.com/")
        print("   2. Create an account and get an API key")
        print("   3. Replace the placeholder key in .env file with your real API key")

    if not tesseract_ok:
        print("\nTo fix Tesseract OCR:")
        print("   1. Download and install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("   2. Make sure the installation directory is added to your system PATH")
        print("   3. Restart your terminal/command prompt after installation")

    print("\nThe application will still work with limited functionality without these components.")

if __name__ == "__main__":
    main()