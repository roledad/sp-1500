"""
Simple connection test for Google GenAI API
"""

import os
import sys
from genai_client import GenAIClient


def test_connection():
    """Test the Google GenAI API connection"""
    print("Testing Google GenAI API Connection")
    print("=" * 40)

    # Check for API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY environment variable not set")
        print("\nTo fix this:")
        print("1. Run: python setup_api_key.py")
        print("2. Or set manually: export GEMINI_API_KEY='your_key_here'")
        return False

    print(f"✓ API key found: {api_key[:8]}...")

    try:
        # Initialize client
        print("Initializing GenAI client...")
        client = GenAIClient(api_key)
        print("✓ Client initialized")

        # Test simple generation
        print("Testing API call...")
        response = client.generate_content(
            contents=["Say 'Hello, API is working!' and nothing else."],
            temperature=0.0
        )

        print(f"✓ API call successful!")
        print(f"Response: {response}")
        return True

    except Exception as e:
        print(f"❌ API call failed: {e}")

        # Provide specific error guidance
        if "API key not valid" in str(e):
            print("\n🔧 API Key Issues:")
            print("1. Check if your API key is correct")
            print("2. Make sure you're using a Google GenAI API key (not Google Cloud)")
            print("3. Get a new key from: https://aistudio.google.com/app/apikey")
            print("4. Run: python setup_api_key.py")
        elif "quota" in str(e).lower():
            print("\n🔧 Quota Issues:")
            print("1. Check your API quota limits")
            print("2. Wait for quota to reset")
        else:
            print("\n🔧 General Issues:")
            print("1. Check your internet connection")
            print("2. Verify the API key is correct")
            print("3. Try running: python setup_api_key.py")

        return False


def main():
    """Main test function"""
    success = test_connection()

    if success:
        print("\n🎉 Connection test passed! You can now use the float share analyzer.")
        print("\nExample usage:")
        print("python float_share_analyzer.py --sp-document doc_assets/sp_float.pdf --proxy-document doc_assets/ajg_proxy.pdf")
    else:
        print("\n❌ Connection test failed. Please fix the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
