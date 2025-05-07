#!/bin/bash

# Activation de l'environnement virtuel
source /opt/venv/bin/activate

# Attente que Ollama soit prêt
echo "Attente du démarrage d'Ollama..."
until curl -s http://ollama:11434/api/version > /dev/null; do
    sleep 1
done

# Vérification du modèle Mistral
if ! curl -s http://ollama:11434/api/tags | grep -q "mistral:7b"; then
    echo "Téléchargement du modèle Mistral..."
    curl -X POST http://ollama:11434/api/pull -d '{"name": "mistral:7b"}'
fi

# Téléchargement des autres modèles
python download_models.py

# Démarrage de l'API
exec uvicorn main_api:app --host 0.0.0.0 --port 8000 
