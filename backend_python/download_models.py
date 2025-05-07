import os
import sys
import shutil
import logging
import requests
from pathlib import Path
import torch
from config import IS_MAIN_SERVICE, IS_TTS_SERVICE, OLLAMA_MODEL

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Configuration de l'espace disque
MIN_DISK_SPACE_GB = 5  # Espace disque minimum requis en GB

# Chemins des modèles
MODELS_DIR = Path("models")
WHISPER_MODEL_SIZE = "base"
TTS_MODEL = "tts_models/fr/css10/vits"  # Alias pour TTS_MODEL_NAME
TTS_MODEL_NAME = "tts_models/fr/css10/vits"
SPACY_MODEL_NAME = "fr_core_news_md"

# Configuration Ollama
OLLAMA_API_URL = "http://0.0.0.0:11434/api"

# Création des répertoires
MODELS_DIR.mkdir(exist_ok=True)
WHISPER_DIR = MODELS_DIR / "whisper"
TTS_DIR = MODELS_DIR / "tts"
SPACY_DIR = MODELS_DIR / "spacy"
OLLAMA_DIR = MODELS_DIR / "ollama"

# Import conditionnel des modules
if IS_MAIN_SERVICE:
    import whisper
    import spacy

if IS_TTS_SERVICE:
    from TTS.utils.manage import ModelManager
    from TTS.utils.synthesizer import Synthesizer
    from TTS.api import TTS

def check_disk_space():
    """Vérifie l'espace disque disponible"""
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)  # Conversion en GB
    if free_gb < MIN_DISK_SPACE_GB:
        raise RuntimeError(f"❌ Espace disque insuffisant. {free_gb}GB disponible, {MIN_DISK_SPACE_GB}GB requis.")

def check_ollama_status():
    """Vérifie le statut d'Ollama via l'API"""
    try:
        response = requests.get(f"{OLLAMA_API_URL}/version")
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        return False
    return False

def check_mistral_model():
    """Vérifie si le modèle Mistral est disponible"""
    try:
        response = requests.get(f"{OLLAMA_API_URL}/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            return any(model["name"] == OLLAMA_MODEL for model in models)
    except requests.exceptions.RequestException:
        return False
    return False

def verify_models():
    """Vérifie si tous les modèles sont présents"""
    models_status = {
        "whisper": False,
        "spacy": False,
        "tts": False,
        "ollama": False,
        "mistral": False
    }
    
    # Vérification Whisper (uniquement pour le service principal)
    if IS_MAIN_SERVICE:
        whisper_model_path = WHISPER_DIR / f"{WHISPER_MODEL_SIZE}.pt"
        models_status["whisper"] = whisper_model_path.exists()
        
        # Vérification Spacy
        try:
            spacy.load(SPACY_MODEL_NAME)
            models_status["spacy"] = True
        except (OSError, ImportError):
            pass
        
        # Vérification Ollama et Mistral
        models_status["ollama"] = check_ollama_status()
        if models_status["ollama"]:
            models_status["mistral"] = check_mistral_model()
    
    # Vérification TTS (uniquement pour le service TTS)
    if IS_TTS_SERVICE:
        try:
            tts = TTS(model_name=TTS_MODEL_NAME, progress_bar=False)
            models_status["tts"] = True
        except Exception:
            pass
    
    return models_status

def download_models():
    """Télécharge tous les modèles nécessaires"""
    # Vérification de l'espace disque
    check_disk_space()

    # 1. Vérification et téléchargement du modèle Whisper
    if IS_MAIN_SERVICE:
        logging.info(f"🔍 Vérification du modèle Whisper ({WHISPER_MODEL_SIZE})...")
        whisper_model_path = WHISPER_DIR / f"{WHISPER_MODEL_SIZE}.pt"
        if not whisper_model_path.exists():
            logging.info(f"⬇️ Téléchargement du modèle Whisper ({WHISPER_MODEL_SIZE})...")
            whisper.load_model(WHISPER_MODEL_SIZE, download_root=str(WHISPER_DIR))
            logging.info(f"✅ Modèle Whisper téléchargé dans {WHISPER_DIR}")
        else:
            logging.info(f"✅ Modèle Whisper déjà présent : {whisper_model_path}")

        # 2. Vérification et téléchargement du modèle Spacy
        logging.info(f"🔍 Vérification du modèle Spacy ({SPACY_MODEL_NAME})...")
        try:
            spacy.load(SPACY_MODEL_NAME)
            logging.info(f"✅ Modèle Spacy déjà présent")
        except (OSError, ImportError):
            logging.info(f"⬇️ Téléchargement du modèle Spacy ({SPACY_MODEL_NAME})...")
            spacy.cli.download(SPACY_MODEL_NAME)
            logging.info(f"✅ Modèle Spacy téléchargé")

    # 3. Vérification et téléchargement du modèle TTS
    if IS_TTS_SERVICE:
        logging.info(f"🔍 Vérification du modèle TTS ({TTS_MODEL_NAME})...")
        try:
            tts = TTS(model_name=TTS_MODEL_NAME, progress_bar=False)
            if tts.speakers and len(tts.speakers) > 0:
                logging.info(f"✅ Modèle TTS déjà présent et fonctionnel")
            else:
                raise RuntimeError("Modèle TTS présent mais pas de locuteurs disponibles")
        except Exception as e:
            logging.info(f"⬇️ Téléchargement du modèle TTS ({TTS_MODEL_NAME})...")
            tts = TTS(model_name=TTS_MODEL_NAME, progress_bar=True)
            if not tts.speakers or len(tts.speakers) == 0:
                raise RuntimeError("Modèle TTS téléchargé mais pas de locuteurs disponibles")
            logging.info(f"✅ Modèle TTS téléchargé")

    # Vérification finale
    models_status = verify_models()
    if all(models_status.values()):
        logging.info("✅ Tous les modèles sont correctement installés et fonctionnels")
    else:
        missing_models = [model for model, status in models_status.items() if not status]
        logging.warning(f"⚠️ Certains modèles ne sont pas correctement installés : {', '.join(missing_models)}")

if __name__ == "__main__":
    download_models()
    