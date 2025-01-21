from fastapi import FastAPI, HTTPException
from models import QueryRequest
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is missing. Please set it in the .env file.")

genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

@app.post("/chat/")
async def chat_with_gemini(request: QueryRequest):
    try:
        model = genai.GenerativeModel("gemini-pro")  
        response = model.generate_content(request.query)

        if response and response.text:
            return {"response": response.text}
        else:
            raise HTTPException(status_code=500, detail="No response from Gemini AI")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

