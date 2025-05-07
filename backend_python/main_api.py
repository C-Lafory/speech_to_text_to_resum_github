from fastapi import FastAPI, UploadFile, HTTPException, Depends, Header
from fastapi.security import APIKeyHeader
from typing import Optional
import os
import secrets
from transcription import transcribe_audio
from resume import generate_summary

app = FastAPI()

# Clé API pour l'authentification entre services
API_KEY = os.getenv("INTERNAL_API_KEY", secrets.token_hex(32))

# Middleware d'authentification
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key

@app.post("/transcribe")
async def transcribe(
    audio_file: UploadFile,
    api_key: str = Depends(verify_api_key)
):
    try:
        # Vérification du type de fichier
        if not audio_file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Vérification de la taille du fichier (max 100MB)
        if audio_file.size > 100 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large")
        
        # Traitement du fichier
        result = transcribe_audio(audio_file)
        return {"transcription": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
async def summarize(
    text: str,
    api_key: str = Depends(verify_api_key)
):
    try:
        # Vérification de la longueur du texte
        if len(text) > 100000:  # 100k caractères max
            raise HTTPException(status_code=400, detail="Text too long")
        
        result = generate_summary(text)
        return {"summary": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 