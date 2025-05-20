from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header
import os
import secrets
import tempfile
from transcription import transcribe_audio, check_audio_format
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
async def transcribe(audio_file: UploadFile = File(...), api_key: str = Depends(verify_api_key)):
    try:
        # Vérifier le type de fichier
        if not audio_file.filename:
            raise HTTPException(status_code=400, detail="Nom de fichier manquant")
        
        # Créer un fichier temporaire avec un nom unique
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.filename)[1]) as temp_file:
            logger.info(f"Création du fichier temporaire : {temp_file.name}")
            
            # Sauvegarder le fichier audio
            shutil.copyfileobj(audio_file.file, temp_file)
            
            # Vérifier le format audio
            if not check_audio_format(temp_file.name):
                os.unlink(temp_file.name)
                raise HTTPException(status_code=400, detail="Format audio non supporté")
            
            # Transcrire l'audio
            logger.info(f"Début de la transcription du fichier : {temp_file.name}")
            transcription = transcribe_audio(temp_file.name)
            logger.info("Transcription terminée avec succès")
            
            # Nettoyer le fichier temporaire
            os.unlink(temp_file.name)
            
            return {"transcription": transcription}
            
    except Exception as e:
        logger.error(f"Erreur lors de la transcription : {str(e)}")
        # Nettoyer le fichier temporaire en cas d'erreur
        if 'temp_file' in locals():
            try:
                os.unlink(temp_file.name)
            except:
                pass
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
