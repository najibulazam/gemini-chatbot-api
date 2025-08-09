from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import asyncio
import os

# load dot-env
load_dotenv()

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=f"{GEMINI_API_KEY}")
model = genai.GenerativeModel("gemini-1.5-flash")

# FastAPI app
app = FastAPI()

# Allow frontend access (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",          # Dev
        "https://gembot-chatbot-by-najib.netlify.app/"  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class PromptRequest(BaseModel):
    prompt: str

# Route to handle chat
@app.post("/chat")
async def chat(request: PromptRequest):
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: model.generate_content(request.prompt))
        return {"response": response.text}
    except Exception as e:
        return {"response": f"[ERROR] {str(e)}"}
