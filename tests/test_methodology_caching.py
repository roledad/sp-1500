#!/usr/bin/env python3
"""
Test script to demonstrate methodology analysis caching
Shows how the system reuses existing analysis files
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.sp_methodology_analyzer import SPMethodologyAnalyzer


def test_methodology_caching():
    """Test the methodology analysis caching functionality"""
    print("Testing S&P Methodology Analysis Caching")
    print("=" * 45)

    # Check API key
    if not os.getenv('GEMINI_API_KEY'):
        print("Error: GEMINI_API_KEY environment variable is required")
        return False

    # Check if S&P document exists
    sp_document = "./doc_assets/sp_float.pdf"
    if not os.path.exists(sp_document):
        print(f"Error: S&P document not found at {sp_document}")
        return False

    try:
        analyzer = SPMethodologyAnalyzer()

        print("First run: Analyzing methodology (will create cache files)...")
        methodology1 = analyzer.analyze_sp_methodology(sp_document)
        print(f"✓ Methodology analysis completed (length: {len(methodology1)} chars)")

        print("\nSecond run: Should use cached analysis...")
        methodology2 = analyzer.analyze_sp_methodology(sp_document)
        print(f"✓ Methodology analysis completed (length: {len(methodology2)} chars)")

        print("\nThird run: Testing D+O rule caching...")
        dno_rule1 = analyzer.get_dno_rule(sp_document)
        print(f"✓ D+O rule analysis completed (length: {len(dno_rule1)} chars)")

        print("\nFourth run: Should use cached D+O rule...")
        dno_rule2 = analyzer.get_dno_rule(sp_document)
        print(f"✓ D+O rule analysis completed (length: {len(dno_rule2)} chars)")

        # Verify caching worked
        if methodology1 == methodology2 and dno_rule1 == dno_rule2:
            print("\n🎉 Caching is working correctly!")
            print("Subsequent runs will be much faster and won't use API calls.")
            return True
        else:
            print("\n❌ Caching may not be working correctly")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    """Run the caching test"""
    success = test_methodology_caching()

    if success:
        print("\n✅ All tests passed!")
        print("\nBenefits of caching:")
        print("- Faster analysis (no API calls for repeated runs)")
        print("- Lower API costs")
        print("- Consistent results")
        print("- Files saved in doc_assets/ for future reference")
        return 0
    else:
        print("\n❌ Tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
