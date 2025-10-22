#!/usr/bin/env python3
"""
Command-line interface for SP1500 Float Share Analyzer
Simple CLI for common operations
"""

import sys
import os
import requests
from src.sp1500_analyzer import SP1500Analyzer
from src.utils.doc_assets_manager import DocAssetsManager


def print_usage():
    """Print usage information"""
    print("""
SP1500 Float Share Analyzer - Command Line Interface
====================================================

Usage: python cli_interface.py <command> [options]

Commands:
  constituents                    - Get S&P 1500 constituents list
  filing-url <TICKER>            - Get DEF 14A filing URL for ticker
  analyze <TICKER>               - Analyze float share for ticker
  batch [--limit N]              - Batch analyze multiple tickers
  documents                       - List downloaded proxy documents
  cleanup [--days N]             - Clean up old proxy documents

Examples:
  python cli_interface.py constituents
  python cli_interface.py filing-url AAPL
  python cli_interface.py analyze AAPL
  python cli_interface.py batch --limit 5
  python cli_interface.py documents
  python cli_interface.py cleanup --days 30

Environment Variables:
  GEMINI_API_KEY                 - Required: Google GenAI API key
  SP_DOCUMENT_PATH               - Optional: Path to S&P document (default: ./doc_assets/sp_float.pdf)
""")


def main():
    """Main CLI function"""

    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    # Check API key
    if not os.getenv('GEMINI_API_KEY'):
        print("Error: GEMINI_API_KEY environment variable is required")
        print("Set it with: export GEMINI_API_KEY='your_api_key_here'")
        return

    try:
        analyzer = SP1500Analyzer()

        if command == "constituents":
            print("Getting S&P 1500 constituents...")
            constituents = analyzer.get_sp1500_constituents()
            print(f"Retrieved {len(constituents)} constituents")
            print("\nFirst 10 constituents:")
            print(constituents[['ticker', 'name', 'GICS Sector']].head(10).to_string(index=False))

        elif command == "filing-url":
            if len(sys.argv) < 3:
                print("Error: Ticker required for filing-url command")
                print("Usage: python cli_interface.py filing-url <TICKER>")
                return

            ticker = sys.argv[2].upper()
            print(f"Getting DEF 14A filing URL for {ticker}...")

            result = analyzer.query_ticker_filing_url(ticker)

            if result['status'] == 'success':
                print(f"✓ Found filing for {ticker}")
                print(f"Company: {result['company_name']}")
                print(f"Filing Date: {result['filing_date']}")
                print(f"URL: {result['url']}")
            else:
                print(f"✗ Error: {result['message']}")

        elif command == "analyze":
            if len(sys.argv) < 3:
                print("Error: Ticker required for analyze command")
                print("Usage: python cli_interface.py analyze <TICKER>")
                return

            ticker = sys.argv[2].upper()
            sp_document = os.getenv('SP_DOCUMENT_PATH', './doc_assets/sp_float.pdf')

            if not os.path.exists(sp_document):
                print(f"Error: S&P document not found at {sp_document}")
                print("Please ensure the S&P float methodology document is available")
                return

            print(f"Analyzing float share for {ticker}...")
            print("This may take a few minutes...")

            result = analyzer.analyze_float_share_from_ticker(
                ticker=ticker,
                sp_document_path=sp_document,
                output_path=f"float_analysis_{ticker}.json"
            )

            if result['status'] == 'success':
                print("✓ Analysis completed successfully!")
                print(f"Results saved to: float_analysis_{ticker}.json")

                # Display key results
                results = result['results']
                print(f"\nFloat Share Analysis Summary for {ticker}:")
                print(f"Company: {results.get('company_name', 'N/A')}")
                print(f"Filing Date: {results.get('filing_date', 'N/A')}")
                print(f"Total Shares Outstanding: {results.get('Total Shares Outstanding', 'N/A'):,}")
                print(f"Float Shares: {results.get('Float Shares', 'N/A'):,}")
                print(f"Adjusted Float Share Percentage: {results.get('adjusted_float_share_percentage', 'N/A')}%")
            else:
                print(f"✗ Analysis failed: {result['message']}")

        elif command == "batch":
            sp_document = os.getenv('SP_DOCUMENT_PATH', './doc_assets/sp_float.pdf')

            if not os.path.exists(sp_document):
                print(f"Error: S&P document not found at {sp_document}")
                print("Please ensure the S&P float methodology document is available")
                return

            # Parse limit if provided
            limit = None
            if len(sys.argv) > 3 and sys.argv[2] == "--limit":
                try:
                    limit = int(sys.argv[3])
                except ValueError:
                    print("Error: Invalid limit value")
                    return

            print("Starting batch analysis...")
            if limit:
                print(f"Limited to {limit} companies")
            print("This may take a while...")

            batch_results = analyzer.batch_analyze_constituents(
                sp_document_path=sp_document,
                max_companies=limit
            )

            print("\nBatch Analysis Results:")
            print(f"Total Companies: {batch_results['total_companies']}")
            print(f"Successful: {batch_results['successful_analyses']}")
            print(f"Failed: {batch_results['failed_analyses']}")

            # Show results for successful analyses
            print("\nSuccessful Analyses:")
            for ticker, result in batch_results['companies'].items():
                if result['status'] == 'success':
                    results = result['results']
                    float_pct = results.get('adjusted_float_share_percentage', 'N/A')
                    company_name = results.get('company_name', 'N/A')
                    print(f"  {ticker} ({company_name}): {float_pct}% float share")

            # Show failed analyses
            failed_count = 0
            for ticker, result in batch_results['companies'].items():
                if result['status'] != 'success':
                    failed_count += 1
                    if failed_count <= 5:  # Show first 5 failures
                        print(f"  {ticker}: Failed - {result['message']}")

            if failed_count > 5:
                print(f"  ... and {failed_count - 5} more failures")

        elif command == "documents":
            # List downloaded proxy documents
            print("Listing downloaded proxy documents...")
            manager = DocAssetsManager()
            documents = manager.list_proxy_documents()

            if not documents:
                print("No proxy documents found in doc_assets folder")
            else:
                print(f"\nFound {len(documents)} proxy documents:")
                for doc in documents:
                    print(f"  {doc['filename']} ({doc['size_mb']} MB) - {doc['created']}")

                # Show storage usage
                usage = manager.get_storage_usage()
                print(f"\nStorage Usage: {usage['total_size_mb']} MB ({usage['total_size_gb']} GB)")

        elif command == "cleanup":
            # Clean up old proxy documents
            days_old = 30  # default
            if len(sys.argv) > 3 and sys.argv[2] == "--days":
                try:
                    days_old = int(sys.argv[3])
                except ValueError:
                    print("Error: Invalid days value")
                    return

            print(f"Cleaning up proxy documents older than {days_old} days...")
            manager = DocAssetsManager()
            manager.cleanup_old_documents(days_old)

        else:
            print(f"Error: Unknown command '{command}'")
            print_usage()

    except (ValueError, KeyError, requests.RequestException) as e:
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure GEMINI_API_KEY is set correctly")
        print("2. Check that the S&P document exists")
        print("3. Ensure you have internet connectivity")
        print("4. Verify that the ticker exists in S&P 1500 constituents")


if __name__ == "__main__":
    main()
