"""
Example usage of the Float Share Analysis system
Demonstrates how to use the complete workflow
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.float_share_analyzer import FloatShareAnalyzer


def main():
    """Example usage of the float share analysis system"""

    # Check if API key is set
    if not os.getenv('GEMINI_API_KEY'):
        print("Error: Please set the GEMINI_API_KEY environment variable")
        print("Example: export GEMINI_API_KEY='your_api_key_here'")
        return

    try:
        # Initialize the analyzer
        analyzer = FloatShareAnalyzer()

        # Example 1: Analyze using local proxy document
        print("Example 1: Using local proxy document")
        print("-" * 40)

        sp_document = "./doc_assets/sp_float.pdf"
        proxy_document = "./doc_assets/ajg_proxy.pdf"

        if os.path.exists(sp_document) and os.path.exists(proxy_document):
            results = analyzer.analyze_company_float_share(
                sp_document_path=sp_document,
                proxy_document_path=proxy_document,
                output_path="example_analysis.json"
            )

            # Display summary
            summary = analyzer.get_analysis_summary(results)
            print(summary)
        else:
            print("Required documents not found:")
            print(f"S&P document: {sp_document} - {'✓' if os.path.exists(sp_document) else '✗'}")
            print(f"Proxy document: {proxy_document} - {'✓' if os.path.exists(proxy_document) else '✗'}")

        # Example 2: Analyze using proxy document URL
        print("\nExample 2: Using proxy document URL")
        print("-" * 40)

        proxy_url = "https://www.sec.gov/Archives/edgar/data/354190/000095017025043725/ajg-ajg_def_14a_2025.pdf"

        if os.path.exists(sp_document):
            print(f"Would analyze using URL: {proxy_url}")
            print("(Uncomment the lines below to run this example)")

            # Uncomment to run this example:
            results = analyzer.analyze_company_from_url(
                sp_document_path=sp_document,
                proxy_url=proxy_url,
                output_path="example_analysis_from_url.json"
            )
            summary = analyzer.get_analysis_summary(results)
            print(summary)
        else:
            print(f"S&P document not found: {sp_document}")

    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure GEMINI_API_KEY is set correctly")
        print("2. Check that the S&P document exists at the specified path")
        print("3. Ensure you have internet connectivity for API calls")


if __name__ == "__main__":
    main()
