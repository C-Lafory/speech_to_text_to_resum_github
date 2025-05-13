from pathlib import Path
import os

# Flags d’environnement
IS_MAIN_SERVICE = os.getenv("IS_MAIN_SERVICE") == "1"
IS_TTS_SERVICE = os.getenv("IS_TTS_SERVICE") == "1"

# Dossiers principaux
MODELS_DIR = Path("models")

# Paramètres des modèles
WHISPER_MODEL_SIZE = "base"
TTS_MODEL_NAME = "tts_models/fr/css10/vits"
SPACY_MODEL_NAME = "fr_core_news_md"  # corrigé ici
OLLAMA_MODEL = "mistral:7b"

# Chemins utiles (utilisés uniquement pour stockage, pas pour chargement spaCy)
WHISPER_MODEL_DIR = MODELS_DIR / "whisper"
TTS_MODEL_DIR = MODELS_DIR / "tts"
SPACY_MODEL_DIR = MODELS_DIR / "spacy"
OLLAMA_DIR = MODELS_DIR / "ollama"

# Ports
MAIN_API_PORT = 8000
TTS_API_PORT = 8001
OLLAMA_PORT = 11434

# Hôte Ollama
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")

# Création des dossiers
for directory in [MODELS_DIR, WHISPER_MODEL_DIR, TTS_MODEL_DIR, SPACY_MODEL_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

assert IS_MAIN_SERVICE or IS_TTS_SERVICE, "Définir IS_MAIN_SERVICE=1 ou IS_TTS_SERVICE=1"
