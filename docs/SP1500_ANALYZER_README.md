# SP1500 Float Share Analyzer

A comprehensive tool for analyzing float share percentages of S&P 1500 constituents using their DEF 14A proxy statements and S&P's float methodology.

## Features

- **S&P 1500 Constituents**: Automatically fetch and manage S&P 1500 index constituents
- **DEF 14A Filing URLs**: Get direct URLs to the latest DEF 14A proxy statements
- **Float Share Analysis**: Calculate float share percentages using Gemini AI
- **Batch Processing**: Analyze multiple companies at once
- **Command Line Interface**: Easy-to-use CLI for common operations

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Google GenAI API key:
```bash
export GEMINI_API_KEY='your_api_key_here'
```

3. Ensure you have the S&P float methodology document at `./doc_assets/sp_float.pdf`

## Usage

### Command Line Interface (Recommended)

The easiest way to use the analyzer is through the CLI:

```bash
# Get S&P 1500 constituents
python cli_interface.py constituents

# Get DEF 14A filing URL for a specific ticker
python cli_interface.py filing-url AAPL

# Analyze float share for a specific ticker
python cli_interface.py analyze AAPL

# Batch analyze multiple tickers (limited to 5 for demo)
python cli_interface.py batch --limit 5

# List downloaded proxy documents
python cli_interface.py documents

# Clean up old proxy documents (older than 30 days)
python cli_interface.py cleanup --days 30
```

### Python API

For more advanced usage, you can use the Python API directly:

```python
from sp1500_analyzer import SP1500Analyzer

# Initialize analyzer
analyzer = SP1500Analyzer()

# Get S&P 1500 constituents
constituents = analyzer.get_sp1500_constituents()
print(f"Retrieved {len(constituents)} constituents")

# Get filing URL for a ticker
filing_info = analyzer.query_ticker_filing_url("AAPL")
print(f"Filing URL: {filing_info['url']}")

# Analyze float share
result = analyzer.analyze_float_share_from_ticker(
    ticker="AAPL",
    sp_document_path="./doc_assets/sp_float.pdf"
)

if result['status'] == 'success':
    print(f"Float share: {result['results']['adjusted_float_share_percentage']}%")
```

### Advanced Usage

#### Batch Analysis

```python
# Analyze multiple companies
batch_results = analyzer.batch_analyze_constituents(
    sp_document_path="./doc_assets/sp_float.pdf",
    tickers=["AAPL", "MSFT", "GOOGL"],  # Specific tickers
    max_companies=10  # Or limit to first 10 companies
)
```

#### Custom Output Paths

```python
# Save results to custom location
result = analyzer.analyze_float_share_from_ticker(
    ticker="AAPL",
    sp_document_path="./doc_assets/sp_float.pdf",
    output_path="./results/apple_analysis.json"
)
```

## File Structure

```
sp_float/
├── sp1500_analyzer.py          # Main analyzer class
├── cli_interface.py            # Command-line interface
├── example_sp1500_usage.py     # Usage examples
├── doc_assets_manager.py       # Document assets management
├── data_constitutents.py       # S&P 1500 data fetching
├── data_api.py                 # EDGAR API integration
├── float_share_analyzer.py     # Float calculation logic
├── doc_assets/
│   ├── sp_float.pdf           # S&P float methodology document
│   └── proxy_*.pdf            # Downloaded proxy documents
└── requirements.txt           # Dependencies
```

## Output Format

### Filing URL Query
```json
{
  "ticker": "AAPL",
  "company_name": "Apple Inc.",
  "cik": "0000320193",
  "filing_date": "2024-01-15",
  "accession_number": "0000320193-24-000006",
  "form_type": "DEF 14A",
  "url": "https://www.sec.gov/Archives/edgar/data/320193/000032019324000006/aapl-20240115_def14a.pdf",
  "status": "success"
}
```

### Float Share Analysis
```json
{
  "ticker": "AAPL",
  "status": "success",
  "results": {
    "company_name": "Apple Inc.",
    "filing_date": "2024-01-15",
    "Total Shares Outstanding": 15728700000,
    "Float Shares": 15234500000,
    "adjusted_float_share_percentage": 96.86,
    "Officers, Directors, and related individuals (O+D) Shares": 494200000,
    "(O+D) Shares percentage": 3.14,
    "Total Strategic Shares to Exclude": 494200000
  }
}
```

## Error Handling

The analyzer includes comprehensive error handling:

- **Missing API Key**: Clear error message with setup instructions
- **Missing S&P Document**: Validation before analysis
- **Invalid Ticker**: Checks against S&P 1500 constituents
- **Network Issues**: Retry mechanisms for API calls
- **Missing Filings**: Graceful handling of companies without DEF 14A filings

## Troubleshooting

### Common Issues

1. **"GEMINI_API_KEY environment variable is required"**
   - Set your API key: `export GEMINI_API_KEY='your_key_here'`

2. **"S&P document not found"**
   - Ensure `./doc_assets/sp_float.pdf` exists
   - Or set custom path: `export SP_DOCUMENT_PATH='/path/to/sp_float.pdf'`

3. **"Ticker not found in S&P 1500 constituents"**
   - Verify the ticker is in the S&P 1500 index
   - Use `python cli_interface.py constituents` to see available tickers

4. **"No DEF 14A filings found"**
   - Some companies may not have recent DEF 14A filings
   - Try a different ticker or check the company's SEC filings manually

## Document Management

The system automatically downloads proxy documents to the `doc_assets` folder:

### Document Storage
- **Location**: `./doc_assets/` folder
- **Naming**: `proxy_YYYYMMDD_HHMMSS_original_filename.pdf`
- **Persistence**: Documents are kept for future reference (not deleted after analysis)

### Document Management Commands
```bash
# List all downloaded proxy documents
python cli_interface.py documents

# Clean up old documents (older than 30 days)
python cli_interface.py cleanup --days 30

# Clean up documents older than 7 days
python cli_interface.py cleanup --days 7
```

### Document Information
Each downloaded document includes:
- Original filename and timestamp
- File size and creation date
- Storage usage statistics

### Performance Tips

- **Batch Analysis**: Use batch mode for multiple companies
- **Rate Limiting**: The analyzer includes built-in delays to respect API limits
- **Caching**: Constituents data is cached to avoid repeated API calls
- **Document Storage**: Automatic organization of downloaded proxy documents

## Dependencies

- `google-genai>=0.8.0` - Gemini AI integration
- `requests>=2.25.0` - HTTP requests
- `pandas>=1.3.0` - Data manipulation
- `urllib3` - URL handling
- `io` - String I/O operations

## License

This project is part of the genai workspace and follows the same licensing terms.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the example usage in `example_sp1500_usage.py`
3. Ensure all dependencies are installed correctly
4. Verify your API key and internet connectivity
