import os
import logging
from pathlib import Path

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Configuration des services
IS_MAIN_SERVICE = os.getenv("SERVICE_TYPE", "main") == "main"
IS_TTS_SERVICE = os.getenv("SERVICE_TYPE", "main") == "tts"

# Configuration des modèles
MODELS_DIR = Path("models")
WHISPER_MODEL_SIZE = "base"
TTS_MODEL = "tts_models/fr/css10/vits"
TTS_MODEL_NAME = "tts_models/fr/css10/vits"
SPACY_MODEL_NAME = "fr_core_news_md"
OLLAMA_MODEL = "mistral"

# Configuration des services
MAIN_API_PORT = 8000
TTS_API_PORT = 8001
OLLAMA_PORT = 11434

# Création des répertoires
MODELS_DIR.mkdir(exist_ok=True)
WHISPER_DIR = MODELS_DIR / "whisper"
TTS_DIR = MODELS_DIR / "tts"
SPACY_DIR = MODELS_DIR / "spacy"
OLLAMA_DIR = MODELS_DIR / "ollama"

# Chemins des modèles
BASE_DIR = Path(__file__).parent
WHISPER_MODEL_DIR = MODELS_DIR / "whisper"
TTS_MODEL_DIR = MODELS_DIR / "tts"
SPACY_MODEL_DIR = MODELS_DIR / "spacy"

# Configuration Ollama
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")

# Création des dossiers nécessaires
for directory in [MODELS_DIR, WHISPER_MODEL_DIR, TTS_MODEL_DIR, SPACY_MODEL_DIR]:
    directory.mkdir(parents=True, exist_ok=True) 