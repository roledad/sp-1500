#!/usr/bin/env python3
"""
Test script for SP1500 Float Share Analyzer
Tests basic functionality without requiring API calls
"""

import os
import sys
from src.sp1500_analyzer import SP1500Analyzer


def test_constituents():
    """Test getting S&P 1500 constituents"""
    print("Testing S&P 1500 constituents retrieval...")

    try:
        analyzer = SP1500Analyzer()
        constituents = analyzer.get_sp1500_constituents()

        print(f"✓ Successfully retrieved {len(constituents)} constituents")
        print(f"Sample constituents:")
        print(constituents[['ticker', 'name', 'GICS Sector']].head(3).to_string(index=False))

        return True

    except Exception as e:
        print(f"✗ Failed to get constituents: {e}")
        return False


def test_filing_url():
    """Test getting filing URL for a known ticker"""
    print("\nTesting filing URL retrieval...")

    try:
        analyzer = SP1500Analyzer()

        # Test with a well-known ticker
        ticker = "AAPL"
        result = analyzer.query_ticker_filing_url(ticker)

        if result['status'] == 'success':
            print(f"✓ Successfully got filing URL for {ticker}")
            print(f"  Company: {result['company_name']}")
            print(f"  Filing Date: {result['filing_date']}")
            print(f"  URL: {result['url'][:80]}...")
            return True
        else:
            print(f"✗ Failed to get filing URL: {result['message']}")
            return False

    except Exception as e:
        print(f"✗ Error testing filing URL: {e}")
        return False


def test_analyzer_initialization():
    """Test analyzer initialization"""
    print("\nTesting analyzer initialization...")

    try:
        # Test without API key (should fail gracefully)
        if 'GEMINI_API_KEY' in os.environ:
            del os.environ['GEMINI_API_KEY']

        try:
            analyzer = SP1500Analyzer()
            print("✗ Should have failed without API key")
            return False
        except ValueError as e:
            if "GEMINI_API_KEY" in str(e):
                print("✓ Correctly failed without API key")
            else:
                print(f"✗ Unexpected error: {e}")
                return False

        # Test with dummy API key
        os.environ['GEMINI_API_KEY'] = 'test_key'
        analyzer = SP1500Analyzer()
        print("✓ Successfully initialized with API key")
        return True

    except Exception as e:
        print(f"✗ Error testing initialization: {e}")
        return False


def main():
    """Run all tests"""
    print("SP1500 Float Share Analyzer - Test Suite")
    print("=" * 50)

    tests = [
        test_analyzer_initialization,
        test_constituents,
        test_filing_url,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")

    print(f"\nTest Results: {passed}/{total} tests passed")

    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
