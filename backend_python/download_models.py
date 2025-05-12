import logging
import shutil
import requests
from pathlib import Path
from config import IS_MAIN_SERVICE, IS_TTS_SERVICE, OLLAMA_MODEL

# Configuration logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Paramètres
MIN_DISK_SPACE_GB = 5
WHISPER_MODEL_SIZE = "base"
SPACY_MODEL_NAME = "fr_core_news_md"
TTS_MODEL_NAME = "tts_models/fr/css10/vits"
OLLAMA_API_URL = "http://ollama:11434/api"

# Répertoires
MODELS_DIR = Path("models")
WHISPER_DIR = MODELS_DIR / "whisper"
SPACY_DIR = MODELS_DIR / "spacy"
TTS_DIR = MODELS_DIR / "tts"

def check_disk_space():
    """Vérifie l'espace disque disponible."""
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)
    if free_gb < MIN_DISK_SPACE_GB:
        raise RuntimeError(f"Espace disque insuffisant : {free_gb} GB disponibles.")

def download_main_models():
    """Téléchargement pour le service principal (transcription, résumé)."""
    import whisper
    import spacy

    logging.info("📥 Téléchargement du modèle Whisper...")
    whisper.load_model(WHISPER_MODEL_SIZE)

    logging.info("📥 Téléchargement du modèle Spacy...")
    try:
        spacy.load(SPACY_MODEL_NAME)
    except OSError:
        from spacy.cli import download
        download(SPACY_MODEL_NAME)
        spacy.load(SPACY_MODEL_NAME)

    logging.info("✅ Modèles principaux téléchargés avec succès.")

def ollama_ready() -> bool:
    """Vérifie si Ollama est joignable."""
    try:
        return requests.get(f"{OLLAMA_API_URL}/version").status_code == 200
    except Exception:
        return False

def mistral_available() -> bool:
    """Vérifie si Mistral est déjà présent dans Ollama."""
    try:
        response = requests.get(f"{OLLAMA_API_URL}/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            return any(m["name"] == OLLAMA_MODEL for m in models)
    except Exception:
        return False

def download_tts_model():
    """Téléchargement pour le service TTS."""
    from TTS.api import TTS

    logging.info("📥 Téléchargement du modèle TTS...")
    TTS(model_name=TTS_MODEL_NAME)
    logging.info("✅ Modèle TTS téléchargé avec succès.")

def main():
    try:
        check_disk_space()
        MODELS_DIR.mkdir(exist_ok=True)

        if IS_MAIN_SERVICE:
            if not ollama_ready():
                raise RuntimeError("❌ Ollama n'est pas disponible sur le port 11434.")
            if not mistral_available():
                raise RuntimeError(f"❌ Le modèle '{OLLAMA_MODEL}' n'est pas encore chargé dans Ollama.")
            download_main_models()

        if IS_TTS_SERVICE:
            download_tts_model()

        logging.info("🎉 Tous les modèles nécessaires ont été installés avec succès.")

    except Exception as e:
        logging.error(f"❌ Erreur lors de l'installation des modèles : {e}")
        raise

if __name__ == "__main__":
    main()
