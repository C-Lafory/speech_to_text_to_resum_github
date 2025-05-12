import os
import re
import sys
import logging
import ffmpeg
import gc
from typing import Any
from pydantic import BaseModel
from TTS.api import TTS
from num2words import num2words
from config import TTS_MODEL, TTS_MODEL_NAME, TTS_MODEL_DIR

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

def split_text_for_tts(text: str, max_length: int = MAX_TEXT_LENGTH) -> list[str]:
    if len(text) <= max_length:
        return [text]
    chunks, current_pos = [], 0
    while current_pos < len(text):
        end_pos = min(current_pos + max_length, len(text))
        last_break = max(text.rfind('.', current_pos, end_pos), text.rfind(',', current_pos, end_pos))
        if last_break != -1:
            end_pos = last_break + 1
        chunks.append(text[current_pos:end_pos].strip())
        current_pos = end_pos
    return chunks

def generate_audio(input_path: str, output_path: str):
    tts = None
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
        cleaned = convert_numbers_to_words(text)
        text_chunks = split_text_for_tts(cleaned)
        tts = TTS(model_path=TTS_MODEL_DIR).to("cpu")
        speaker = tts.speakers[0] if tts.speakers else None
        language = "fr" if "fr" in tts.languages else tts.languages[0]
        if not speaker:
            raise RuntimeError("Aucun locuteur disponible")
        temp_files = []
        for i, chunk in enumerate(text_chunks):
            temp = f"temp_chunk_{i}.wav"
            tts.tts_to_file(text=chunk, speaker=speaker, language=language, file_path=temp)
            temp_files.append(temp)
        if len(temp_files) > 1:
            inputs = [ffmpeg.input(f) for f in temp_files]
            ffmpeg.concat(*inputs, v=0, a=1).output(WAV_TEMP_FILE).run(overwrite_output=True)
        else:
            os.rename(temp_files[0], WAV_TEMP_FILE)
        convert_to_mp3(WAV_TEMP_FILE, output_path)
    finally:
        if tts:
            del tts
        gc.collect()
        for f in temp_files:
            if os.path.exists(f): os.remove(f)
        if os.path.exists(WAV_TEMP_FILE):
            os.remove(WAV_TEMP_FILE)

def main():
    if len(sys.argv) != 2:
        logging.error("Usage : python generate_audio.py <audio_id>")
        sys.exit(1)
    audio_id = sys.argv[1]
    input_file = f"./static/file/{audio_id}/resum.txt"
    output_file = f"./static/file/{audio_id}/audio_resume.mp3"
    try:
        generate_audio(input_file, output_file)
    except Exception as e:
        logging.error(f"Erreur audio : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
