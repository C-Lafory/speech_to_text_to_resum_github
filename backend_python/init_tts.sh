#!/bin/bash

# Téléchargement des modèles TTS
echo "Téléchargement des modèles TTS..."
python download_models.py

# Démarrage du serveur API TTS
echo "Démarrage du serveur API TTS..."
uvicorn tts_api:app --host 0.0.0.0 --port 8001 