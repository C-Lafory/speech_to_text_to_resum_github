#!/bin/bash

# Activation de l'environnement virtuel
source /opt/venv/bin/activate

# Vérification de l'installation d'Ollama
if ! command -v ollama &> /dev/null; then
    echo "Installation d'Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Vérification du modèle Mistral
if ! ollama list | grep -q "mistral:7b"; then
    echo "Téléchargement du modèle Mistral..."
    ollama pull mistral:7b
fi

# Démarrage d'Ollama en arrière-plan
ollama serve &

# Attente que Ollama soit prêt
echo "Attente du démarrage d'Ollama..."
until curl -s http://localhost:11434/api/version > /dev/null; do
    sleep 1
done

# Téléchargement des autres modèles
python download_models.py

# Démarrage de l'API
exec uvicorn main_api:app --host 0.0.0.0 --port 8000 
