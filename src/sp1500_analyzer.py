"""
SP1500 Float Share Analyzer
Comprehensive script to analyze S&P 1500 constituents and their float share percentages
"""

import os
import json
import argparse
import pandas as pd
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime
# Import existing modules
from src.data.data_constitutents import consolidate_data
from src.data.data_api import EdgarAPI
from src.float_share_analyzer import FloatShareAnalyzer


class SP1500Analyzer:
    """Main analyzer for S&P 1500 constituents and their float share analysis"""

    def __init__(self, api_key: str = None):
        """
        Initialize the SP1500 analyzer

        Args:
            api_key: Google GenAI API key
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        self.float_analyzer = FloatShareAnalyzer(self.api_key)
        self.constituents_data = None
        self.filings_data = {}

    def get_sp1500_constituents(self, refresh: bool = False) -> pd.DataFrame:
        """
        Get S&P 1500 constituents data

        Args:
            refresh: Whether to refresh the data from sources

        Returns:
            DataFrame with S&P 1500 constituents
        """
        if self.constituents_data is None or refresh:
            print("Fetching S&P 1500 constituents data...")
            self.constituents_data = consolidate_data()
            print(f"✓ Retrieved {len(self.constituents_data)} constituents")

        return self.constituents_data

    def get_company_filings(self, ticker: str, filing_type: str = "DEF 14A") -> pd.DataFrame:
        """
        Get company filings for a specific ticker

        Args:
            ticker: Company ticker symbol
            filing_type: Type of filing to filter (default: DEF 14A)

        Returns:
            DataFrame with company filings
        """
        # Get CIK from constituents data
        if self.constituents_data is None:
            self.get_sp1500_constituents()

        ticker_data = self.constituents_data[self.constituents_data['ticker'] == ticker]
        if ticker_data.empty:
            raise ValueError(f"Ticker {ticker} not found in S&P 1500 constituents")

        cik = ticker_data['cik'].iloc[0]
        company_name = ticker_data['name'].iloc[0]

        print(f"Getting filings for {company_name} ({ticker}) - CIK: {cik}")

        # Get company submissions
        edgar_api = EdgarAPI(retrieval="submission", cik=cik)
        filings_df = edgar_api.get_company_filings(filing_type=[filing_type])

        if filings_df.empty:
            print(f"No {filing_type} filings found for {ticker}")
            return pd.DataFrame()

        # Sort by filing date and get the latest
        filings_df['filingDate'] = pd.to_datetime(filings_df['filingDate'])
        filings_df = filings_df.sort_values('filingDate', ascending=False)

        # Add company info
        filings_df['ticker'] = ticker
        filings_df['company_name'] = company_name
        filings_df['cik'] = cik

        return filings_df

    def get_latest_def14a_url(self, ticker: str) -> Optional[str]:
        """
        Get the URL for the latest DEF 14A filing for a ticker

        Args:
            ticker: Company ticker symbol

        Returns:
            URL to the latest DEF 14A filing PDF, or None if not found
        """
        filings_df = self.get_company_filings(ticker, "DEF 14A")

        if filings_df.empty:
            return None

        # Get the latest filing
        latest_filing = filings_df.iloc[0]
        # Construct the PDF URL
        # Format: https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number}/{filename}
        accession_number = latest_filing['accessionNumber'].replace('-', '')
        filename = latest_filing['primaryDocument']

        # Extract the base filename and add .pdf extension if needed
        # if not filename.endswith('.pdf'):
        #     filename = filename.replace('.txt', '.pdf')

        pdf_url = f"https://www.sec.gov/Archives/edgar/data/{latest_filing['cik']}/{accession_number}/{filename}"

        return pdf_url

    def query_ticker_filing_url(self, ticker: str) -> Dict[str, Any]:
        """
        Query filing URL for a specific ticker

        Args:
            ticker: Company ticker symbol

        Returns:
            Dictionary with filing information and URL
        """
        try:
            filings_df = self.get_company_filings(ticker, "DEF 14A")

            if filings_df.empty:
                return {
                    'ticker': ticker,
                    'status': 'error',
                    'message': f'No DEF 14A filings found for {ticker}',
                    'url': None
                }

            latest_filing = filings_df.iloc[0]
            pdf_url = self.get_latest_def14a_url(ticker)

            return {
                'ticker': ticker,
                'company_name': latest_filing['company_name'],
                'cik': latest_filing['cik'],
                'filing_date': latest_filing['filingDate'].strftime('%Y-%m-%d'),
                'accession_number': latest_filing['accessionNumber'],
                'form_type': latest_filing['form'],
                'url': pdf_url,
                'status': 'success'
            }

        except (ValueError, KeyError, requests.RequestException) as e:
            return {
                'ticker': ticker,
                'status': 'error',
                'message': str(e),
                'url': None
            }

    def analyze_float_share_from_ticker(self, ticker: str, sp_document_path: str,
                                      output_path: str = None) -> Dict[str, Any]:
        """
        Analyze float share percentage for a specific ticker

        Args:
            ticker: Company ticker symbol
            sp_document_path: Path to S&P float methodology document
            output_path: Path to save results (optional)

        Returns:
            Dictionary with analysis results
        """
        # Get filing URL
        filing_info = self.query_ticker_filing_url(ticker)

        if filing_info['status'] != 'success':
            return {
                'ticker': ticker,
                'status': 'error',
                'message': f"Could not get filing URL: {filing_info['message']}",
                'results': None
            }

        pdf_url = filing_info['url']
        print(f"Analyzing float share for {ticker} using URL: {pdf_url}")

        # Use the existing float analyzer
        try:
            results = self.float_analyzer.analyze_company_from_url(
                sp_document_path=sp_document_path,
                proxy_url=pdf_url,
                output_path=output_path or f"float_analysis_{ticker}.json"
            )

            # Add ticker information to results
            results['ticker'] = ticker
            results['company_name'] = filing_info['company_name']
            results['filing_date'] = filing_info['filing_date']
            results['filing_url'] = pdf_url

            return {
                'ticker': ticker,
                'status': 'success',
                'results': results
            }

        except (ValueError, KeyError, requests.RequestException) as e:
            return {
                'ticker': ticker,
                'status': 'error',
                'message': str(e),
                'results': None
            }

    def batch_analyze_constituents(self, sp_document_path: str,
                                 tickers: List[str] = None,
                                 max_companies: int = None) -> Dict[str, Any]:
        """
        Batch analyze multiple constituents

        Args:
            sp_document_path: Path to S&P float methodology document
            tickers: List of specific tickers to analyze (optional)
            max_companies: Maximum number of companies to analyze (optional)

        Returns:
            Dictionary with batch analysis results
        """
        # Get constituents
        constituents = self.get_sp1500_constituents()

        if tickers:
            # Filter to specific tickers
            constituents = constituents[constituents['ticker'].isin(tickers)]
        elif max_companies:
            # Limit to first N companies
            constituents = constituents.head(max_companies)

        results = {
            'analysis_date': datetime.now().isoformat(),
            'total_companies': len(constituents),
            'successful_analyses': 0,
            'failed_analyses': 0,
            'companies': {}
        }

        print(f"Starting batch analysis for {len(constituents)} companies...")

        for idx, (_, company) in enumerate(constituents.iterrows(), 1):
            ticker = company['ticker']
            company_name = company['name']

            print(f"\n[{idx}/{len(constituents)}] Analyzing {company_name} ({ticker})")

            try:
                analysis_result = self.analyze_float_share_from_ticker(
                    ticker, sp_document_path
                )

                results['companies'][ticker] = analysis_result

                if analysis_result['status'] == 'success':
                    results['successful_analyses'] += 1
                    print(f"✓ Successfully analyzed {ticker}")
                else:
                    results['failed_analyses'] += 1
                    print(f"✗ Failed to analyze {ticker}: {analysis_result['message']}")

            except (ValueError, KeyError, requests.RequestException) as e:
                results['failed_analyses'] += 1
                results['companies'][ticker] = {
                    'ticker': ticker,
                    'status': 'error',
                    'message': str(e),
                    'results': None
                }
                print(f"✗ Error analyzing {ticker}: {e}")

        # Save batch results
        batch_output_path = f"batch_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(batch_output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)

        print("\nBatch analysis completed!")
        print(f"Successful: {results['successful_analyses']}")
        print(f"Failed: {results['failed_analyses']}")
        print(f"Results saved to: {batch_output_path}")

        return results


def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description="S&P 1500 Float Share Analyzer")
    parser.add_argument("--action", choices=['constituents', 'filing-url', 'analyze', 'batch'],
                       required=True, help="Action to perform")
    parser.add_argument("--ticker", help="Company ticker symbol")
    parser.add_argument("--sp-document", help="Path to S&P float methodology document")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--max-companies", type=int, help="Maximum companies for batch analysis")
    parser.add_argument("--api-key", help="Google GenAI API key (or set GEMINI_API_KEY env var)")

    args = parser.parse_args()

    try:
        # Initialize analyzer
        analyzer = SP1500Analyzer(args.api_key)

        if args.action == 'constituents':
            # Get S&P 1500 constituents
            constituents = analyzer.get_sp1500_constituents()
            print(f"Retrieved {len(constituents)} S&P 1500 constituents")
            if args.output:
                constituents.to_csv(args.output, index=False)
                print(f"Saved to {args.output}")
            else:
                print(constituents.head())

        elif args.action == 'filing-url':
            # Get filing URL for ticker
            if not args.ticker:
                print("Error: --ticker is required for filing-url action")
                return

            result = analyzer.query_ticker_filing_url(args.ticker)
            print(json.dumps(result, indent=2))

        elif args.action == 'analyze':
            # Analyze single ticker
            if not args.ticker or not args.sp_document:
                print("Error: --ticker and --sp-document are required for analyze action")
                return

            result = analyzer.analyze_float_share_from_ticker(
                args.ticker, args.sp_document, args.output
            )
            print(json.dumps(result, indent=2))

        elif args.action == 'batch':
            # Batch analyze multiple tickers
            if not args.sp_document:
                print("Error: --sp-document is required for batch action")
                return

            result = analyzer.batch_analyze_constituents(
                args.sp_document,
                max_companies=args.max_companies
            )
            print(f"Batch analysis completed: {result['successful_analyses']} successful, {result['failed_analyses']} failed")

    except (ValueError, KeyError, requests.RequestException) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
