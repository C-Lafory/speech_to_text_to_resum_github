import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from text_to_speech import generate_tts_audio

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = FastAPI()

class TextToSpeechRequest(BaseModel):
    text: str

@app.post("/tts")
async def text_to_speech(request: TextToSpeechRequest):
    try:
        # Créer le répertoire de sortie s'il n'existe pas
        output_dir = "static/output/tts"
        os.makedirs(output_dir, exist_ok=True)
        
        # Générer un nom de fichier unique
        output_path = os.path.join(output_dir, f"tts_output_{hash(request.text)}.wav")
        
        # Générer l'audio
        audio_path = generate_tts_audio(request.text, output_path)
        
        return {"audio_path": audio_path}
        
    except Exception as e:
        logging.error(f"Erreur lors de la génération de l'audio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 