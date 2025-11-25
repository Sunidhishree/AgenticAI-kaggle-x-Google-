"""
Setup and Authentication for Google Gemini API
"""
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Fix encoding for Windows when running in background
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Load environment variables
load_dotenv()

try:
    # Get API key from environment
    GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
    os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
    
    # Configure Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    
    print("[OK] Setup and authentication complete.")
    
except Exception as e:
    print(f"[ERROR] Authentication Error: {e}")
    raise

print("[OK] Gemini API configured successfully.")
