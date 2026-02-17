import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_groq(text):
    chat = client.chat.completions.create(
        messages=[{"role": "user", "content": text}],
        model="llama3-8b-8192",
    )
    return chat.choices[0].message.content