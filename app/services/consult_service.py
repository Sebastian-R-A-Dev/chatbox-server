#consult service logic
import json
import faiss
import numpy as np
import re
from sentence_transformers import SentenceTransformer
import requests

# === CONFIG VARIABLES ===
CONTEXT_PATH = 'app/data/context.json'
OLLAMA_MODEL = 'llama2:latest'
OLLAMA_URL = 'http://localhost:11434/api/generate'

# === LOAD THE JSON ===
with open(CONTEXT_PATH, 'r', encoding='utf-8') as f:
    context_data = json.load(f)

# === PREPARE DATA ===
documents = []

# === Every disease is now a complete object ===
for disease in context_data['enfermedades']:
    text = f"Enfermedad: {disease['nombre']}\n"
    text += f"Descripción: {disease['descripcion']}\n"
    text += f"Síntomas: {', '.join(disease['sintomas'])}\n"
    text += f"Tratamientos: {', '.join(disease['tratamientos'])}\n"
    text += f"Acción inmediata: {disease['accion_inmediata']}"
    documents.append((disease['nombre'], text))

# === CREATE EMBEDDINGS ===
model_embedder = SentenceTransformer('all-MiniLM-L6-v2')  # Modelo pequeño y rápido
texts = [doc[1] for doc in documents]
embeddings = model_embedder.encode(texts)

# === CREATE THE FAISS INDEX ===
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))   

def extract_keywords(question):
    # Words of at least 4 letters, to ignore "the", "of", "my", etc.
    words = re.findall(r'\b\w{4,}\b', question.lower())
    return words

# === FUNCTION TO SEARCH FOR RELEVANT DISEASES ===
def search_context(question):
    key_words = extract_keywords(question)
    question_emb = model_embedder.encode([question])
    D, I = index.search(np.array(question_emb), k=5)  # Search up to 5 similar ones

    diseases_context = []
    for idx in I[0]:  # I[0] contains the k indices found
        disease_found, context_text = documents[idx]

        # Check if any of the symptoms contain the keywords
        if any(word in context_text.lower() for word in key_words):
            diseases_context.append((disease_found, context_text))

    return diseases_context


def consult_ollama(question, context, language):
    prompt = f"""
Eres un veterinario experto en enfermedades caninas.
Responde esta vez en **{language}** de forma clara, detallada y comprensible para cualquier dueño de perro.
Si la pregunta no está relacionada con perros o sus enfermedades, responde con una explicación de tu rol.

Utiliza el siguiente contexto para responder:

{context}

Pregunta del usuario: {question}
    """.strip()

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    if response.status_code == 200:
        return response.json()['response']
    else:
        raise Exception(f"Error consultando Ollama: {response.text}")
    

def analyze_question_with_context(user_question, language="español"):
    diseases_contexts = search_context(user_question)

    diseases = [disease for disease, _ in diseases_contexts]
    full_context = "\n\n".join([ctx for _, ctx in diseases_contexts]) if diseases_contexts else ""

    answer = consult_ollama(user_question, full_context, language)

    return {
        "diseases": diseases,
        "answer": answer,
        "question": user_question
    }
