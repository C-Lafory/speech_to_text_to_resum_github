import logging
import shutil
import requests
import whisper
import spacy
from TTS.api import TTS
from pathlib import Path
from config import (
    IS_MAIN_SERVICE,
    IS_TTS_SERVICE,
    WHISPER_MODEL_SIZE,
    SPACY_MODEL_NAME,
    TTS_MODEL_NAME,
    TTS_MODEL_DIR,
    WHISPER_MODEL_DIR,
    SPACY_MODEL_DIR,
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
    # Whisper
    logging.info("📥 Téléchargement du modèle Whisper dans %s...", WHISPER_MODEL_DIR)
    WHISPER_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    whisper.load_model(WHISPER_MODEL_SIZE, download_root=str(WHISPER_MODEL_DIR))
    logging.info("✅ Modèle Whisper téléchargé localement.")

    # spaCy
    logging.info("📥 Téléchargement du modèle Spacy dans %s...", SPACY_MODEL_DIR)
    SPACY_MODEL_DIR.mkdir(parents=True, exist_ok=True)

    try:
        spacy.load(str(SPACY_MODEL_DIR / SPACY_MODEL_NAME))
        logging.info("✅ Modèle Spacy déjà présent localement.")
    except:
        from spacy.cli import download
        download(SPACY_MODEL_NAME)
        logging.info("✅ Modèle Spacy téléchargé via spacy.cli.")

    # Ollama Mistral
    try:
        tags = requests.get(f"{OLLAMA_API_URL}/tags").json()
        if not any(model["name"] == OLLAMA_MODEL for model in tags.get("models", [])):
            logging.info("📥 Téléchargement du modèle Ollama : %s", OLLAMA_MODEL)
            requests.post(f"{OLLAMA_API_URL}/pull", json={"name": OLLAMA_MODEL})
            logging.info("✅ Modèle Ollama téléchargé.")
        else:
            logging.info("✅ Modèle Ollama déjà présent.")
    except Exception as e:
        logging.warning(f"⚠️ Impossible de vérifier Ollama : {e}")

def download_tts_models():
    logging.info("📥 Téléchargement du modèle TTS dans %s...", TTS_MODEL_DIR)
    TTS_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    try:
        TTS(model_name=TTS_MODEL_NAME, progress_bar=False).to("cpu")
        logging.info("✅ Modèle TTS téléchargé localement.")
    except Exception as e:
        logging.error(f"❌ Erreur de téléchargement du modèle TTS : {e}")
        raise

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
