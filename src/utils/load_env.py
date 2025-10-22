"""
Environment variable loader
Loads variables from .env file if it exists
"""

import os
from pathlib import Path


def load_env_file():
    """Load environment variables from .env file if it exists"""
    env_file = Path(__file__).parent / ".env"

    if env_file.exists():
        print(f"Loading environment variables from {env_file}")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print("✓ Environment variables loaded")
    else:
        print("No .env file found, using system environment variables")


# Auto-load when this module is imported
load_env_file()
