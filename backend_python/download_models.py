import os
import logging
import subprocess
import shutil
from config import *

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def check_disk_space():
    """Vérifie l'espace disque disponible"""
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)  # Conversion en GB
    if free_gb < MIN_DISK_SPACE_GB:
        raise RuntimeError(f"❌ Espace disque insuffisant. {free_gb}GB disponible, {MIN_DISK_SPACE_GB}GB requis.")

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
        whisper_model_path = WHISPER_MODEL_DIR / f"{WHISPER_MODEL_SIZE}.pt"
        models_status["whisper"] = whisper_model_path.exists()
        
        # Vérification Spacy
        try:
            import spacy
            spacy.load(SPACY_MODEL)
            models_status["spacy"] = True
        except (OSError, ImportError):
            pass
    
    # Vérification TTS (uniquement pour le service TTS)
    if IS_TTS_SERVICE:
        try:
            from TTS.api import TTS
            tts = TTS(model_name=TTS_MODEL, progress_bar=False)
            models_status["tts"] = True
        except Exception:
            pass
    
    # Vérification Ollama (uniquement pour le service principal)
    if IS_MAIN_SERVICE:
        try:
            result = subprocess.run(["ollama", "--version"], 
                                 capture_output=True, text=True)
            if result.returncode == 0:
                models_status["ollama"] = True
                result = subprocess.run(["ollama", "list"], 
                                     capture_output=True, text=True)
                models_status["mistral"] = OLLAMA_MODEL in result.stdout
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
        whisper_model_path = WHISPER_MODEL_DIR / f"{WHISPER_MODEL_SIZE}.pt"
        if not whisper_model_path.exists():
            logging.info(f"⬇️ Téléchargement du modèle Whisper ({WHISPER_MODEL_SIZE})...")
            import whisper
            whisper.load_model(WHISPER_MODEL_SIZE, download_root=str(WHISPER_MODEL_DIR))
            logging.info(f"✅ Modèle Whisper téléchargé dans {WHISPER_MODEL_DIR}")
        else:
            logging.info(f"✅ Modèle Whisper déjà présent : {whisper_model_path}")

        # 2. Vérification et téléchargement du modèle Spacy
        logging.info(f"🔍 Vérification du modèle Spacy ({SPACY_MODEL})...")
        try:
            import spacy
            spacy.load(SPACY_MODEL)
            logging.info(f"✅ Modèle Spacy déjà présent")
        except (OSError, ImportError):
            logging.info(f"⬇️ Téléchargement du modèle Spacy ({SPACY_MODEL})...")
            spacy.cli.download(SPACY_MODEL)
            logging.info(f"✅ Modèle Spacy téléchargé")

    # 3. Vérification et téléchargement du modèle TTS
    if IS_TTS_SERVICE:
        logging.info(f"🔍 Vérification du modèle TTS ({TTS_MODEL})...")
        try:
            from TTS.api import TTS
            tts = TTS(model_name=TTS_MODEL, progress_bar=False)
            if tts.speakers and len(tts.speakers) > 0:
                logging.info(f"✅ Modèle TTS déjà présent et fonctionnel")
            else:
                raise RuntimeError("Modèle TTS présent mais pas de locuteurs disponibles")
        except Exception as e:
            logging.info(f"⬇️ Téléchargement du modèle TTS ({TTS_MODEL})...")
            tts = TTS(model_name=TTS_MODEL, progress_bar=True)
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
    