"""
SP1500 Float Share Analyzer Package
Convenience imports for easy usage
"""

import sys
import os

# Add project root to path automatically when package is imported
_project_root = os.path.dirname(os.path.abspath(__file__))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Version info
__version__ = "1.0.0"
__author__ = "SP1500 Analysis Team"

# Convenience imports (optional)
# from src.sp1500_analyzer import SP1500Analyzer
# from src.float_share_analyzer import FloatShareAnalyzer
# from src.models.genai_client import GenAIClient
