from fastapi import FastAPI, HTTPException, Depends, Header
from typing import Optional
import os
import secrets
import tempfile
from text_to_speech import generate_tts_audio
import logging

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = FastAPI()

# Clé API pour l'authentification entre services
API_KEY = os.getenv("INTERNAL_API_KEY", secrets.token_hex(32))

# Middleware d'authentification
async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key

@app.post("/generate-audio")
async def generate_audio(
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
        
        # Création d'un fichier temporaire pour le texte
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_input:
            temp_input.write(text)
            temp_input_path = temp_input.name
        
        # Création d'un fichier temporaire pour l'audio
        temp_output_path = temp_input_path.replace('.txt', '.mp3')
        
        try:
            # Génération de l'audio
            generate_tts_audio(temp_input_path, temp_output_path)
            
            # Lecture du fichier audio généré
            with open(temp_output_path, 'rb') as audio_file:
                audio_content = audio_file.read()
            
            return {"audio_path": temp_output_path}
            
        finally:
            # Nettoyage des fichiers temporaires
            if os.path.exists(temp_input_path):
                os.unlink(temp_input_path)
            if os.path.exists(temp_output_path):
                os.unlink(temp_output_path)
                
    except Exception as e:
        logging.error(f"Erreur lors de la génération de l'audio : {e}")
        raise HTTPException(status_code=500, detail=str(e)) 