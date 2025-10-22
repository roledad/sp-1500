# Float Share Analysis using S&P Methodology

This package provides tools to analyze public company float shares using S&P's methodology for float share adjustment. It uses Google's GenAI API to process documents and calculate adjusted float share percentages.

## Features

1. **Google GenAI API Integration**: Call Google GenAI API for document analysis
2. **S&P Methodology Analysis**: Summarize float share adjustment methodology from S&P documents
3. **Proxy Document Processing**: Extract Security Ownership information from proxy documents
4. **Float Share Calculation**: Calculate adjusted float share percentage using S&P methodology
5. **Structured JSON Output**: Output results in a defined JSON schema

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Set up your Google GenAI API key:
```bash
export GEMINI_API_KEY="your_api_key_here"
```

## Usage

### Command Line Interface

The main script provides a command-line interface for complete analysis:

```bash
# Using a local proxy document
python float_share_analyzer.py --sp-document prompting/sp_float.pdf --proxy-document path/to/proxy.pdf --output results.json

# Using a proxy document URL
python float_share_analyzer.py --sp-document prompting/sp_float.pdf --proxy-url "https://sec.gov/..." --output results.json
```

### Individual Components

You can also use individual components:

#### 1. Google GenAI Client
```python
from genai_client import GenAIClient

client = GenAIClient()
document = client.upload_file("document.pdf")
summary = client.summarize_document(document, "Summarize this document")
```

#### 2. S&P Methodology Analyzer
```python
from sp_methodology_analyzer import SPMethodologyAnalyzer

analyzer = SPMethodologyAnalyzer()
methodology = analyzer.analyze_sp_methodology("sp_float.pdf")
dno_rule = analyzer.get_dno_rule("sp_float.pdf")
```

#### 3. Proxy Ownership Extractor
```python
from proxy_ownership_extractor import ProxyOwnershipExtractor

extractor = ProxyOwnershipExtractor()
# Download proxy document
proxy_path = extractor.download_proxy_document("https://sec.gov/...", "proxy.pdf")
# Extract ownership information
ownership = extractor.extract_ownership_section(proxy_path)
```

#### 4. Float Share Calculator
```python
from float_share_calculator import FloatShareCalculator

calculator = FloatShareCalculator()
results = calculator.calculate_float_share_json(ownership, methodology, dno_rule)
```

## Output Schema

The analysis outputs a JSON structure with the following fields:

```json
{
  "Total Shares Outstanding": 255734802,
  "Officers, Directors, and related individuals (O+D) Shares": 3364457,
  "Individual person with a 5% or greater stake Shares": 0,
  "Private Equity, Venture Capital, and Special Equity Firms Shares": 0,
  "Asset Managers and Insurance Companies with direct board representation Shares": 0,
  "Publicly Traded Company Shares": 0,
  "Restricted Shares": 0,
  "Employee Plans Shares": 0,
  "Foundations, Government Entities, and Endowments Shares": 0,
  "Sovereign Wealth Funds Shares": 0,
  "(O+D) Shares percentage": 1.3155,
  "(O+D) Shares as Strategic Shares": 0,
  "Total Strategic Shares to Exclude": 0,
  "Float Shares": 255734802,
  "adjusted_float_share_percentage": 100.0
}
```

## File Structure
See [PROJECT STRUCTURE](/sp_float/docs/PROJECT_STRUCTURE.md)

## Requirements

- Python 3.7+
- Google GenAI API key
- Internet connection for document downloads and API calls

## Notes

- The S&P methodology document (`sp_float.pdf`) is summarized in text file for recycled use
- Proxy documents can be provided as local files or URLs
- Results are saved in JSON format for further processing
- The analysis follows S&P's float share adjustment methodology including the 5% rule for Directors and Officers
