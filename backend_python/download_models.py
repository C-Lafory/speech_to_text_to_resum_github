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
    logging.info("📥 Téléchargement du modèle Whisper dans %s...", WHISPER_MODEL_DIR)
    WHISPER_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    whisper.load_model(WHISPER_MODEL_SIZE, download_root=str(WHISPER_MODEL_DIR))
    logging.info("✅ Modèle Whisper téléchargé localement.")

    logging.info("📥 Téléchargement du modèle Spacy dans %s...", SPACY_MODEL_DIR)
    SPACY_MODEL_DIR.mkdir(parents=True, exist_ok=True)

    try:
        spacy.load(str(SPACY_MODEL_DIR))
        logging.info("✅ Modèle Spacy déjà disponible.")
    except:
        from spacy.cli import download
        download(SPACY_MODEL_NAME)
        # Déplacement manuel du modèle téléchargé
        import shutil as sh
        import importlib.util
        spec = importlib.util.find_spec(SPACY_MODEL_NAME)
        if spec and spec.submodule_search_locations:
            model_path = Path(spec.submodule_search_locations[0])
            if model_path.exists():
                sh.copytree(model_path, SPACY_MODEL_DIR, dirs_exist_ok=True)
                logging.info("✅ Modèle Spacy copié localement dans %s.", SPACY_MODEL_DIR)
            else:
                raise RuntimeError("Impossible de localiser le modèle Spacy téléchargé.")
        else:
            raise RuntimeError("Erreur lors de la détection du modèle Spacy.")

def ollama_ready():
    try:
        return requests.get(f"{OLLAMA_API_URL}/version").status_code == 200
    except Exception:
        return False

def mistral_available():
    try:
        response = requests.get(f"{OLLAMA_API_URL}/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            return any(m["name"] == OLLAMA_MODEL for m in models)
    except Exception:
        return False

def download_tts_model():
    logging.info("📥 Téléchargement du modèle TTS...")
    tts = TTS(model_name=TTS_MODEL_NAME)
    tts.save_model(output_path=TTS_MODEL_DIR)
    logging.info(f"✅ Modèle TTS sauvegardé localement dans {TTS_MODEL_DIR}")

def main():
    try:
        check_disk_space()

        if IS_MAIN_SERVICE:
            if not ollama_ready():
                raise RuntimeError("❌ Ollama n'est pas disponible.")
            if not mistral_available():
                raise RuntimeError(f"❌ Le modèle '{OLLAMA_MODEL}' n'est pas encore chargé dans Ollama.")
            download_main_models()

        if IS_TTS_SERVICE:
            download_tts_model()

        logging.info("🎉 Tous les modèles ont été installés localement avec succès.")

    except Exception as e:
        logging.error(f"❌ Erreur : {e}")
        raise

if __name__ == "__main__":
    main()
