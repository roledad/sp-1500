"""
S&P Float Methodology Analyzer
Extracts and summarizes the float share adjustment methodology from S&P documents
"""

import os
import glob
from src.models.genai_client import GenAIClient


class SPMethodologyAnalyzer:
    """Analyzer for S&P float share methodology"""

    def __init__(self, api_key: str = None):
        """
        Initialize the S&P methodology analyzer

        Args:
            api_key: Google GenAI API key
        """
        self.client = GenAIClient(api_key)
        self._cached_document = None
        self._cached_document_path = None

    def _get_cached_document(self, sp_document_path: str):
        """
        Get cached document or upload if not cached

        Args:
            sp_document_path: Path to the S&P float methodology PDF

        Returns:
            Uploaded document object
        """
        if (self._cached_document is None or
            self._cached_document_path != sp_document_path):

            if not os.path.exists(sp_document_path):
                raise FileNotFoundError(f"S&P document not found: {sp_document_path}")

            # Upload the S&P document
            self._cached_document = self.client.upload_file(sp_document_path)
            self._cached_document_path = sp_document_path

        return self._cached_document

    def analyze_sp_methodology(self, sp_document_path: str, save_to_file: bool = True) -> str:
        """
        Analyze and summarize the S&P float methodology from the document

        Args:
            sp_document_path: Path to the S&P float methodology PDF
            save_to_file: Whether to save the analysis to a text file

        Returns:
            Summary of the S&P float methodology
        """
        # Check if methodology analysis already exists
        existing_analysis = self._load_existing_analysis(sp_document_path, "methodology")
        if existing_analysis:
            print("✓ Using existing methodology analysis from doc_assets")
            return existing_analysis

        # Get cached document
        sp_document = self._get_cached_document(sp_document_path)

        # Request for methodology summary
        request = "Summarize the float share adjustment methodology used by S&P"

        # Get the methodology summary
        methodology_summary = self.client.summarize_document(
            document_file=sp_document,
            request=request
        )

        # Save to file if requested
        if save_to_file:
            self._save_analysis_to_file(methodology_summary, sp_document_path, "methodology")

        return methodology_summary

    def get_dno_rule(self, sp_document_path: str, save_to_file: bool = True) -> str:
        """
        Extract the 5% rule for Directors and Officers (D+O) holders

        Args:
            sp_document_path: Path to the S&P float methodology PDF
            save_to_file: Whether to save the analysis to a text file

        Returns:
            Description of the 5% rule for D+O holders
        """
        # Check if D+O rule analysis already exists
        existing_analysis = self._load_existing_analysis(sp_document_path, "dno_rule")
        if existing_analysis:
            print("✓ Using existing D+O rule analysis from doc_assets")
            return existing_analysis

        # Get cached document
        sp_document = self._get_cached_document(sp_document_path)

        # Request for D+O rule
        request = "What is the 5% rule for D+O holders specified in the document"

        # Get the D+O rule
        dno_rule = self.client.generate_content(
            contents=[request, sp_document],
            temperature=0.0
        )

        # Save to file if requested
        if save_to_file:
            self._save_analysis_to_file(dno_rule, sp_document_path, "dno_rule")

        return dno_rule

    def _save_analysis_to_file(self, analysis_text: str, original_doc_path: str, analysis_type: str):
        """
        Save analysis results to a text file in doc_assets directory

        Args:
            analysis_text: The analysis text to save
            original_doc_path: Path to the original document
            analysis_type: Type of analysis (methodology, dno_rule, etc.)
        """
        import os
        from datetime import datetime

        # Ensure doc_assets directory exists
        doc_assets_dir = "doc_assets"
        os.makedirs(doc_assets_dir, exist_ok=True)

        # Create filename based on original document and analysis type
        original_filename = os.path.basename(original_doc_path)
        base_name = os.path.splitext(original_filename)[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        output_filename = f"{base_name}_{analysis_type}_analysis_{timestamp}.txt"
        output_path = os.path.join(doc_assets_dir, output_filename)

        # Save the analysis
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"S&P Float Methodology Analysis\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Source Document: {original_doc_path}\n")
            f.write(f"Analysis Type: {analysis_type}\n")
            f.write("=" * 80 + "\n\n")
            f.write(analysis_text)

        print(f"✓ Analysis saved to: {output_path}")

    def _load_existing_analysis(self, original_doc_path: str, analysis_type: str) -> str:
        """
        Load existing analysis from doc_assets directory if available

        Args:
            original_doc_path: Path to the original document
            analysis_type: Type of analysis (methodology, dno_rule, etc.)

        Returns:
            Existing analysis text or None if not found
        """
        # Ensure doc_assets directory exists
        doc_assets_dir = "doc_assets"
        if not os.path.exists(doc_assets_dir):
            return None

        # Create pattern to match existing analysis files
        original_filename = os.path.basename(original_doc_path)
        base_name = os.path.splitext(original_filename)[0]
        pattern = os.path.join(doc_assets_dir, f"{base_name}_{analysis_type}_analysis_*.txt")

        # Find matching files
        matching_files = glob.glob(pattern)
        if not matching_files:
            return None

        # Get the most recent file
        latest_file = max(matching_files, key=os.path.getctime)

        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract just the analysis content (skip header)
            lines = content.split('\n')
            analysis_start = False
            analysis_lines = []

            for line in lines:
                if line.startswith('=' * 80):
                    analysis_start = True
                    continue
                if analysis_start and line.strip():
                    analysis_lines.append(line)

            if analysis_lines:
                return '\n'.join(analysis_lines)

        except (OSError, IOError):
            pass

        return None


def main():
    """Example usage of the S&P methodology analyzer"""
    try:
        analyzer = SPMethodologyAnalyzer()

        # Analyze the S&P methodology
        sp_doc_path = "/Users/qrui/Projects/genai/prompting/sp_float.pdf"
        methodology = analyzer.analyze_sp_methodology(sp_doc_path)

        print("S&P Float Methodology Summary:")
        print("=" * 50)
        print(methodology)

        # Get the D+O rule
        dno_rule = analyzer.get_dno_rule(sp_doc_path)

        print("\nD+O 5% Rule:")
        print("=" * 50)
        print(dno_rule)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
