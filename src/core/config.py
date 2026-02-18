import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = "SARA_AI"
    
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    
    # Brain Config - Using the absolute latest Flash model
    GEMINI_MODEL = "gemini-2.0-flash-exp" # या "gemini-2.0-flash" अगर आपके रीजन में उपलब्ध है
    
    TEMPERATURE = 0.7
    MAX_TOKENS = 512 # वॉयस के लिए छोटे रिस्पॉन्स बेहतर होते हैं

settings = Settings()