import os
import sys
import logging
import spacy
import ollama
import gc
from download_models import SPACY_MODEL

# Configuration des chemins
BASE_DIR = "static/file"
RESUME_FILENAME = "resum.txt"
TRANSCRIPTION_FILENAME = "transcription.txt"
MIN_CHUNK_SIZE = 512
MAX_CHUNK_SIZE = 2048
TARGET_CHUNK_SIZE = 1024

# Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Initialiser Spacy avec le modèle préchargé
try:
    nlp = spacy.load(SPACY_MODEL)
except OSError:
    logging.error(f"❌ Modèle Spacy ({SPACY_MODEL}) non trouvé. Exécutez d'abord download_models.py")
    sys.exit(1)

def count_tokens(text: str) -> int:
    return len(nlp(text))

def calculate_optimal_chunk_size(text: str) -> int:
    """Calcule la taille optimale des chunks en fonction de la longueur du texte"""
    total_tokens = count_tokens(text)
    if total_tokens < MIN_CHUNK_SIZE:
        return total_tokens
    elif total_tokens > MAX_CHUNK_SIZE * 10:  # Pour les très longs textes
        return MAX_CHUNK_SIZE
    else:
        return min(max(MIN_CHUNK_SIZE, total_tokens // 10), MAX_CHUNK_SIZE)

def split_text(text: str) -> list[str]:
    """Divise le texte en chunks de taille optimale"""
    chunk_size = calculate_optimal_chunk_size(text)
    sections = []
    start = 0
    
    while start < len(text):
        end = min(start + chunk_size, len(text))
        # Chercher le dernier point ou la dernière virgule dans la fenêtre
        last_dot = text.rfind('.', start, end)
        last_comma = text.rfind(',', start, end)
        last_break = max(last_dot, last_comma)
        
        if last_break != -1:
            end = last_break + 1
        sections.append(text[start:end].strip())
        start = end
    
    return sections

def summarize_chunk(chunk: str) -> str:
    try:
        response = ollama.chat(model="mistral:7b", messages=[
            {"role": "system", "content": "Tu es un expert en résumé de texte en français."},
            {"role": "user", "content": (
                "Fais un résumé détaillé de ce texte en incluant toutes les informations importantes, "
                "y compris les noms propres, dates, chiffres et mots-clés. Le résumé doit faire environ 25% du texte original "
                f"et il doit être en français : {chunk}"
            )}
        ])
        return response.get("message", {}).get("content", "")
    except Exception as e:
        logging.error(f"❌ Erreur lors de l'utilisation d'Ollama : {e}")
        raise RuntimeError("Erreur avec Ollama. Vérifiez que le modèle mistral:7b est bien installé via download_models.py")

def summarize_file(input_path: str, output_path: str):
    logging.info(f"📄 Lecture de {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    token_count = count_tokens(text)
    logging.info(f"📊 {token_count} tokens détectés.")

    if token_count < 500:
        logging.info("🔹 Texte trop court, pas de résumé généré.")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        return

    chunks = split_text(text)
    logging.info(f"🧩 {len(chunks)} morceaux à résumer")

    summaries = []
    for idx, chunk in enumerate(chunks):
        try:
            logging.info(f"📝 Résumé du chunk {idx + 1}/{len(chunks)}")
            summary = summarize_chunk(chunk)
            summaries.append(summary)
            # Nettoyage de la mémoire après chaque chunk
            gc.collect()
        except Exception as e:
            logging.error(f"❌ Échec du résumé du chunk {idx + 1} : {e}")

    final_summary = "\n".join(summaries)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_summary)
    logging.info(f"✅ Résumé généré dans {output_path}")

def main():
    if len(sys.argv) != 2:
        logging.error("❌ Usage : python summarizer.py <user_id>")
        sys.exit(1)

    user_id = sys.argv[1]
    user_dir = os.path.join(BASE_DIR, user_id)
    input_file = os.path.join(user_dir, TRANSCRIPTION_FILENAME)
    output_file = os.path.join(user_dir, RESUME_FILENAME)

    if not os.path.isfile(input_file):
        logging.error(f"❌ Fichier de transcription introuvable : {input_file}")
        sys.exit(2)

    try:
        summarize_file(input_file, output_file)
    except Exception as e:
        logging.error(f"🚨 Erreur lors du résumé : {e}")
        sys.exit(3)

if __name__ == "__main__":
    main()
