import logging
import spacy
import ollama
import gc
from config import SPACY_MODEL_NAME

# Configuration logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Chargement du modèle spaCy
try:
    nlp = spacy.load(SPACY_MODEL_NAME)
except Exception as e:
    logging.error(f"❌ Erreur chargement modèle spaCy ({SPACY_MODEL_NAME}) : {e}")
    raise RuntimeError("Erreur de chargement spaCy")

# Constantes
MIN_CHUNK_SIZE = 512
MAX_CHUNK_SIZE = 2048

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
        raise RuntimeError("Vérifie que Mistral est bien installé et lancé via Ollama")

def summarize_text(text: str) -> str:
    """Fonction à importer dans FastAPI : prend un texte brut, retourne le résumé complet"""
    if count_tokens(text) < 500:
        return text

    chunks = split_text(text)
    summaries = []
    for i, chunk in enumerate(chunks):
        try:
            logging.info(f"📝 Résumé chunk {i+1}/{len(chunks)}")
            summaries.append(summarize_chunk(chunk))
            gc.collect()
        except Exception as e:
            logging.error(f"⚠️ Chunk {i+1} échoué : {e}")
    return "\n".join(summaries)
