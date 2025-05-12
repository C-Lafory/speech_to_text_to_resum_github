import os
import logging
from pathlib import Path

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Configuration des services via des variables d'environnement claires
IS_MAIN_SERVICE = os.getenv("IS_MAIN_SERVICE") == "1"
IS_TTS_SERVICE = os.getenv("IS_TTS_SERVICE") == "1"

# Modèles à télécharger
MODELS_DIR = Path("models")
WHISPER_MODEL_SIZE = "base"
TTS_MODEL = "tts_models/fr/css10/vits"
TTS_MODEL_NAME = "tts_models/fr/css10/vits"
SPACY_MODEL_NAME = "fr_core_news_md"
OLLAMA_MODEL = "mistral:7b"

# Ports
MAIN_API_PORT = 8000
TTS_API_PORT = 8001
OLLAMA_PORT = 11434

# Chemins des modèles
BASE_DIR = Path(__file__).parent
WHISPER_MODEL_DIR = MODELS_DIR / "whisper"
TTS_MODEL_DIR = MODELS_DIR / "tts"
SPACY_MODEL_DIR = MODELS_DIR / "spacy"
OLLAMA_DIR = MODELS_DIR / "ollama"

# Configuration de Ollama (en dev ou prod)
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")

# Création des dossiers nécessaires
for directory in [MODELS_DIR, WHISPER_MODEL_DIR, TTS_MODEL_DIR, SPACY_MODEL_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Vérification de sécurité
assert IS_MAIN_SERVICE or IS_TTS_SERVICE, "⚠️ Définir IS_MAIN_SERVICE=1 ou IS_TTS_SERVICE=1 dans les variables d'environnement."
