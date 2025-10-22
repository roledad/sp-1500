"""
API Key Setup and Test Script
Helps set up and test the Google GenAI API key
"""

import os
import sys
from genai_client import GenAIClient


def setup_api_key():
    """Interactive setup for API key"""
    print("Google GenAI API Key Setup")
    print("=" * 40)

    # Check if API key is already set
    existing_key = os.getenv('GEMINI_API_KEY')
    if existing_key:
        print(f"Found existing API key: {existing_key[:8]}...")
        use_existing = input("Use existing key? (y/n): ").lower().strip()
        if use_existing == 'y':
            return existing_key

    # Get new API key
    print("\nTo get a Google GenAI API key:")
    print("1. Go to https://aistudio.google.com/app/apikey")
    print("2. Create a new API key")
    print("3. Copy the key and paste it below")
    print()

    api_key = input("Enter your Google GenAI API key: ").strip()

    if not api_key:
        print("No API key provided. Exiting.")
        return None

    # Validate the key format
    if not api_key.startswith('AIza'):
        print("Warning: API key doesn't start with 'AIza' - this might be incorrect")
        confirm = input("Continue anyway? (y/n): ").lower().strip()
        if confirm != 'y':
            return None

    return api_key


def test_api_key(api_key):
    """Test the API key by making a simple request"""
    print("\nTesting API key...")

    try:
        # Set the environment variable
        os.environ['GEMINI_API_KEY'] = api_key

        # Initialize client
        client = GenAIClient(api_key)

        # Test with a simple request
        test_prompt = "Hello, this is a test. Please respond with 'API key is working'."

        response = client.generate_content(
            contents=[test_prompt],
            temperature=0.0
        )

        print("✓ API key is working!")
        print(f"Response: {response}")
        return True

    except Exception as e:
        print(f"✗ API key test failed: {e}")
        return False


def save_api_key_to_env_file(api_key):
    """Save API key to .env file for future use"""
    env_file = ".env"

    # Read existing .env file if it exists
    env_content = []
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            env_content = f.readlines()

    # Update or add GEMINI_API_KEY
    updated = False
    for i, line in enumerate(env_content):
        if line.startswith('GEMINI_API_KEY='):
            env_content[i] = f'GEMINI_API_KEY={api_key}\n'
            updated = True
            break

    if not updated:
        env_content.append(f'GEMINI_API_KEY={api_key}\n')

    # Write back to .env file
    with open(env_file, 'w') as f:
        f.writelines(env_content)

    print(f"✓ API key saved to {env_file}")


def main():
    """Main setup function"""
    print("Google GenAI API Key Setup and Test")
    print("=" * 50)

    # Setup API key
    api_key = setup_api_key()
    if not api_key:
        print("Setup cancelled.")
        return

    # Test the API key
    if test_api_key(api_key):
        # Save to .env file
        save_api_key_to_env_file(api_key)

        print("\n" + "=" * 50)
        print("Setup completed successfully!")
        print("\nNext steps:")
        print("1. You can now run the float share analyzer")
        print("2. The API key is saved in .env file")
        print("3. Make sure to keep your API key secure")

        # Show example usage
        print("\nExample usage:")
        print("python float_share_analyzer.py --sp-document doc_assets/sp_float.pdf --proxy-document doc_assets/ajg_proxy.pdf")

    else:
        print("\nSetup failed. Please check your API key and try again.")


if __name__ == "__main__":
    main()
