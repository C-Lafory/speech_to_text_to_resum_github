import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from transcription import transcribe_audio
from resume import summarize_file

app = FastAPI()

AUDIO_UPLOAD_DIR = "static/upload/audio"
TEXT_OUTPUT_PATH = "static/file/transcription.txt"
SUMMARY_OUTPUT_PATH = "static/file/resum.txt"

@app.post("/api/audio")
async def process_audio(file: UploadFile = File(...)):
    # Sauvegarde du fichier uploadé
    audio_path = os.path.join(AUDIO_UPLOAD_DIR, file.filename)
    with open(audio_path, "wb") as f:
        f.write(await file.read())

    # Transcription
    transcription = transcribe_audio(audio_path)
    with open(TEXT_OUTPUT_PATH, "w") as f:
        f.write(transcription)

    # Résumé à partir du fichier de transcription
    summarize_file(TEXT_OUTPUT_PATH, SUMMARY_OUTPUT_PATH)

    return FileResponse(SUMMARY_OUTPUT_PATH, media_type="text/plain")
