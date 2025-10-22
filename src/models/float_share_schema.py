"""
JSON Schema Definition for Float Share Analysis Output
Based on the schema defined in the proxy_summary.ipynb notebook
"""

from typing import Dict, Any


def get_float_share_schema() -> Dict[str, Any]:
    """
    Get the JSON schema for float share analysis output

    Returns:
        JSON schema dictionary
    """
    return {
        "type": "object",
        "properties": {
            "Total Shares Outstanding": {
                "type": "number",
                "description": "number of total shares outstanding"
            },
            "Officers, Directors, and related individuals (O+D) Shares": {
                "type": "number"
            },
            "Individual person with a 5% or greater stake Shares": {
                "type": "number"
            },
            "Private Equity, Venture Capital, and Special Equity Firms Shares": {
                "type": "number"
            },
            "Asset Managers and Insurance Companies with direct board representation Shares": {
                "type": "number"
            },
            "Publicly Traded Company Shares": {
                "type": "number"
            },
            "Restricted Shares": {
                "type": "number"
            },
            "Employee Plans Shares": {
                "type": "number"
            },
            "Foundations, Government Entities, and Endowments Shares": {
                "type": "number"
            },
            "Sovereign Wealth Funds Shares": {
                "type": "number"
            },
            "(O+D) Shares percentage": {
                "type": "number"
            },
            "(O+D) Shares as Strategic Shares": {
                "type": "number"
            },
            "Total Strategic Shares to Exclude": {
                "type": "number"
            },
            "Float Shares": {
                "type": "number"
            },
            "adjusted_float_share_percentage": {
                "type": "number"
            }
        },
        "required": [
            "Total Shares Outstanding",
            "(O+D) Shares percentage",
            "(O+D) Shares as Strategic Shares",
            "Total Strategic Shares to Exclude",
            "Float Shares",
            "adjusted_float_share_percentage"
        ]
    }


def get_float_share_prompt() -> str:
    """
    Get the prompt for float share calculation

    Returns:
        Prompt string for GenAI
    """
    return """
You are an AI that ONLY outputs json format. No explanation, no words.

Task: Calculate adjusted float shares percentage using S&P methodology and proxy data.
Rules: Consider 5% rule for D+O holders. Assume no board representation from asset managers such as Vanguard, BlackRock, etc.

Output the following information in JSON format:
- Total Shares Outstanding
- Officers, Directors, and related individuals (O+D) Shares
- Individual person with a 5% or greater stake Shares
- Private Equity, Venture Capital, and Special Equity Firms Shares
- Asset Managers and Insurance Companies with direct board representation Shares
- Publicly Traded Company Shares
- Restricted Shares
- Employee Plans Shares
- Foundations, Government Entities, and Endowments Shares
- Sovereign Wealth Funds Shares
- (O+D) Shares percentage
- (O+D) Shares as Strategic Shares
- Total Strategic Shares to Exclude
- Float Shares
- adjusted_float_share_percentage
"""


def get_numerical_calculation_prompt() -> str:
    """
    Get the prompt for numerical calculation only

    Returns:
        Prompt string for numerical output
    """
    return """
You are an AI that ONLY outputs numbers. No text, no explanation, no words.

Task: Calculate adjusted float shares percentage using S&P methodology and proxy data.
Rules: Consider 5% rule for D+O holders. Assume no board representation from asset managers such as Vanguard, BlackRock, etc.

Output only the numerical result followed immediately by the percent sign. Do not include any other text, explanation, or conversational filler.
"""


def main():
    """Example usage of the schema"""
    schema = get_float_share_schema()
    print("Float Share Analysis JSON Schema:")
    print("=" * 50)

    import json
    print(json.dumps(schema, indent=2))

    print("\nFloat Share Calculation Prompt:")
    print("=" * 50)
    print(get_float_share_prompt())


if __name__ == "__main__":
    main()
