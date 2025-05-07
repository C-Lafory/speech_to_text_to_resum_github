import os
import logging
import subprocess
import shutil

# Configuration
MODEL_DIR = "models"
WHISPER_MODEL_SIZE = "medium"
SPACY_MODEL = "fr_core_news_sm"
TTS_MODEL = "tts_models/multilingual/multi-dataset/your_tts"
MIN_DISK_SPACE_GB = 10  # Espace disque minimum requis en GB

# Déterminer quel service exécute le script
IS_TTS_SERVICE = os.path.exists("text_to_speech.py")
IS_MAIN_SERVICE = os.path.exists("transcription.py")

# Importer les modules en fonction du service
if IS_MAIN_SERVICE:
    import whisper
    import spacy
if IS_TTS_SERVICE:
    from TTS.api import TTS

def check_disk_space():
    """Vérifie l'espace disque disponible"""
    total, used, free = shutil.disk_usage("/")
    free_gb = free // (2**30)  # Conversion en GB
    if free_gb < MIN_DISK_SPACE_GB:
        raise RuntimeError(f"❌ Espace disque insuffisant. {free_gb}GB disponible, {MIN_DISK_SPACE_GB}GB requis.")

def verify_models():
    """Vérifie si tous les modèles sont présents"""
    models_status = {
        "whisper": False,
        "spacy": False,
        "tts": False,
        "ollama": False,
        "mistral": False
    }
    
    # Vérification Whisper (uniquement pour le service principal)
    if IS_MAIN_SERVICE:
        whisper_model_path = os.path.join(MODEL_DIR, WHISPER_MODEL_SIZE + ".pt")
        models_status["whisper"] = os.path.isfile(whisper_model_path)
        
        # Vérification Spacy
        try:
            spacy.load(SPACY_MODEL)
            models_status["spacy"] = True
        except OSError:
            pass
    
    # Vérification TTS (uniquement pour le service TTS)
    if IS_TTS_SERVICE:
        try:
            TTS(model_name=TTS_MODEL, progress_bar=False)
            models_status["tts"] = True
        except Exception:
            pass
    
    # Vérification Ollama (uniquement pour le service principal)
    if IS_MAIN_SERVICE:
        try:
            subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            models_status["ollama"] = True
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass
        
        # Vérification Mistral
        if models_status["ollama"]:
            try:
                subprocess.run(["ollama", "list"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                models_status["mistral"] = "mistral:7b" in subprocess.run(["ollama", "list"], capture_output=True, text=True).stdout
            except subprocess.CalledProcessError:
                pass
    
    return models_status

def download_models():
    """Télécharge tous les modèles nécessaires et crée le dossier si nécessaire."""
    # Vérification de l'espace disque
    check_disk_space()
    
    # Créer le dossier des modèles s'il n'existe pas
    if not os.path.exists(MODEL_DIR):
        logging.info(f"📁 Création du dossier des modèles : {MODEL_DIR}")
        os.makedirs(MODEL_DIR, exist_ok=True)

    # 1. Vérification et téléchargement du modèle Whisper (uniquement pour le service principal)
    if IS_MAIN_SERVICE:
        logging.info(f"🔍 Vérification du modèle Whisper ({WHISPER_MODEL_SIZE})...")
        whisper_model_path = os.path.join(MODEL_DIR, WHISPER_MODEL_SIZE + ".pt")
        if not os.path.isfile(whisper_model_path):
            logging.info(f"⬇️ Téléchargement du modèle Whisper ({WHISPER_MODEL_SIZE})...")
            whisper.load_model(WHISPER_MODEL_SIZE, download_root=MODEL_DIR)
            logging.info(f"✅ Modèle Whisper téléchargé dans {MODEL_DIR}")
        else:
            logging.info(f"✅ Modèle Whisper déjà présent : {whisper_model_path}")

        # 2. Vérification et téléchargement du modèle Spacy
        logging.info(f"🔍 Vérification du modèle Spacy ({SPACY_MODEL})...")
        try:
            spacy.load(SPACY_MODEL)
            logging.info(f"✅ Modèle Spacy déjà présent")
        except OSError:
            logging.info(f"⬇️ Téléchargement du modèle Spacy ({SPACY_MODEL})...")
            spacy.cli.download(SPACY_MODEL)
            logging.info(f"✅ Modèle Spacy téléchargé")

    # 3. Vérification et téléchargement du modèle TTS (uniquement pour le service TTS)
    if IS_TTS_SERVICE:
        logging.info(f"🔍 Vérification du modèle TTS ({TTS_MODEL})...")
        try:
            tts = TTS(model_name=TTS_MODEL, progress_bar=False)
            if tts.speakers and len(tts.speakers) > 0:
                logging.info(f"✅ Modèle TTS déjà présent et fonctionnel")
            else:
                raise RuntimeError("Modèle TTS présent mais pas de locuteurs disponibles")
        except Exception as e:
            logging.info(f"⬇️ Téléchargement du modèle TTS ({TTS_MODEL})...")
            tts = TTS(model_name=TTS_MODEL, progress_bar=True)
            if not tts.speakers or len(tts.speakers) == 0:
                raise RuntimeError("Modèle TTS téléchargé mais pas de locuteurs disponibles")
            logging.info(f"✅ Modèle TTS téléchargé")

    # 4. Vérification et installation du client Ollama (uniquement pour le service principal)
    if IS_MAIN_SERVICE:
        logging.info("🔍 Vérification du client Ollama...")
        try:
            subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logging.info("✅ Client Ollama déjà installé.")
        except (FileNotFoundError, subprocess.CalledProcessError):
            logging.info("⬇️ Installation du client Ollama...")
            try:
                # Vérifier si curl est installé
                subprocess.run(["curl", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except (FileNotFoundError, subprocess.CalledProcessError):
                logging.info("⬇️ Installation de curl...")
                subprocess.run(["apt-get", "update"], check=True)
                subprocess.run(["apt-get", "install", "-y", "curl"], check=True)
            
            try:
                install_command = "curl -fsSL https://ollama.com/install.sh | sh"
                result = subprocess.run(install_command, shell=True, capture_output=True, text=True)
                if result.returncode != 0:
                    raise RuntimeError(f"Échec de l'installation d'Ollama: {result.stderr}")
                logging.info("✅ Client Ollama installé avec succès.")
            except Exception as e:
                logging.error(f"❌ Échec de l'installation du client Ollama : {e}")
                logging.warning("⚠️ Ollama n'est pas installé. Le résumé ne sera pas disponible.")
                return  # On continue sans Ollama

        # 5. Vérification du modèle Mistral via Ollama
        logging.info("🔍 Vérification du modèle Mistral via Ollama...")
        try:
            subprocess.run(["ollama", "pull", "mistral:7b"], check=True)
            logging.info("✅ Modèle Mistral vérifié/installé via Ollama")
        except Exception as e:
            logging.error(f"❌ Erreur lors de la vérification du modèle Mistral : {e}")
            logging.warning("⚠️ Le modèle Mistral n'est pas disponible. Le résumé ne sera pas disponible.")
            return  # On continue sans Mistral

    # Vérification finale
    models_status = verify_models()
    if all(models_status.values()):
        logging.info("✅ Tous les modèles sont correctement installés et fonctionnels")
    else:
        missing_models = [model for model, status in models_status.items() if not status]
        logging.warning(f"⚠️ Certains modèles ne sont pas correctement installés : {', '.join(missing_models)}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    download_models()
    