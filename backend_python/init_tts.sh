#!/bin/bash

# Activation de l'environnement virtuel
source /opt/venv/bin/activate

# Téléchargement des modèles TTS
echo "Téléchargement des modèles TTS..."
python download_models.py

# Démarrage de l'API TTS
echo "Démarrage de l'API TTS..."
exec uvicorn tts_api:app --host 0.0.0.0 --port 8001 