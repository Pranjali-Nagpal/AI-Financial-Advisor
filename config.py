import os
from dotenv import load_dotenv
from google import genai

def setup_environment():
    """Loads the API key and returns a Gemini client."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("API Key missing! Please set GEMINI_API_KEY in your .env file.")
        
    client = genai.Client(api_key=api_key)
    return client