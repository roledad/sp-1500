# SP1500 Float Share Analyzer - Project Structure

## 📁 Organized Directory Structure

```
sp_float/
├── main.py                          # Main entry point
├── requirements.txt                  # Dependencies
├── PROJECT_STRUCTURE.md             # This file
│
├── src/                             # Core source code
│   ├── __init__.py
│   ├── sp1500_analyzer.py           # Main analyzer class
│   ├── float_share_analyzer.py     # Float calculation orchestrator
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
│   ├── analysis/                    # Analysis engines
│   │   ├── __init__.py
│   │   ├── sp_methodology_analyzer.py    # S&P methodology analysis
│   │   ├── proxy_ownership_extractor.py  # Proxy document analysis
│   │   └── float_share_calculator.py     # Float calculation logic
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
│   ├── __init__.py
│   ├── example_usage.py             # Basic usage examples
│   ├── example_sp1500_usage.py     # SP1500 specific examples
│   └── analyze_sp_methodology.py   # Methodology analysis example
│
├── docs/                            # Documentation
│   ├── README.md                    # Main documentation
│   ├── SP1500_ANALYZER_README.md   # Detailed usage guide
│   ├── IMPLEMENTATION_SUMMARY.md   # Implementation details
│   └── TROUBLESHOOTING.md          # Troubleshooting guide
│
├── config/                          # Configuration files
│   └── (example JSON files)
│
└── doc_assets/                      # Document storage
    ├── sp_float.pdf                 # S&P methodology document
    ├── proxy_*.pdf                  # Downloaded proxy documents
    └── *_analysis_*.txt            # Cached analysis files
```

## 🎯 **Layer Separation**

### **Data Layer** (`src/data/`)
- **Purpose**: External data integration
- **Files**: EDGAR API, S&P 1500 constituents
- **Responsibilities**: Data fetching, API calls, data validation

### **Models Layer** (`src/models/`)
- **Purpose**: AI model integration and data schemas
- **Files**: Gemini AI client, data schemas
- **Responsibilities**: AI interactions, data structure definitions

### **Analysis Layer** (`src/analysis/`)
- **Purpose**: Core business logic and analysis engines
- **Files**: Methodology analysis, ownership extraction, calculations
- **Responsibilities**: Float share calculations, document processing

### **Utils Layer** (`src/utils/`)
- **Purpose**: Helper functions and utilities
- **Files**: Document management, environment setup
- **Responsibilities**: File operations, configuration management

## 🚀 **Usage**

### **Main Entry Point**
```bash
python main.py constituents
python main.py analyze AAPL
python main.py batch --limit 5
```

### **Direct Module Usage**
```python
from src.sp1500_analyzer import SP1500Analyzer
from src.models.genai_client import GenAIClient
from src.data.data_api import EdgarAPI
```

### **Testing**
```bash
python -m pytest tests/
python tests/quick_test.py
```
