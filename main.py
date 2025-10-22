#!/usr/bin/env python3
"""
SP1500 Float Share Analyzer - Main Entry Point
Organized and clean project structure
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.cli_interface import main as cli_main

def main():
    """Main entry point for the SP1500 Float Share Analyzer"""
    print("SP1500 Float Share Analyzer")
    print("=" * 30)
    print("Organized project structure with clean separation of concerns")
    print()

    # Delegate to CLI interface
    cli_main()

if __name__ == "__main__":
    main()
