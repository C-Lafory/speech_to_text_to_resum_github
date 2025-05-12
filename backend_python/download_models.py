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
    SPACY_MODEL_DIR,
    TTS_MODEL_NAME,
    TTS_MODEL_DIR,
    OLLAMA_MODEL
)

# Configuration logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

MIN_DISK_SPACE_GB = 5
OLLAMA_API_URL = "http://ollama:11434/api"

def check_disk_space():
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)
    if free_gb < MIN_DISK_SPACE_GB:
        raise RuntimeError(f"Espace disque insuffisant : {free_gb} GB disponibles.")

def download_main_models():
    import whisper
    import spacy
    import requests
    from spacy.cli import download as spacy_download

    # Whisper
    logging.info("📥 Téléchargement du modèle Whisper dans %s...", WHISPER_MODEL_DIR)
    WHISPER_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    whisper.load_model(WHISPER_MODEL_SIZE, download_root=str(WHISPER_MODEL_DIR))
    logging.info("✅ Modèle Whisper téléchargé localement.")

    # spaCy
    logging.info("📥 Vérification du modèle spaCy dans %s...", SPACY_MODEL_DIR)
    SPACY_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    try:
        spacy.load(str(SPACY_MODEL_DIR / SPACY_MODEL_NAME))
        logging.info("✅ Modèle spaCy déjà présent localement.")
    except:
        spacy_download(SPACY_MODEL_NAME)
        logging.info("✅ Modèle spaCy téléchargé.")

    # Ollama
    try:
        tags = requests.get(f"{OLLAMA_API_URL}/tags").json()
        if not any(model["name"] == OLLAMA_MODEL for model in tags.get("models", [])):
            logging.info(f"📥 Téléchargement du modèle Ollama {OLLAMA_MODEL}...")
            requests.post(f"{OLLAMA_API_URL}/pull", json={"name": OLLAMA_MODEL})
            logging.info("✅ Modèle Ollama téléchargé.")
        else:
            logging.info("✅ Modèle Ollama déjà installé.")
    except Exception as e:
        logging.warning(f"⚠️ Vérification Ollama impossible : {e}")

def download_tts_models():
    from TTS.api import TTS
    logging.info("📥 Téléchargement du modèle TTS dans %s...", TTS_MODEL_DIR)
    TTS_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    TTS(model_name=TTS_MODEL_NAME).to("cpu")
    logging.info("✅ Modèle TTS téléchargé localement.")

def main():
    check_disk_space()
    if IS_MAIN_SERVICE:
        logging.info("🔧 Service principal détecté (main_api)")
        download_main_models()
    if IS_TTS_SERVICE:
        logging.info("🔧 Service TTS détecté (tts_service)")
        download_tts_models()

if __name__ == "__main__":
    main()
