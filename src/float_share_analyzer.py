"""
Main Float Share Analyzer
Orchestrates the complete float share analysis workflow using S&P methodology
"""

import os
import argparse
import re
from urllib.parse import urlparse
from datetime import datetime
from typing import Dict, Any

from src.sp_methodology_analyzer import SPMethodologyAnalyzer
from src.proxy_ownership_extractor import ProxyOwnershipExtractor
from src.float_share_calculator import FloatShareCalculator


class FloatShareAnalyzer:
    """Main analyzer that orchestrates the complete float share analysis workflow"""

    def __init__(self, api_key: str = None):
        """
        Initialize the float share analyzer

        Args:
            api_key: Google GenAI API key
        """
        self.sp_analyzer = SPMethodologyAnalyzer(api_key)
        self.proxy_extractor = ProxyOwnershipExtractor(api_key)
        self.calculator = FloatShareCalculator(api_key)

    def analyze_company_float_share(self, sp_document_path: str, proxy_document_path: str,
                                  output_path: str = "float_share_analysis.json") -> Dict[str, Any]:
        """
        Perform complete float share analysis for a company

        Args:
            sp_document_path: Path to S&P float methodology document
            proxy_document_path: Path to company proxy document
            output_path: Path to save the analysis results

        Returns:
            Dictionary containing the complete analysis results
        """
        print("Starting float share analysis...")
        print("=" * 50)

        # Step 1: Analyze S&P methodology
        print("Step 1: Analyzing S&P float methodology...")
        methodology_summary = self.sp_analyzer.analyze_sp_methodology(sp_document_path)
        dno_rule = self.sp_analyzer.get_dno_rule(sp_document_path)
        print("✓ S&P methodology analyzed")

        # Step 2: Extract ownership information from proxy
        print("Step 2: Extracting ownership information from proxy document...")
        try:
            ownership_summary = self.proxy_extractor.extract_ownership_section(proxy_document_path)
            print("✓ Ownership information extracted")
        except Exception as e:
            if "token limit" in str(e).lower() or "too long" in str(e).lower():
                print("Document too large, using compressed extraction...")
                ownership_summary = self.proxy_extractor.extract_ownership_compressed(proxy_document_path)
                print("✓ Compressed ownership information extracted")
            else:
                raise e

        # Step 3: Calculate float share percentage
        print("Step 3: Calculating float share percentage...")
        results = self.calculator.calculate_float_share_json(
            ownership_summary, methodology_summary, dno_rule
        )
        print("✓ Float share percentage calculated")

        # Step 4: Save results
        print("Step 4: Saving results...")
        self.calculator.save_results_to_file(results, output_path)
        print(f"✓ Results saved to {output_path}")

        print("\nAnalysis completed successfully!")
        print("=" * 50)

        return results

    def analyze_company_from_url(self, sp_document_path: str, proxy_url: str,
                               output_path: str = "float_share_analysis.json") -> Dict[str, Any]:
        """
        Perform complete float share analysis for a company from proxy URL

        Args:
            sp_document_path: Path to S&P float methodology document
            proxy_url: URL to company proxy document
            output_path: Path to save the analysis results

        Returns:
            Dictionary containing the complete analysis results
        """
        print("Starting float share analysis from URL...")
        print("=" * 50)

        # Download proxy document to doc_assets folder
        print("Downloading proxy document...")

        # Ensure doc_assets folder exists
        doc_assets_dir = "doc_assets"
        os.makedirs(doc_assets_dir, exist_ok=True)

        # Create a descriptive filename from the URL
        parsed_url = urlparse(proxy_url)
        filename = os.path.basename(parsed_url.path)
        # if not filename or not filename.endswith('.pdf'):
        #     filename = "proxy_document.pdf"

        # Add timestamp to avoid conflicts
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = re.sub(r'[^\w\-_\.]', '_', filename)
        proxy_filename = f"proxy_{timestamp}_{safe_filename}"

        proxy_document_path = os.path.join(doc_assets_dir, proxy_filename)

        proxy_document_path = self.proxy_extractor.download_proxy_document(
            proxy_url, proxy_document_path
        )
        print("✓ Proxy document downloaded")

        # Perform analysis
        results = self.analyze_company_float_share(
            sp_document_path, proxy_document_path, output_path
        )

        # Keep the proxy document in doc_assets folder for future reference
        print(f"✓ Proxy document saved to: {proxy_document_path}")

        return results

    def get_analysis_summary(self, results: Dict[str, Any]) -> str:
        """
        Get a summary of the analysis results

        Args:
            results: Analysis results dictionary

        Returns:
            Summary string
        """
        summary = f"""
        Float Share Analysis Summary:
        ============================
        Total Shares Outstanding: {results.get('Total Shares Outstanding', 'N/A'):,}
        Float Shares: {results.get('Float Shares', 'N/A'):,}
        Adjusted Float Share Percentage: {results.get('adjusted_float_share_percentage', 'N/A')}%

        Key Ownership Details:
        - Officers & Directors (O+D) Shares: {results.get('Officers, Directors, and related individuals (O+D) Shares', 'N/A'):,}
        - O+D Percentage: {results.get('(O+D) Shares percentage', 'N/A')}%
        - Strategic Shares to Exclude: {results.get('Total Strategic Shares to Exclude', 'N/A'):,}
        """
        return summary.strip()


def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description="Float Share Analysis using S&P Methodology")
    parser.add_argument("--sp-document", required=True, help="Path to S&P float methodology document")
    parser.add_argument("--proxy-document", help="Path to proxy document")
    parser.add_argument("--proxy-url", help="URL to proxy document")
    parser.add_argument("--output", default="float_share_analysis.json", help="Output file path")
    parser.add_argument("--api-key", help="Google GenAI API key (or set GEMINI_API_KEY env var)")

    args = parser.parse_args()

    try:
        # Initialize analyzer
        analyzer = FloatShareAnalyzer(args.api_key)

        # Perform analysis
        if args.proxy_document:
            results = analyzer.analyze_company_float_share(
                args.sp_document, args.proxy_document, args.output
            )
        elif args.proxy_url:
            results = analyzer.analyze_company_from_url(
                args.sp_document, args.proxy_url, args.output
            )
        else:
            print("Error: Must provide either --proxy-document or --proxy-url")
            return

        # Display summary
        summary = analyzer.get_analysis_summary(results)
        print(summary)

    except (ValueError, FileNotFoundError, OSError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
