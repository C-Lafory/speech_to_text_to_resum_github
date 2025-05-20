import logging
import whisper
import ffmpeg
import os
import gc
from typing import Optional
from config import WHISPER_MODEL_SIZE, WHISPER_MODEL_DIR

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

SUPPORTED_FORMATS = ['.mp3', '.wav', '.m4a', '.ogg', '.flac', '.qt']

def check_audio_format(file_path: str) -> bool:
    _, ext = os.path.splitext(file_path)
    return ext.lower() in SUPPORTED_FORMATS

def convert_to_wav(input_path: str, output_path: str):
    if not check_audio_format(input_path):
        raise ValueError(f"Format non supporté : {input_path}")
    ffmpeg.input(input_path).output(output_path, ar=16000, ac=1).run(overwrite_output=True)

def transcribe_audio(audio_path: str) -> str:
    model: Optional[whisper.Whisper] = None
    try:
        if not os.path.isfile(audio_path):
            raise FileNotFoundError(f"Fichier introuvable : {audio_path}")

        # Conversion
        wav_path = os.path.splitext(audio_path)[0] + "_converted.wav"
        convert_to_wav(audio_path, wav_path)

        # Chargement modèle
        model_file = WHISPER_MODEL_DIR / f"{WHISPER_MODEL_SIZE}.pt"
        if not model_file.exists():
            raise FileNotFoundError(f"Modèle Whisper introuvable : {model_file}")

        model = whisper.load_model(WHISPER_MODEL_SIZE, download_root=str(WHISPER_MODEL_DIR))

        # Transcription
        result = model.transcribe(wav_path, language="fr")
        return result["text"]

    finally:
        if model:
            del model
        gc.collect()
