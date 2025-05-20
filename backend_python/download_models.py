import logging
import shutil
import os
from pathlib import Path
from config import (
    IS_MAIN_SERVICE,
    IS_TTS_SERVICE,
    WHISPER_MODEL_SIZE,
    SPACY_MODEL_NAME,
    WHISPER_MODEL_DIR,
    TTS_MODEL_NAME,
    TTS_MODEL_DIR,
    OLLAMA_MODEL
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
OLLAMA_API_URL = "http://ollama:11434/api"

def check_disk_space():
    total, used, free = shutil.disk_usage("/")
    if free // (2**30) < 5:
        raise RuntimeError("Espace disque insuffisant")

def download_main_models():
    import whisper
    import spacy
    import requests
    from spacy.cli import download as spacy_download

    logging.info("📥 Téléchargement Whisper...")
    WHISPER_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    whisper.load_model(WHISPER_MODEL_SIZE, download_root=str(WHISPER_MODEL_DIR))
    logging.info("✅ Whisper OK.")

    try:
        spacy.load(SPACY_MODEL_NAME)
        logging.info("✅ spaCy déjà installé.")
    except:
        logging.info(f"📥 Téléchargement spaCy : {SPACY_MODEL_NAME}")
        spacy_download(SPACY_MODEL_NAME)

    try:
        tags = requests.get(f"{OLLAMA_API_URL}/tags").json()
        if not any(model["name"] == OLLAMA_MODEL for model in tags.get("models", [])):
            logging.info(f"📥 Téléchargement du modèle Ollama {OLLAMA_MODEL}...")
            requests.post(f"{OLLAMA_API_URL}/pull", json={"name": OLLAMA_MODEL})
        else:
            logging.info("✅ Modèle Ollama déjà présent.")
    except Exception as e:
        logging.warning(f"⚠️ Vérification Ollama impossible : {e}")

def download_tts_models():
    from TTS.api import TTS
    logging.info("📥 Téléchargement du modèle TTS...")
    TTS_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    
    # Initialisation du modèle avec un locuteur spécifique
    tts = TTS(model_name=TTS_MODEL_NAME, progress_bar=False)
    tts.to("cpu")
    
    # Vérification et configuration du locuteur
    if hasattr(tts, 'speakers') and tts.speakers:
        logging.info(f"✅ TTS OK. Locuteurs disponibles : {tts.speakers}")
    else:
        logging.warning("⚠️ Aucun locuteur détecté dans le modèle TTS")
    
    # Sauvegarde de la configuration
    config_path = TTS_MODEL_DIR / "tts_config.json"
    with open(config_path, "w") as f:
        import json
        json.dump({
            "model_name": TTS_MODEL_NAME,
            "speakers": tts.speakers if hasattr(tts, 'speakers') else [],
            "languages": ["fr"]
        }, f, indent=2)
    
    logging.info("✅ Configuration TTS sauvegardée.")

def main():
    check_disk_space()
    if IS_MAIN_SERVICE:
        download_main_models()
    if IS_TTS_SERVICE:
        download_tts_models()

if __name__ == "__main__":
    main()
