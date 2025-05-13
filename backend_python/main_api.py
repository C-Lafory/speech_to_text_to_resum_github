from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header
import os
import secrets
from transcription import transcribe_audio
from resume import summarize_text

API_KEY = os.getenv("INTERNAL_API_KEY", secrets.token_hex(32))
app = FastAPI()

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

@app.post("/transcribe")
async def transcribe(audio_file: UploadFile = File(...), api_key: str = Depends(verify_api_key)):
    path = f"/tmp/{audio_file.filename}"
    with open(path, "wb") as f:
        f.write(await audio_file.read())
    text = transcribe_audio(path)
    return {"transcription": text}

@app.post("/summarize")
async def summarize(body: dict, api_key: str = Depends(verify_api_key)):
    summary = summarize_text(body.get("text", ""))
    return {"summary": summary}
