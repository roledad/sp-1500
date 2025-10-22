"""
Float Share Calculator
Calculates adjusted float share percentage using S&P methodology
"""

import json
from src.models.genai_client import GenAIClient
from src.models.float_share_schema import get_float_share_schema, get_float_share_prompt, get_numerical_calculation_prompt
from typing import Dict, Any, Optional


class FloatShareCalculator:
    """Calculator for float share percentage using S&P methodology"""

    def __init__(self, api_key: str = None):
        """
        Initialize the float share calculator

        Args:
            api_key: Google GenAI API key
        """
        self.client = GenAIClient(api_key)
        self.schema = get_float_share_schema()

    def calculate_float_share_json(self, ownership_summary: str, methodology_summary: str,
                                 dno_rule: str) -> Dict[str, Any]:
        """
        Calculate float share percentage and return as JSON

        Args:
            ownership_summary: Summary of ownership from proxy document
            methodology_summary: S&P methodology summary
            dno_rule: D+O 5% rule description

        Returns:
            Dictionary containing float share analysis results
        """
        prompt = get_float_share_prompt()

        # Generate content with JSON schema
        json_output = self.client.generate_content(
            contents=[prompt, ownership_summary, methodology_summary, dno_rule],
            temperature=0.0,
            response_mime_type="application/json",
            response_schema=self.schema
        )

        # Parse JSON output
        try:
            result = json.loads(json_output)
            return result
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON output: {e}")

    def calculate_float_share_percentage(self, ownership_summary: str, methodology_summary: str,
                                       dno_rule: str) -> str:
        """
        Calculate float share percentage and return as numerical result

        Args:
            ownership_summary: Summary of ownership from proxy document
            methodology_summary: S&P methodology summary
            dno_rule: D+O 5% rule description

        Returns:
            Numerical percentage result
        """
        prompt = get_numerical_calculation_prompt()

        # Generate numerical result
        result = self.client.generate_content(
            contents=[prompt, ownership_summary, methodology_summary, dno_rule],
            temperature=0.0,
            response_mime_type="text/plain"
        )

        return result.strip()

    def calculate_with_proxy_document(self, proxy_document_path: str, methodology_summary: str,
                                   dno_rule: str) -> Dict[str, Any]:
        """
        Calculate float share percentage using a proxy document directly

        Args:
            proxy_document_path: Path to the proxy document
            methodology_summary: S&P methodology summary
            dno_rule: D+O 5% rule description

        Returns:
            Dictionary containing float share analysis results
        """
        # Upload the proxy document
        proxy_document = self.client.upload_file(proxy_document_path)

        prompt = get_float_share_prompt()

        # Generate content with JSON schema
        json_output = self.client.generate_content(
            contents=[prompt, proxy_document, methodology_summary, dno_rule],
            temperature=0.0,
            response_mime_type="application/json",
            response_schema=self.schema
        )

        # Parse JSON output
        try:
            result = json.loads(json_output)
            return result
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON output: {e}")

    def save_results_to_file(self, results: Dict[str, Any], output_path: str) -> None:
        """
        Save calculation results to a JSON file

        Args:
            results: Calculation results dictionary
            output_path: Path to save the results
        """
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to: {output_path}")


def main():
    """Example usage of the float share calculator"""
    try:
        calculator = FloatShareCalculator()

        # Example data (replace with actual data from other components)
        ownership_summary = "Example ownership summary..."
        methodology_summary = "Example methodology summary..."
        dno_rule = "Example D+O rule..."

        # Calculate float share percentage
        results = calculator.calculate_float_share_json(
            ownership_summary, methodology_summary, dno_rule
        )

        print("Float Share Analysis Results:")
        print("=" * 50)
        print(json.dumps(results, indent=2))

        # Save results
        calculator.save_results_to_file(results, "float_share_results.json")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
