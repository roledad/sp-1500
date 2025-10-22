# Troubleshooting Guide

## API Key Issues

### Error: "API key not valid. Please pass a valid API key."

This error occurs when the Google GenAI API key is missing or invalid.

#### Solution 1: Interactive Setup
```bash
python setup_api_key.py
```

#### Solution 2: Manual Setup
1. Get an API key from: https://aistudio.google.com/app/apikey
2. Set the environment variable:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

#### Solution 3: Create .env file
Create a `.env` file in the project directory:
```
GEMINI_API_KEY=your_api_key_here
```

### Test Your API Key
```bash
python test_connection.py
```

## Common Issues

### 1. Import Errors
If you get import errors, make sure you're running from the correct directory:
```bash
cd /Users/qrui/Projects/genai/sp_float
python float_share_analyzer.py --help
```

### 2. File Not Found Errors
Make sure the required documents exist:
- S&P document: `doc_assets/sp_float.pdf`
- Proxy document: `doc_assets/ajg_proxy.pdf`

### 3. Network Issues
- Check your internet connection
- Verify you can access Google services
- Try running the test script: `python test_connection.py`

### 4. Quota Exceeded
If you get quota errors:
- Check your API usage limits
- Wait for quota to reset
- Consider upgrading your API plan

## Quick Start Guide

1. **Set up API key:**
   ```bash
   python setup_api_key.py
   ```

2. **Test connection:**
   ```bash
   python test_connection.py
   ```

3. **Run analysis:**
   ```bash
   python float_share_analyzer.py --sp-document doc_assets/sp_float.pdf --proxy-document doc_assets/ajg_proxy.pdf
   ```

## File Structure
```
sp_float/
├── doc_assets/
│   ├── sp_float.pdf          # S&P methodology document
│   └── ajg_proxy.pdf         # Example proxy document
├── .env                      # API key (create this)
├── setup_api_key.py         # Interactive API key setup
├── test_connection.py       # Connection test
├── float_share_analyzer.py  # Main analyzer
└── ...                      # Other modules
```

## Getting Help

If you're still having issues:

1. Run the test script: `python test_connection.py`
2. Check the error messages carefully
3. Verify your API key is correct
4. Make sure you have the required documents
5. Check your internet connection
