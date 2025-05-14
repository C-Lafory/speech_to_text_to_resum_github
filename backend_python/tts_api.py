from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import FileResponse
from text_to_speech import text_to_speech
import os
import secrets

API_KEY = os.getenv("INTERNAL_API_KEY", secrets.token_hex(32))
app = FastAPI()

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

@app.post("/speak")
async def speak(body: dict, api_key: str = Depends(verify_api_key)):
    text = body.get("text", "")
    output = "/tmp/tts_output.wav"
    text_to_speech(text, output)
    return FileResponse(output, media_type="audio/wav")