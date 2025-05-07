# 🎙️ Audio Transcription, Résumé & Synthèse Vocale

Ce projet permet de :

✅ Transcrire automatiquement un fichier audio (.wav, .mp3, .m4a...)  
✅ Résumer le texte transcrit via un modèle Mistral (local avec Ollama)  
✅ Générer un fichier audio à partir du résumé  

---

## 🚀 Installation

### 1️⃣ Cloner le projet

```bash
git clone https://github.com/your-repo.git
cd your-repo

2️⃣ Créer un environnement virtuel
Environnement Python 3.12 – Transcription & Résumé

python3.12 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

Installer les dépendances principales :

pip install -r requirement_3.12.txt

Environnement Python 3.10 – Synthèse vocale

    À créer séparément si nécessaire sur votre machine ou via Docker

python3.10 -m venv venv_audio
source venv_audio/bin/activate
pip install -r requirement_3.10.txt

🧠 Environnements Python
🧾 Python 3.12 – Transcription & Résumé

    Scripts utilisés :

        transcription.py : transcrit un fichier audio en texte avec Whisper

        resum.py : résume le texte avec le modèle mistral:7b via Ollama

    Fichiers générés :

        transcription.txt : texte complet issu de l’audio

        resum.txt : résumé du texte transcrit

    Dépendances (requirement_3.12.txt) :

        whisper, ffmpeg-python, spacy, fr_core_news_sm, ollama

🔊 Python 3.10 – Synthèse vocale à partir du résumé

    Script utilisé :

        text_to_speech.py : lit le fichier resum.txt et génère un fichier .mp3

    Dépendances (requirement_3.10.txt) :

        TTS : synthèse vocale multilingue

        num2words : conversion de nombres en lettres

        ffmpeg-python : traitement et conversion audio

⚙️ Environnement de Développement Local

Un fichier requirements-dev.txt permet d’assurer un code propre, lisible et maintenable :

black
flake8
mypy
isort
pre-commit

✨ À quoi servent ces outils ?
Outil	Rôle
black	Formatte automatiquement ton code selon la PEP8
flake8	Détecte les erreurs de style et bugs potentiels
isort	Trie les imports dans le bon ordre
mypy	Vérifie les types si tu utilises des annotations
pre-commit	Automatise le lancement des outils avant chaque commit


▶️ Installation

pip install -r requirements-dev.txt

⚙️ Pre-commit : configuration automatique

Crée un fichier .pre-commit-config.yaml à la racine :

repos:
  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black

  - repo: https://github.com/pre-commit/mirrors-flake8
    rev: v7.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-isort
    rev: v5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy

Puis installe le hook :

pre-commit install

Test :

git add .
git commit -m "Test hooks"

Tous les outils seront automatiquement exécutés avant le commit ✅

💡 Intégration dans VSCode (optionnel mais recommandé)

Ajoute ce fichier .vscode/settings.json :

{
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "python.linting.flake8Enabled": true,
  "python.linting.enabled": true,
  "python.linting.mypyEnabled": true,
  "python.sortImports.args": ["--profile", "black"]
}

🐳 Docker & Production

Le projet est pensé pour être utilisé dans un environnement Docker (avec un Dockerfile principal dans le dépôt API_déploiement).
Deux images sont générées :

    Une pour les scripts Python (transcription, résumé, TTS)

    Une pour l’API Go (API_skynet)

Remarque : Le fichier requirements-dev.txt est destiné uniquement au développement local et ne doit pas être installé dans les images Docker utilisées en production.
📜 Licence

MIT – open source, réutilisable comme bon vous semble.

