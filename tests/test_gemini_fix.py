#!/usr/bin/env python3
"""
Test script to verify the Gemini API fixes
Tests file upload and processing with retry logic
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.sp_methodology_analyzer import SPMethodologyAnalyzer


def test_sp_methodology_analysis():
    """Test S&P methodology analysis with retry logic"""
    print("Testing S&P methodology analysis with retry logic...")

    # Check if API key is set
    if not os.getenv('GEMINI_API_KEY'):
        print("Error: GEMINI_API_KEY environment variable is required")
        return False

    # Check if S&P document exists
    sp_document = "./doc_assets/sp_float.pdf"
    if not os.path.exists(sp_document):
        print(f"Error: S&P document not found at {sp_document}")
        print("Please ensure the S&P float methodology document is available")
        return False

    try:
        # Initialize analyzer
        analyzer = SPMethodologyAnalyzer()

        print("Step 1: Analyzing S&P methodology...")
        methodology = analyzer.analyze_sp_methodology(sp_document)
        print("✓ S&P methodology analysis completed")
        print(f"Summary length: {len(methodology)} characters")

        print("\nStep 2: Getting D+O rule...")
        dno_rule = analyzer.get_dno_rule(sp_document)
        print("✓ D+O rule extraction completed")
        print(f"Rule length: {len(dno_rule)} characters")

        print("\n✓ All tests passed! The Gemini API fixes are working.")
        return True

    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def main():
    """Run the test"""
    print("Gemini API Fix Test")
    print("=" * 30)

    success = test_sp_methodology_analysis()

    if success:
        print("\n🎉 All tests passed! You can now run the SP1500 analyzer.")
        return 0
    else:
        print("\n❌ Tests failed. Please check the error messages above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
