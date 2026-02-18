import os
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import google.generativeai as genai
import uvicorn

load_dotenv()

# --- PATH SETUP ---
# This ensures the 'templates' folder is found correctly inside 'src'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# --- GEMINI SETUP ---
# Match the key name in your .env (GEMINI_API_KEY)
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file")
else:
    print("✅ API Key loaded successfully")

genai.configure(api_key=api_key)

# Using Gemini 2.0 Flash (latest high-speed model)
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash', # Use the exact string you saw in check_models.py
    system_instruction="You are SARA, a helpful voice assistant. Keep answers very short (1-2 sentences)."
)

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🚀 WebSocket Connected to Client")
    
    try:
        while True:
            # Receive message from frontend
            user_text = await websocket.receive_text()
            print(f"📩 User Message: {user_text}")
            
            try:
                # Use generate_content_async for proper FastAPI streaming
                response = await model.generate_content_async(user_text, stream=True)
                
                print("🧠 Gemini is thinking...")
                async for chunk in response:
                 if chunk.text:
                    # Strip extra spaces if necessary, but send the text
                    await websocket.send_text(chunk.text)
            
            
                
                # Signal the frontend that the response is finished
                await websocket.send_text("<END>")
                print("✅ Response fully streamed")

            except Exception as e:
                error_msg = f"Gemini Error: {str(e)}"
                print(f"❌ {error_msg}")
                await websocket.send_text(error_msg)
                await websocket.send_text("<END>")

    except Exception as e:
        print(f"⚠️ Connection closed: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    # Run server on port 5000
    uvicorn.run(app, host="0.0.0.0", port=5000)