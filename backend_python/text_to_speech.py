import os
import re
import sys
import logging
import ffmpeg
import gc
from typing import List
from TTS.api import TTS
from num2words import num2words
from config import TTS_MODEL_NAME

# Configuration des logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Constantes
WAV_TEMP_FILE = "output.wav"
MAX_TEXT_LENGTH = 5000  # Longueur maximale d’un morceau de texte

def convert_numbers_to_words(text: str, lang: str = "fr") -> str:
    """Remplace les chiffres par des mots pour une meilleure synthèse vocale"""
    def replace_number(match):
        return num2words(match.group(), lang=lang)

    text = re.sub(r'\d+', replace_number, text)
    return text.replace("km²", " kilomètres carrés") \
               .replace("m²", " mètres carrés") \
               .replace("%", " pour cent")

def convert_to_mp3(input_wav: str, output_mp3: str):
    """Convertit un fichier WAV en MP3 avec ffmpeg"""
    try:
        ffmpeg.input(input_wav).output(output_mp3, format="mp3", acodec="libmp3lame", audio_bitrate="192k").run(overwrite_output=True)
        logging.info(f"✅ Audio converti : {output_mp3}")
    except Exception as e:
        logging.error(f"❌ Erreur de conversion audio : {e}")
        raise

def split_text_for_tts(text: str, max_length: int = MAX_TEXT_LENGTH) -> List[str]:
    """Divise le texte en morceaux compatibles avec le modèle TTS"""
    if len(text) <= max_length:
        return [text]

    chunks = []
    current_pos = 0

    while current_pos < len(text):
        end_pos = min(current_pos + max_length, len(text))
        last_break = max(text.rfind('.', current_pos, end_pos), text.rfind(',', current_pos, end_pos))
        if last_break != -1:
            end_pos = last_break + 1
        chunks.append(text[current_pos:end_pos].strip())
        current_pos = end_pos

    return chunks

def generate_audio(input_path: str, output_path: str):
    """Génère un fichier audio MP3 à partir du texte d’un résumé"""
    tts = None
    temp_files = []

    try:
        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"Fichier introuvable : {input_path}")

        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        cleaned_text = convert_numbers_to_words(text)
        text_chunks = split_text_for_tts(cleaned_text)
        logging.info(f"📄 {len(text_chunks)} morceau(x) à synthétiser...")

        # Chargement du modèle TTS depuis le cache local
        tts = TTS(model_name=TTS_MODEL_NAME).to("cpu")

        speaker = tts.speakers[0] if tts.speakers else None
        language = "fr" if "fr" in tts.languages else tts.languages[0]

        if not speaker:
            raise RuntimeError("Aucun locuteur disponible pour ce modèle.")

        # Synthèse de chaque morceau de texte
        for i, chunk in enumerate(text_chunks):
            temp_wav = f"temp_chunk_{i}.wav"
            logging.info(f"🎙️ Synthèse du morceau {i+1}/{len(text_chunks)}...")
            tts.tts_to_file(text=chunk, speaker=speaker, language=language, file_path=temp_wav)
            temp_files.append(temp_wav)

        # Concaténation WAV
        if len(temp_files) > 1:
            logging.info("🔄 Concaténation des fichiers audio...")
            inputs = [ffmpeg.input(f) for f in temp_files]
            ffmpeg.concat(*inputs, v=0, a=1).output(WAV_TEMP_FILE).run(overwrite_output=True)
        else:
            os.rename(temp_files[0], WAV_TEMP_FILE)

        # Conversion finale en MP3
        convert_to_mp3(WAV_TEMP_FILE, output_path)
        logging.info(f"✅ Fichier audio généré : {output_path}")

    except Exception as e:
        logging.error(f"❌ Erreur lors de la génération audio : {e}")
        raise RuntimeError("Erreur avec TTS. Vérifiez que le modèle est bien installé via download_models.py")

    finally:
        # Nettoyage mémoire et fichiers temporaires
        if tts:
            del tts
        gc.collect()
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        if os.path.exists(WAV_TEMP_FILE):
            os.remove(WAV_TEMP_FILE)

def main():
    if len(sys.argv) != 2:
        logging.error("❌ Utilisation : python generate_audio.py <audio_id>")
        sys.exit(1)

    audio_id = sys.argv[1]
    input_file = f"./static/file/{audio_id}/resum.txt"
    output_file = f"./static/file/{audio_id}/audio_resume.mp3"

    try:
        generate_audio(input_file, output_file)
        sys.exit(0)
    except FileNotFoundError as e:
        logging.error(str(e))
        sys.exit(2)
    except Exception as e:
        logging.error(f"🚨 Erreur inattendue : {e}")
        sys.exit(3)

if __name__ == "__main__":
    main()
