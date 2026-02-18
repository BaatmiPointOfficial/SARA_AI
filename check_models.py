import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load your .env file
load_dotenv()

# Configure with your key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("--- FETCHING AVAILABLE MODELS ---")
try:
    # List all models
    for m in genai.list_models():
        # Check if the model supports generating content
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model Name: {m.name}")
            print(f"Display Name: {m.display_name}")
            print("-" * 30)
except Exception as e:
    print(f"Error fetching models: {e}")