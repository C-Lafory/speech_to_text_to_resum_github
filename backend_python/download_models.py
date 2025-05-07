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
OLLAMA_API_URL = "http://ollama:11434/api"

# Création des répertoires
MODELS_DIR.mkdir(exist_ok=True)
WHISPER_DIR = MODELS_DIR / "whisper"
TTS_DIR = MODELS_DIR / "tts"
SPACY_DIR = MODELS_DIR / "spacy"
OLLAMA_DIR = MODELS_DIR / "ollama"

def get_whisper():
    """Importe whisper uniquement si nécessaire"""
    if IS_MAIN_SERVICE:
        import whisper
        return whisper
    return None

def get_spacy():
    """Importe spacy uniquement si nécessaire"""
    if IS_MAIN_SERVICE:
        import spacy
        return spacy
    return None

def check_disk_space():
    """Vérifie l'espace disque disponible"""
    try:
        total, used, free = shutil.disk_usage("/")
        free_gb = free // (2**30)  # Conversion en GB
        if free_gb < 5:  # 5 GB minimum requis
            raise Exception(f"Espace disque insuffisant: {free_gb} GB disponibles")
    except Exception as e:
        logging.error(f"Erreur lors de la vérification de l'espace disque: {str(e)}")
        raise

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
    models_status = {}
    
    # Vérification des modèles pour le service principal
    if IS_MAIN_SERVICE:
        models_status.update({
            "whisper": False,
            "spacy": False,
            "ollama": False,
            "mistral": False
        })
        
        # Vérification Whisper
        whisper = get_whisper()
        if whisper:
            whisper_model_path = WHISPER_DIR / f"{WHISPER_MODEL_SIZE}.pt"
            models_status["whisper"] = whisper_model_path.exists()
        
        # Vérification Spacy
        spacy = get_spacy()
        if spacy:
            try:
                spacy.load(SPACY_MODEL_NAME)
                models_status["spacy"] = True
            except (OSError, ImportError):
                pass
        
        # Vérification Ollama et Mistral
        models_status["ollama"] = check_ollama_status()
        if models_status["ollama"]:
            models_status["mistral"] = check_mistral_model()
    
    # Vérification des modèles pour le service TTS
    if IS_TTS_SERVICE:
        models_status.update({
            "tts": False
        })
        try:
            from TTS.api import TTS
            tts = TTS(model_name=TTS_MODEL_NAME, progress_bar=False)
            models_status["tts"] = True
        except Exception:
            pass
    
    return models_status

def download_models():
    """Télécharge les modèles nécessaires"""
    try:
        # Vérifier l'espace disque
        check_disk_space()
        
        # Créer les répertoires
        MODELS_DIR.mkdir(exist_ok=True)
        
        # Télécharger les modèles selon le service
        if IS_MAIN_SERVICE:
            # Télécharger Whisper
            logging.info("Téléchargement du modèle Whisper...")
            import whisper
            whisper.load_model(WHISPER_MODEL_SIZE)
            
            # Télécharger Spacy
            logging.info("Téléchargement du modèle Spacy...")
            import spacy
            spacy.load(SPACY_MODEL_NAME)
            
        if IS_TTS_SERVICE:
            # Télécharger TTS
            logging.info("Téléchargement du modèle TTS...")
            from TTS.api import TTS
            TTS(model_name=TTS_MODEL_NAME)
            
        logging.info("Tous les modèles ont été téléchargés avec succès")
        
    except Exception as e:
        logging.error(f"Erreur lors du téléchargement des modèles: {str(e)}")
        raise

if __name__ == "__main__":
    download_models()
    