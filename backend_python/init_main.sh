#!/bin/bash

# Téléchargement des modèles
echo "Téléchargement des modèles pour la transcription et le résumé..."
python download_models.py

# Démarrage du serveur API principal
echo "Démarrage du serveur API principal..."
uvicorn main_api:app --host 0.0.0.0 --port 8000 
