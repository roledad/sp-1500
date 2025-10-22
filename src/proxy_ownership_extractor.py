"""
Proxy Document Ownership Extractor
Extracts Security Ownership information from proxy documents
"""

import os
import time
import requests
from src.models.genai_client import GenAIClient


class ProxyOwnershipExtractor:
    """Extractor for Security Ownership information from proxy documents"""

    def __init__(self, api_key: str = None):
        """
        Initialize the proxy ownership extractor

        Args:
            api_key: Google GenAI API key
        """
        self.client = GenAIClient(api_key)

    def download_proxy_document(self, pdf_url: str, local_path: str,
                              user_agent: str = "Educational Research Tool (research@example.com)") -> str:
        """
        Download a proxy document from SEC EDGAR

        Args:
            pdf_url: URL to the proxy document
            local_path: Local path to save the document
            user_agent: User agent string for SEC compliance

        Returns:
            Path to the downloaded file
        """
        # SEC-compliant headers
        headers = {
            'User-Agent': user_agent,
            'Accept': 'application/pdf,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

        print(f"Downloading proxy document from: {pdf_url}")

        try:
            # Add a small delay to be respectful to SEC servers
            time.sleep(1)

            response = requests.get(pdf_url, headers=headers, timeout=30)
            print(f"Response status code: {response.status_code}")

            if response.status_code == 404:
                raise FileNotFoundError("Document not found (404). The URL might be incorrect.")
            elif response.status_code == 403:
                print("Access forbidden (403). Trying without special headers...")
                # Try without special headers
                response = requests.get(pdf_url, timeout=30)
                print(f"Simple request status: {response.status_code}")

            response.raise_for_status()

            # Save the PDF file
            with open(local_path, "wb") as f:
                f.write(response.content)

            # Verify the file was downloaded correctly
            if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
                print(f"Successfully downloaded {local_path}")
                print(f"File size: {os.path.getsize(local_path)} bytes")
                return local_path
            else:
                raise RuntimeError(f"File {local_path} was not downloaded correctly")

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Request error: {str(e)}") from e
        except (OSError, IOError) as e:
            raise RuntimeError(f"Download error: {str(e)}") from e

    def extract_ownership_section(self, proxy_document_path: str) -> str:
        """
        Extract the Security Ownership by Certain Beneficial Owners and Management section

        Args:
            proxy_document_path: Path to the proxy document

        Returns:
            Extracted ownership information
        """
        if not os.path.exists(proxy_document_path):
            raise FileNotFoundError(f"Proxy document not found: {proxy_document_path}")

        # First, find the relevant section using a focused request
        print("Step 1: Locating ownership section...")
        proxy_document = self.client.upload_file(proxy_document_path)

        # Use a targeted request to find the ownership section
        location_request = """
        Find and extract ONLY the "Security Ownership by Certain Beneficial Owners and Management" section.
        Look for tables showing share ownership, including:
        - Number of shares owned by officers and directors
        - Percentage of ownership
        - Beneficial ownership information
        Return ONLY this section, nothing else.
        """

        ownership_section = self.client.summarize_document(
            document_file=proxy_document,
            request=location_request
        )

        print("✓ Ownership section located and extracted")

        # If the extracted section is still too long, compress it further
        if len(ownership_section) > 8000:  # Approximate token limit
            print("Step 2: Compressing ownership section...")
            compression_request = """
            Compress the ownership information to focus only on:
            1. Total shares outstanding
            2. Shares owned by officers and directors (with names and share counts)
            3. Percentage ownership for each person
            4. Any beneficial ownership disclosures
            Remove all other text, footnotes, and legal disclaimers.
            """

            compressed_section = self.client.generate_content(
                contents=[compression_request, ownership_section],
                temperature=0.0
            )
            print("✓ Ownership section compressed")
            return compressed_section

        return ownership_section

    def extract_ownership_with_dno_rule(self, proxy_document_path: str) -> str:
        """
        Extract ownership information considering the D+O 5% rule

        Args:
            proxy_document_path: Path to the proxy document
            dno_rule: The 5% rule for D+O holders

        Returns:
            Ownership information with D+O rule consideration
        """
        if not os.path.exists(proxy_document_path):
            raise FileNotFoundError(f"Proxy document not found: {proxy_document_path}")

        # Upload the proxy document
        proxy_document = self.client.upload_file(proxy_document_path)

        # Request for ownership with D+O rule consideration
        request = """
        Based on the float share methodology used by S&P and the information in the Security Ownership by Certain Beneficial Owners and Management Section,
        Calculate the adjusted float shares percentage for the company, considering the 5% rule for D+O holders in the document
        """

        # Get the ownership analysis with D+O rule
        ownership_analysis = self.client.generate_content(
            contents=[request, proxy_document],
            temperature=0.0
        )

        return ownership_analysis

    def extract_ownership_compressed(self, proxy_document_path: str) -> str:
        """
        Extract ownership information with aggressive compression for large documents

        Args:
            proxy_document_path: Path to the proxy document

        Returns:
            Compressed ownership information
        """
        if not os.path.exists(proxy_document_path):
            raise FileNotFoundError(f"Proxy document not found: {proxy_document_path}")

        print("Using compressed extraction for large document...")
        proxy_document = self.client.upload_file(proxy_document_path)

        # Ultra-focused request for large documents
        focused_request = """
        Extract ONLY the essential ownership data in this exact format:

        TOTAL SHARES OUTSTANDING: [number]

        OFFICERS AND DIRECTORS:
        - [Name]: [shares] shares ([percentage]%)
        - [Name]: [shares] shares ([percentage]%)

        BENEFICIAL OWNERS (>5%):
        - [Name]: [shares] shares ([percentage]%)

        Return ONLY this structured data, no other text.
        """

        compressed_ownership = self.client.summarize_document(
            document_file=proxy_document,
            request=focused_request
        )

        print("✓ Compressed ownership data extracted")
        return compressed_ownership


def main():
    """Example usage of the proxy ownership extractor"""
    try:
        extractor = ProxyOwnershipExtractor()

        # Example proxy document URL (replace with actual URL)
        proxy_url = "https://www.sec.gov/Archives/edgar/data/354190/000095017025043725/ajg-ajg_def_14a_2025.pdf"
        local_path = "proxy_document.pdf"

        # Download the proxy document
        downloaded_path = extractor.download_proxy_document(proxy_url, local_path)

        # Extract ownership section
        ownership_info = extractor.extract_ownership_section(downloaded_path)

        print("Security Ownership Information:")
        print("=" * 50)
        print(ownership_info)

    except (FileNotFoundError, ConnectionError, RuntimeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
