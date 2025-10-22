#!/usr/bin/env python3
"""
Test script to verify doc_assets folder functionality
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.doc_assets_manager import DocAssetsManager


def test_doc_assets_manager():
    """Test the document assets manager"""
    print("Testing Document Assets Manager")
    print("=" * 30)

    try:
        # Initialize manager
        manager = DocAssetsManager()
        print("✓ Document assets manager initialized")

        # Test directory creation
        if os.path.exists("doc_assets"):
            print("✓ doc_assets directory exists")
        else:
            print("✗ doc_assets directory not found")
            return False

        # List documents
        documents = manager.list_proxy_documents()
        print(f"✓ Found {len(documents)} proxy documents")

        # Show storage usage
        usage = manager.get_storage_usage()
        print(f"✓ Storage usage: {usage['total_size_mb']} MB")

        # Test document info (if any documents exist)
        if documents:
            first_doc = documents[0]
            info = manager.get_document_info(first_doc['filename'])
            if 'error' not in info:
                print(f"✓ Document info retrieved for {first_doc['filename']}")
            else:
                print(f"✗ Error getting document info: {info['error']}")

        print("\n✓ All tests passed!")
        return True

    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def main():
    """Run the test"""
    success = test_doc_assets_manager()

    if success:
        print("\n🎉 Document assets functionality is working!")
        print("\nYou can now use:")
        print("  python cli_interface.py documents  # List downloaded documents")
        print("  python cli_interface.py cleanup  # Clean up old documents")
        return 0
    else:
        print("\n❌ Tests failed. Please check the error messages above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
