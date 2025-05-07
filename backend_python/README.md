📁 README.md - Projet de Transcription, Résumé & Synthèse Vocale

Ce projet est organisé en deux environnements Python distincts, chacun dédié à une partie spécifique du pipeline de traitement :

Python 3.12 : Transcription et Résumé de texte

Python 3.10 : Synthèse vocale à partir du résumé (génération audio)

Un environnement de développement local (optionnel) est aussi proposé pour travailler efficacement avec VSCode.

🧠 1. Transcription & Résumé (Python 3.12)

📄 Fichier : requirement_3.12.txt

📦 Dépendances principales :

Package

Utilité

spacy

Tokenisation & découpage du texte

fr_core_news_sm

Modèle linguistique français pour spaCy

ollama

Appel au modèle mistral:7b pour résumer les textes

🔁 Fonctionnement :

Transcription écrite dans transcription.txt

Résumé généré et sauvegardé dans resum.txt

🔊 2. Synthèse Vocale du Résumé (Python 3.10)

📄 Fichier : requirement_3.10.txt

📦 Dépendances principales :

Package

Utilité

TTS

Synthèse vocale multilingue

num2words

Conversion des chiffres en lettres (ex : 2024 → deux mille vingt-quatre)

ffmpeg-python

Conversion audio (WAV → MP3 par exemple)

🔁 Fonctionnement :

Lecture de resum.txt

Génération d'un fichier audio .mp3

🛠️ 3. Développement local (optionnel)

📄 Fichier : requirements-dev.txt

📦 Dépendances :

Package

Utilité

black

Formatage automatique du code

flake8

Analyse de code (linting)

mypy

Vérification statique des types (si annotations)

pytest

Lancement de tests unitaires (si besoin)

⚙️ Intégration avec VSCode :

Crée un fichier .vscode/settings.json avec :

{
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "python.linting.flake8Enabled": true,
  "python.linting.enabled": true,
  "python.linting.mypyEnabled": true,
  "python.testing.pytestEnabled": true
}

Cela permet :

Formatage du code auto à l'enregistrement

Analyse de code continue

Tests unitaires en local (optionnel)

🐳 Docker & Déploiement

Si tu utilises Docker, installe seulement requirement_3.12.txt ou requirement_3.10.txt selon l’image cible. requirements-dev.txt n'est pas requis en production.


il faut installer : sudo apt update & sudo apt install ffmpeg

pour tester les modèles en local il faut lancer la fonction "download_models" dans le fichier qui porte le même nom

faire attention à ce que curl soit bien installé sinon faire la commande : "sudo apt install curl"
