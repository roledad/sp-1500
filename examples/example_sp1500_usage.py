"""
Example usage of the SP1500 Float Share Analyzer
Demonstrates how to use the comprehensive workflow
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.sp1500_analyzer import SP1500Analyzer


def main():
    """Example usage of the SP1500 analyzer"""

    # Check if API key is set
    if not os.getenv('GEMINI_API_KEY'):
        print("Error: Please set the GEMINI_API_KEY environment variable")
        print("Example: export GEMINI_API_KEY='your_api_key_here'")
        return

    try:
        # Initialize the analyzer
        analyzer = SP1500Analyzer()

        # Example 1: Get S&P 1500 constituents
        print("Example 1: Getting S&P 1500 constituents")
        print("-" * 50)

        constituents = analyzer.get_sp1500_constituents()
        print(f"Retrieved {len(constituents)} constituents")
        print("\nFirst 5 constituents:")
        print(constituents[['ticker', 'name', 'GICS Sector']].head())

        # Example 2: Query filing URL for a specific ticker
        print("\nExample 2: Getting DEF 14A filing URL for a ticker")
        print("-" * 50)

        ticker = "AAPL"  # Apple Inc.
        filing_info = analyzer.query_ticker_filing_url(ticker)
        print(f"Filing info for {ticker}:")
        print(f"Company: {filing_info.get('company_name', 'N/A')}")
        print(f"Filing Date: {filing_info.get('filing_date', 'N/A')}")
        print(f"URL: {filing_info.get('url', 'N/A')}")

        # Example 3: Analyze float share for a specific ticker
        print("\nExample 3: Analyzing float share for a ticker")
        print("-" * 50)

        # Check if S&P document exists
        sp_document = "./doc_assets/sp_float.pdf"
        if not os.path.exists(sp_document):
            print(f"S&P document not found at {sp_document}")
            print("Please ensure the S&P float methodology document is available")
            return

        ticker = "AAPL"
        print(f"Analyzing float share for {ticker}...")

        result = analyzer.analyze_float_share_from_ticker(
            ticker=ticker,
            sp_document_path=sp_document,
            output_path=f"float_analysis_{ticker}.json"
        )

        if result['status'] == 'success':
            print("✓ Analysis completed successfully!")
            print(f"Results saved to: float_analysis_{ticker}.json")

            # Display summary
            results = result['results']
            print(f"\nFloat Share Analysis Summary for {ticker}:")
            print(f"Company: {results.get('company_name', 'N/A')}")
            print(f"Filing Date: {results.get('filing_date', 'N/A')}")
            print(f"Total Shares Outstanding: {results.get('Total Shares Outstanding', 'N/A'):,}")
            print(f"Float Shares: {results.get('Float Shares', 'N/A'):,}")
            print(f"Adjusted Float Share Percentage: {results.get('adjusted_float_share_percentage', 'N/A')}%")
        else:
            print(f"✗ Analysis failed: {result['message']}")

        # Example 4: Batch analysis (limited to 3 companies for demo)
        print("\nExample 4: Batch analysis (limited demo)")
        print("-" * 50)

        # Get a few tickers for demo
        demo_tickers = constituents['ticker'].head(3).tolist()
        print(f"Analyzing {len(demo_tickers)} companies: {demo_tickers}")

        batch_results = analyzer.batch_analyze_constituents(
            sp_document_path=sp_document,
            tickers=demo_tickers
        )

        print("\nBatch Analysis Results:")
        print(f"Successful: {batch_results['successful_analyses']}")
        print(f"Failed: {batch_results['failed_analyses']}")

        # Show results for each company
        for ticker, result in batch_results['companies'].items():
            if result['status'] == 'success':
                results = result['results']
                float_pct = results.get('adjusted_float_share_percentage', 'N/A')
                print(f"  {ticker}: {float_pct}% float share")
            else:
                print(f"  {ticker}: Failed - {result['message']}")

    except (ValueError, KeyError, requests.RequestException) as e:
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure GEMINI_API_KEY is set correctly")
        print("2. Check that the S&P document exists at ./doc_assets/sp_float.pdf")
        print("3. Ensure you have internet connectivity for API calls")
        print("4. Verify that the ticker exists in S&P 1500 constituents")


if __name__ == "__main__":
    main()
