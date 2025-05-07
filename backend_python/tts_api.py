from fastapi import FastAPI, HTTPException, Depends, Header
from typing import Optional
import os
import secrets
from text_to_speech import generate_audio

app = FastAPI()

# Clé API pour l'authentification entre services
API_KEY = os.getenv("INTERNAL_API_KEY", secrets.token_hex(32))

# Middleware d'authentification
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key

@app.post("/generate-audio")
async def generate_tts(
    text: str,
    api_key: str = Depends(verify_api_key)
):
    try:
        # Vérification de la longueur du texte
        if len(text) > 50000:  # 50k caractères max
            raise HTTPException(status_code=400, detail="Text too long")
        
        # Vérification du contenu (pas de code malveillant)
        if "<script>" in text.lower() or "javascript:" in text.lower():
            raise HTTPException(status_code=400, detail="Invalid text content")
        
        result = generate_audio(text)
        return {"audio_path": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 