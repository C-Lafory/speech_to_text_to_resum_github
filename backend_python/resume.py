import os
import sys
import logging
import spacy
import ollama
import gc
from config import SPACY_MODEL_NAME

# Chemins et fichiers
BASE_DIR = "static/file"
RESUME_FILENAME = "resum.txt"
TRANSCRIPTION_FILENAME = "transcription.txt"
MIN_CHUNK_SIZE = 512
MAX_CHUNK_SIZE = 2048

# Configuration des logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Chargement du modèle spaCy depuis le cache local (pas de chemin personnalisé ici)
try:
    nlp = spacy.load(SPACY_MODEL_NAME)
except Exception as e:
    logging.error(f"❌ Erreur chargement modèle spaCy ({SPACY_MODEL_NAME}) : {e}")
    sys.exit(1)

def count_tokens(text: str) -> int:
    return len(nlp(text))

def calculate_optimal_chunk_size(text: str) -> int:
    total_tokens = count_tokens(text)
    if total_tokens < MIN_CHUNK_SIZE:
        return total_tokens
    elif total_tokens > MAX_CHUNK_SIZE * 10:
        return MAX_CHUNK_SIZE
    else:
        return min(max(MIN_CHUNK_SIZE, total_tokens // 10), MAX_CHUNK_SIZE)

def split_text(text: str) -> list[str]:
    chunk_size = calculate_optimal_chunk_size(text)
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
        logging.error(f"❌ Erreur Ollama : {e}")
        raise RuntimeError("Vérifie que Mistral est bien installé dans Ollama")

def summarize_file(input_path: str, output_path: str):
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    if count_tokens(text) < 500:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        return

    chunks = split_text(text)
    summaries = []
    for i, chunk in enumerate(chunks):
        try:
            logging.info(f"📝 Résumé chunk {i+1}/{len(chunks)}")
            summaries.append(summarize_chunk(chunk))
            gc.collect()
        except Exception as e:
            logging.error(f"⚠️ Chunk {i+1} échoué : {e}")

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

    try:
        summarize_file(input_file, output_file)
    except Exception as e:
        logging.error(f"Erreur lors du résumé : {e}")
        sys.exit(3)

if __name__ == "__main__":
    main()
