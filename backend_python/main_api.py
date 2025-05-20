from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header
import os
import secrets
from transcription import transcribe_audio
from resume import summarize_text
from fastapi.middleware.cors import CORSMiddleware
import shutil
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("INTERNAL_API_KEY", secrets.token_hex(32))
app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...), api_key: str = Depends(verify_api_key)):
    try:
        # Chemin du fichier créé par Golang
        file_path = f"/tmp/static/file/user_2/f44ef1e3-b16f-4e84-9cd2-605699743237/audio.qt"
        
        # Vérifier si le fichier existe
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Fichier audio non trouvé")
        
        # Transcrire l'audio
        transcription = transcribe_audio(file_path)
        return {"transcription": transcription}
    except Exception as e:
        logger.error(f"Erreur lors de la transcription : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/summarize")
async def summarize(body: dict, api_key: str = Depends(verify_api_key)):
    text = body.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Texte manquant.")
    try:
        summary = summarize_text(text)
        return {"summary": summary}
    except Exception as e:
        logger.error(f"Erreur lors de la génération du résumé : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
