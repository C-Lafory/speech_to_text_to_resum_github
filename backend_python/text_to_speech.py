# resum_audio.py
import os
import re
import logging
import ffmpeg
import gc
from typing import List
from TTS.api import TTS
from num2words import num2words
from config import TTS_MODEL_NAME

# Logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

WAV_TEMP_FILE = "output.wav"
MAX_TEXT_LENGTH = 5000

def convert_numbers_to_words(text: str, lang: str = "fr") -> str:
    def replace_number(match):
        return num2words(match.group(), lang=lang)
    text = re.sub(r'\d+', replace_number, text)
    return text.replace("km²", " kilomètres carrés").replace("m²", " mètres carrés").replace("%", " pour cent")

def convert_to_mp3(input_wav: str, output_mp3: str):
    ffmpeg.input(input_wav).output(output_mp3, format="mp3", acodec="libmp3lame", audio_bitrate="192k").run(overwrite_output=True)

def split_text_for_tts(text: str, max_length: int = MAX_TEXT_LENGTH) -> List[str]:
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

def text_to_speech(text: str, output_path: str):
    """Génère un fichier audio MP3 à partir du texte d'un résumé"""
    tts = None
    temp_files = []

    try:
        cleaned_text = convert_numbers_to_words(text)
        text_chunks = split_text_for_tts(cleaned_text)
        logging.info(f"📄 {len(text_chunks)} morceau(x) à synthétiser...")

        # Vérification du modèle
        if not TTS_MODEL_NAME.startswith("tts_models/fr/"):
            raise RuntimeError(f"Le modèle {TTS_MODEL_NAME} n'est pas un modèle français")

        # Initialisation du modèle
        tts = TTS(model_name=TTS_MODEL_NAME, progress_bar=False).to("cpu")
        
        # Vérification des langues disponibles
        if not hasattr(tts, 'languages') or not tts.languages:
            raise RuntimeError("Le modèle TTS n'a pas de langues configurées")
        
        if "fr" not in tts.languages:
            raise RuntimeError(f"Le modèle {TTS_MODEL_NAME} ne supporte pas le français")
        
        # Vérification des locuteurs
        if not hasattr(tts, 'speakers') or not tts.speakers:
            raise RuntimeError("Le modèle TTS n'a pas de locuteurs configurés")
        
        # Synthèse de chaque chunk
        for i, chunk in enumerate(text_chunks):
            temp_wav = f"temp_chunk_{i}.wav"
            logging.info(f"🎙️ Synthèse {i+1}/{len(text_chunks)}...")
            tts.tts_to_file(text=chunk, speaker=tts.speakers[0], language="fr", file_path=temp_wav)
            temp_files.append(temp_wav)

        # Concat
        if len(temp_files) > 1:
            logging.info("🔄 Concaténation des audios...")
            inputs = [ffmpeg.input(f) for f in temp_files]
            ffmpeg.concat(*inputs, v=0, a=1).output(WAV_TEMP_FILE).run(overwrite_output=True)
        else:
            os.rename(temp_files[0], WAV_TEMP_FILE)

        # Conversion finale
        convert_to_mp3(WAV_TEMP_FILE, output_path)
        logging.info(f"✅ Audio final : {output_path}")

    except Exception as e:
        logging.error(f"❌ Erreur TTS : {e}")
        raise RuntimeError(f"Erreur TTS : {str(e)}")

    finally:
        if tts:
            del tts
        gc.collect()
        for f in temp_files:
            if os.path.exists(f):
                os.remove(f)
        if os.path.exists(WAV_TEMP_FILE):
            os.remove(WAV_TEMP_FILE)
