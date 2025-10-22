#!/usr/bin/env python3
"""
Quick test script to verify the SP1500 analyzer works
"""
import os
import sys

# Add parent directory to path to find setup_path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import setup_path  # This configures the Python path

from src.sp1500_analyzer import SP1500Analyzer

def main():
    """Quick test of the SP1500 analyzer"""
    print("SP1500 Analyzer Quick Test")
    print("=" * 30)

    # Check API key
    if not os.getenv('GEMINI_API_KEY'):
        print("❌ Error: GEMINI_API_KEY environment variable is required")
        print("Set it with: export GEMINI_API_KEY='your_api_key_here'")
        return 1

    # Check S&P document
    sp_document = "./doc_assets/sp_float.pdf"
    if not os.path.exists(sp_document):
        print(f"❌ Error: S&P document not found at {sp_document}")
        print("Please ensure the S&P float methodology document is available")
        return 1

    try:
        print("✓ Environment setup looks good")

        # Test 1: Get constituents
        print("\nTest 1: Getting S&P 1500 constituents...")
        analyzer = SP1500Analyzer()
        constituents = analyzer.get_sp1500_constituents()
        print(f"✓ Retrieved {len(constituents)} constituents")

        # Test 2: Get filing URL
        print("\nTest 2: Getting filing URL for AAPL...")
        filing_info = analyzer.query_ticker_filing_url("AJG")
        if filing_info['status'] == 'success':
            print(f"✓ Found filing URL: {filing_info['url'][:80]}...")
        else:
            print(f"⚠️  Could not get filing URL: {filing_info['message']}")

        # Test 3: Try analysis (this is where the error occurred)
        print("\nTest 3: Testing float share analysis for AAPL...")
        print("This will test the Gemini API fixes...")

        result = analyzer.analyze_float_share_from_ticker(
            ticker="AJG",
            sp_document_path=sp_document,
            output_path="test_analysis.json"
        )

        if result['status'] == 'success':
            print("🎉 SUCCESS! Float share analysis completed")
            print(f"Float share percentage: {result['results'].get('adjusted_float_share_percentage', 'N/A')}%")
            print("The Gemini API fixes are working correctly!")
        else:
            print(f"❌ Analysis failed: {result['message']}")
            return 1

        return 0

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
