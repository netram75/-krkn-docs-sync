import glob
import os

import faiss
import numpy as np
from google import genai
from sentence_transformers import SentenceTransformer

from diff_parser import ScenarioChange

_MODEL = "gemini-2.5-flash-lite"
_EMBED_MODEL = "all-MiniLM-L6-v2"
_CORPUS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "rag_corpus")


def _load_corpus() -> list[str]:
    paths = sorted(glob.glob(os.path.join(_CORPUS_DIR, "*.md")))
    return [open(p, encoding="utf-8").read() for p in paths]


def _find_similar(query: str, texts: list[str], top_k: int = 2) -> list[str]:
    embedder = SentenceTransformer(_EMBED_MODEL)
    corpus_embeddings = embedder.encode(texts, convert_to_numpy=True).astype(np.float32)
    query_embedding = embedder.encode([query], convert_to_numpy=True).astype(np.float32)

    index = faiss.IndexFlatL2(corpus_embeddings.shape[1])
    index.add(corpus_embeddings)
    _, indices = index.search(query_embedding, min(top_k, len(texts)))

    return [texts[i] for i in indices[0]]


def generate_doc(change: ScenarioChange) -> str:
    corpus = _load_corpus()
    query = f"{change.file_path} {' '.join(change.classes)} {' '.join(change.functions[:5])}"
    examples = _find_similar(query, corpus)

    examples_block = "\n\n---example---\n\n".join(examples)

    prompt = (
        "You are generating Hugo documentation for a new krkn-chaos scenario.\n"
        "Match the style, structure, and frontmatter format of these existing docs exactly:\n\n"
        f"{examples_block}\n\n"
        "---\n\n"
        "Generate _index.md for this new scenario:\n\n"
        f"File: {change.file_path}\n"
        f"Classes: {', '.join(change.classes)}\n"
        f"Functions: {', '.join(change.functions[:8])}\n\n"
        f"Source:\n{change.source[:3000]}\n\n"
        "Output only the Hugo markdown. Start with ---"
    )

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(model=_MODEL, contents=prompt)
    return response.text.strip()
