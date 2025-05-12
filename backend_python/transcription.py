import os
import sys
import logging
import whisper
import ffmpeg
import gc
from typing import Dict, Any, Optional
from pydantic import BaseModel
from config import WHISPER_MODEL_SIZE, WHISPER_MODEL_DIR

# Configuration
AUDIO_UPLOAD_DIR = "static/upload/audio"
OUTPUT_BASE_DIR = "static/file"
SUPPORTED_FORMATS = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def check_audio_format(file_path: str) -> bool:
    """Vérifie si le format audio est supporté"""
    _, ext = os.path.splitext(file_path)
    return ext.lower() in SUPPORTED_FORMATS

def convert_to_wav(input_path: str, output_path: str):
    """Convertir un fichier audio en WAV (mono, 16kHz)."""
    try:
        if not check_audio_format(input_path):
            raise ValueError(f"Format audio non supporté. Formats acceptés : {', '.join(SUPPORTED_FORMATS)}")
            
        logging.info(f"🎧 Conversion en cours : {input_path} → {output_path}")
        ffmpeg.input(input_path).output(output_path, ar=16000, ac=1).run(overwrite_output=True)
        logging.info("✅ Conversion réussie.")
    except Exception as e:
        logging.error(f"❌ Erreur de conversion : {e}")
        raise

def transcribe_audio(audio_id: str, audio_ext: str) -> str:
    """Transcrire un fichier audio avec Whisper et sauvegarder le texte."""
    model = None
    try:
        # Chemins dynamiques
        input_audio_path = os.path.join(AUDIO_UPLOAD_DIR, f"{audio_id}.{audio_ext}")
        output_dir = os.path.join(OUTPUT_BASE_DIR, audio_id)
        os.makedirs(output_dir, exist_ok=True)
        wav_output_path = os.path.join(output_dir, f"{audio_id}.wav")
        transcription_output_path = os.path.join(output_dir, "transcription.txt")

        # Vérification du fichier source
        if not os.path.isfile(input_audio_path):
            raise FileNotFoundError(f"❌ Fichier introuvable : {input_audio_path}")

        # Vérification que le modèle Whisper est bien présent localement
        if not WHISPER_MODEL_DIR.exists():
            raise FileNotFoundError(f"❌ Dossier du modèle Whisper introuvable à {WHISPER_MODEL_DIR}. Exécutez d'abord download_models.py")

        # Étape 1 : conversion en WAV
        convert_to_wav(input_audio_path, wav_output_path)

        # Étape 2 : chargement du modèle local
        logging.info(f"🧠 Chargement de Whisper ({WHISPER_MODEL_SIZE}) depuis {WHISPER_MODEL_DIR}...")
        model = whisper.load_model(WHISPER_MODEL_SIZE, download_root=str(WHISPER_MODEL_DIR))

        # Étape 3 : transcription
        logging.info(f"✍️ Transcription en cours de {wav_output_path}...")
        result = model.transcribe(wav_output_path, language="fr")

        with open(transcription_output_path, "w", encoding="utf-8") as f:
            f.write(result["text"])

        logging.info(f"✅ Transcription enregistrée : {transcription_output_path}")
        return transcription_output_path

    finally:
        # Nettoyage mémoire
        if model is not None:
            del model
            gc.collect()

def main():
    if len(sys.argv) != 3:
        logging.error("❌ Utilisation : python transcription.py <audio_id> <extension>")
        sys.exit(1)

    audio_id, audio_ext = sys.argv[1], sys.argv[2]

    try:
        path = transcribe_audio(audio_id, audio_ext)
        logging.info(f"✅ Terminé. Résultat dans : {path}")
        sys.exit(0)
    except FileNotFoundError as e:
        logging.error(str(e))
        sys.exit(2)
    except ValueError as e:
        logging.error(str(e))
        sys.exit(3)
    except Exception as e:
        logging.error(f"🚨 Une erreur inattendue est survenue : {e}")
        sys.exit(4)

if __name__ == "__main__":
    main()
