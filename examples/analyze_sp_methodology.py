#!/usr/bin/env python3
"""
Analyze S&P Float Methodology Document
Extracts and saves the methodology analysis to text files
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.sp_methodology_analyzer import SPMethodologyAnalyzer


def main():
    """Analyze the S&P float methodology document and save results"""
    print("S&P Float Methodology Analysis")
    print("=" * 40)

    # Check API key
    if not os.getenv('GEMINI_API_KEY'):
        print("Error: GEMINI_API_KEY environment variable is required")
        print("Set it with: export GEMINI_API_KEY='your_api_key_here'")
        return 1

    # Check if S&P document exists
    sp_document = "./doc_assets/sp_float.pdf"
    if not os.path.exists(sp_document):
        print(f"Error: S&P document not found at {sp_document}")
        print("Please ensure the S&P float methodology document is available")
        return 1

    try:
        # Initialize analyzer
        analyzer = SPMethodologyAnalyzer()

        print("Step 1: Analyzing S&P float methodology...")
        methodology = analyzer.analyze_sp_methodology(sp_document, save_to_file=True)
        print("✓ Methodology analysis completed and saved")

        print("\nStep 2: Extracting D+O rule...")
        dno_rule = analyzer.get_dno_rule(sp_document, save_to_file=True)
        print("✓ D+O rule extraction completed and saved")

        print("\nAnalysis Summary:")
        print(f"Methodology length: {len(methodology)} characters")
        print(f"D+O rule length: {len(dno_rule)} characters")

        print("\nFiles saved in doc_assets directory:")
        print("- sp_float_methodology_analysis_[timestamp].txt")
        print("- sp_float_dno_rule_analysis_[timestamp].txt")

        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
