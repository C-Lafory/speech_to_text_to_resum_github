import os
from pathlib import Path

# Chemins des modèles
BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"
WHISPER_MODEL_DIR = MODELS_DIR / "whisper"
TTS_MODEL_DIR = MODELS_DIR / "tts"
SPACY_MODEL_DIR = MODELS_DIR / "spacy"

# Configuration des modèles
WHISPER_MODEL_SIZE = "base"
SPACY_MODEL = "fr_core_news_sm"
TTS_MODEL = "tts_models/multilingual/multi-dataset/your_tts"
OLLAMA_MODEL = "mistral:7b"

# Configuration des services
IS_TTS_SERVICE = os.path.exists(BASE_DIR / "text_to_speech.py")
IS_MAIN_SERVICE = os.path.exists(BASE_DIR / "transcription.py")

# Configuration des ports
MAIN_API_PORT = int(os.getenv("MAIN_API_PORT", "8000"))
TTS_API_PORT = int(os.getenv("TTS_API_PORT", "8001"))

# Configuration Ollama
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_PORT = int(os.getenv("OLLAMA_PORT", "11434"))

# Création des dossiers nécessaires
for directory in [MODELS_DIR, WHISPER_MODEL_DIR, TTS_MODEL_DIR, SPACY_MODEL_DIR]:
    directory.mkdir(parents=True, exist_ok=True) 