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
# Main entry point - analyze constituents
python main.py constituents

# Analyze a specific company
python main.py analyze AAPL

# Batch analyze multiple companies
python main.py batch --limit 5

# Using the float share analyzer directly
python src/float_share_analyzer.py --sp-document doc_assets/sp_float.pdf --proxy-document path/to/proxy.pdf --output results.json

# Using a proxy document URL
python src/float_share_analyzer.py --sp-document doc_assets/sp_float.pdf --proxy-url "https://sec.gov/..." --output results.json
```

### Individual Components

You can also use individual components:

#### 1. Google GenAI Client
```python
from src.models.genai_client import GenAIClient

client = GenAIClient()
document = client.upload_file("document.pdf")
summary = client.summarize_document(document, "Summarize this document")
```

#### 2. S&P Methodology Analyzer
```python
from src.sp_methodology_analyzer import SPMethodologyAnalyzer

analyzer = SPMethodologyAnalyzer()
methodology = analyzer.analyze_sp_methodology("sp_float.pdf")
dno_rule = analyzer.get_dno_rule("sp_float.pdf")
```

#### 3. Proxy Ownership Extractor
```python
from src.proxy_ownership_extractor import ProxyOwnershipExtractor

extractor = ProxyOwnershipExtractor()
# Download proxy document
proxy_path = extractor.download_proxy_document("https://sec.gov/...", "proxy.pdf")
# Extract ownership information
ownership = extractor.extract_ownership_section(proxy_path)
```

#### 4. Float Share Calculator
```python
from src.float_share_calculator import FloatShareCalculator

calculator = FloatShareCalculator()
results = calculator.calculate_float_share_json(ownership, methodology, dno_rule)
```

#### 5. SP1500 Analyzer (Main Component)
```python
from src.sp1500_analyzer import SP1500Analyzer

analyzer = SP1500Analyzer()
# Analyze a specific company
result = analyzer.analyze_company("AAPL")
# Batch analyze multiple companies
results = analyzer.batch_analyze(limit=10)
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

```
edgar/
├── main.py                          # Main entry point
├── requirements.txt                 # Dependencies
├── README.md                        # This file
├── sp1500_constituents.csv          # S&P 1500 companies data
├── sp1500_dei.csv                   # DEI filing data
├── filing_analysis.ipynb            # Jupyter notebook for analysis
│
├── src/                             # Core source code
│   ├── __init__.py
│   ├── sp1500_analyzer.py           # Main analyzer class
│   ├── float_share_analyzer.py      # Float calculation orchestrator
│   ├── float_share_calculator.py    # Float calculation logic
│   ├── proxy_ownership_extractor.py # Proxy document analysis
│   ├── sp_methodology_analyzer.py   # S&P methodology analysis
│   ├── cli_interface.py             # Command-line interface
│   │
│   ├── data/                        # Data layer
│   │   ├── __init__.py
│   │   ├── data_api.py              # EDGAR API integration
│   │   └── data_constitutents.py    # S&P 1500 data fetching
│   │
│   ├── models/                      # AI models and schemas
│   │   ├── __init__.py
│   │   ├── genai_client.py          # Gemini AI client
│   │   └── float_share_schema.py    # Data schemas
│   │
│   ├── analysis/                    # Analysis engines (empty - reserved)
│   │   └── __init__.py
│   │
│   └── utils/                       # Utilities and helpers
│       ├── __init__.py
│       ├── doc_assets_manager.py    # Document management
│       ├── load_env.py              # Environment configuration
│       └── setup_api_key.py         # API key setup
│
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── test_sp1500_analyzer.py      # Main analyzer tests
│   ├── test_doc_assets.py           # Document management tests
│   ├── test_gemini_fix.py           # Gemini API tests
│   ├── test_methodology_caching.py  # Caching tests
│   ├── test_connection.py           # Connection tests
│   └── quick_test.py                # Quick validation
│
├── examples/                        # Usage examples
│   ├── example_usage.py             # Basic usage examples
│   ├── example_sp1500_usage.py      # SP1500 specific examples
│   └── analyze_sp_methodology.py    # Methodology analysis example
│
├── docs/                            # Documentation
│   ├── PROJECT_STRUCTURE.md         # Detailed project structure
│   ├── SP1500_ANALYZER_README.md    # Detailed usage guide
│   ├── IMPLEMENTATION_SUMMARY.md    # Implementation details
│   └── TROUBLESHOOTING.md           # Troubleshooting guide
│
└── config/                          # Configuration files (empty)
```

For detailed project structure, see [PROJECT_STRUCTURE.md](./docs/PROJECT_STRUCTURE.md)

## Requirements

- Python 3.7+
- Google GenAI API key
- Internet connection for document downloads and API calls

## Notes

- The S&P methodology document (`sp_float.pdf`) is stored in `doc_assets/` and summarized in text files for recycled use
- Proxy documents can be provided as local files or URLs and are cached in `doc_assets/`
- Results are saved in JSON format for further processing
- The analysis follows S&P's float share adjustment methodology including the 5% rule for Directors and Officers
- The project supports both individual company analysis and batch processing of S&P 1500 constituents
- All core functionality is organized in the `src/` directory with proper layer separation
