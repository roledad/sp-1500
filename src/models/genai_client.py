"""
Google GenAI API Client for Float Share Analysis
Based on the proxy_summary.ipynb notebook implementation
"""

import os
import time
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from typing import Optional, Dict, Any


class GenAIClient:
    """Client for Google GenAI API operations"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the GenAI client

        Args:
            api_key: Google GenAI API key. If None, will try to get from GEMINI_API_KEY env var
        """
        if api_key is None:
            api_key = os.getenv('GEMINI_API_KEY')

        if api_key is None:
            raise ValueError("API key not provided and GEMINI_API_KEY environment variable not set")

        self.client = genai.Client()

    def upload_file(self, file_path: str, max_retries: int = 3) -> Any:
        """
        Upload a file to the GenAI API with retry logic

        Args:
            file_path: Path to the file to upload
            max_retries: Maximum number of retry attempts

        Returns:
            Uploaded file object
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        for attempt in range(max_retries):
            try:
                document_file = self.client.files.upload(file=file_path)
                print(f"File successfully uploaded: {file_path}")
                return document_file
            except ClientError as e:
                if "not in an ACTIVE state" in str(e) and attempt < max_retries - 1:
                    print(f"File not ready, waiting 5 seconds before retry {attempt + 1}/{max_retries}...")
                    time.sleep(5)
                    continue
                else:
                    raise e
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Upload failed, retrying in 5 seconds... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(5)
                    continue
                else:
                    raise e

    def summarize_document(self, document_file: Any, request: str, model: str = "gemini-2.5-flash", max_retries: int = 3) -> str:
        """
        Summarize a document using GenAI with retry logic

        Args:
            document_file: Uploaded file object
            request: Summary request/prompt
            model: Model to use for generation
            max_retries: Maximum number of retry attempts

        Returns:
            Summary text
        """
        for attempt in range(max_retries):
            try:
                config = types.GenerateContentConfig(temperature=0.0)
                response = self.client.models.generate_content(
                    model=model,
                    config=config,
                    contents=[request, document_file],
                )
                return response.text
            except ClientError as e:
                if "not in an ACTIVE state" in str(e) and attempt < max_retries - 1:
                    print(f"File not ready for processing, waiting 10 seconds before retry {attempt + 1}/{max_retries}...")
                    time.sleep(10)
                    continue
                else:
                    raise e
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Processing failed, retrying in 5 seconds... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(5)
                    continue
                else:
                    raise e

    def generate_content(self, contents: list, model: str = "gemini-2.5-flash",
                        temperature: float = 0.0, response_mime_type: str = "text/plain",
                        response_schema: Optional[Dict] = None, max_retries: int = 3) -> str:
        """
        Generate content using GenAI with retry logic

        Args:
            contents: List of content to process
            model: Model to use
            temperature: Temperature for generation
            response_mime_type: MIME type for response
            response_schema: JSON schema for structured output
            max_retries: Maximum number of retry attempts

        Returns:
            Generated content
        """
        for attempt in range(max_retries):
            try:
                config_params = {
                    "temperature": temperature,
                    "response_mime_type": response_mime_type
                }

                if response_schema:
                    config_params["response_schema"] = response_schema

                config = types.GenerateContentConfig(**config_params)

                response = self.client.models.generate_content(
                    model=model,
                    config=config,
                    contents=contents,
                )
                return response.text
            except ClientError as e:
                if "not in an ACTIVE state" in str(e) and attempt < max_retries - 1:
                    print(f"File not ready for processing, waiting 10 seconds before retry {attempt + 1}/{max_retries}...")
                    time.sleep(10)
                    continue
                else:
                    raise e
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Processing failed, retrying in 5 seconds... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(5)
                    continue
                else:
                    raise e


def main():
    """Example usage of the GenAI client"""
    try:
        client = GenAIClient()
        print("GenAI client initialized successfully")
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set the GEMINI_API_KEY environment variable")


if __name__ == "__main__":
    main()
