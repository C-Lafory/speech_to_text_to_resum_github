import os
import sys
import logging
import spacy
import ollama
import gc
from config import SPACY_MODEL_NAME

BASE_DIR = "static/file"
RESUME_FILENAME = "resum.txt"
TRANSCRIPTION_FILENAME = "transcription.txt"
MIN_CHUNK_SIZE = 512
MAX_CHUNK_SIZE = 2048

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

try:
    nlp = spacy.load(SPACY_MODEL_NAME)
except Exception as e:
    logging.error(f"❌ spaCy non trouvé : {e}")
    sys.exit(1)

def count_tokens(text: str) -> int:
    return len(nlp(text))

def split_text(text: str) -> list[str]:
    chunk_size = min(max(MIN_CHUNK_SIZE, len(text) // 10), MAX_CHUNK_SIZE)
    sections, start = [], 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        last_break = max(text.rfind('.', start, end), text.rfind(',', start, end))
        if last_break != -1:
            end = last_break + 1
        sections.append(text[start:end].strip())
        start = end
    return sections

def summarize_chunk(chunk: str) -> str:
    try:
        response = ollama.chat(model="mistral:7b", messages=[
            {"role": "system", "content": "Tu es un expert en résumé de texte en français."},
            {"role": "user", "content": f"Fais un résumé en 25 % du texte suivant : {chunk}"}
        ])
        return response.get("message", {}).get("content", "")
    except Exception as e:
        logging.error(f"Erreur Ollama : {e}")
        return ""

def summarize_file(input_path: str, output_path: str):
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    if count_tokens(text) < 500:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        return
    summaries = [summarize_chunk(chunk) for chunk in split_text(text)]
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(summaries))

def main():
    if len(sys.argv) != 2:
        logging.error("Usage : python resume.py <user_id>")
        sys.exit(1)
    user_id = sys.argv[1]
    input_file = os.path.join(BASE_DIR, user_id, TRANSCRIPTION_FILENAME)
    output_file = os.path.join(BASE_DIR, user_id, RESUME_FILENAME)
    if not os.path.isfile(input_file):
        logging.error(f"Fichier introuvable : {input_file}")
        sys.exit(2)
    summarize_file(input_file, output_file)

if __name__ == "__main__":
    main()
