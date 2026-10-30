"""
Experiment No: 05
Title: Foundational Dense Retrieval-Augmented Generation (RAG) Pipeline
Course: CS501PC - Foundations of Artificial Intelligence Lab
"""

import os
from pathlib import Path
from typing import List, Tuple

import numpy as np
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from groq import Groq


# ---------------------------------------------------------
# 1. LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------

# Load .env from the project root directory
ROOT_ENV = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ROOT_ENV)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "CRITICAL ERROR: GROQ_API_KEY is not defined in the root .env file."
    )


# ---------------------------------------------------------
# 2. INITIALIZE GROQ CLIENT AND EMBEDDING MODEL
# ---------------------------------------------------------

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "openai/gpt-oss-120b"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

print(f"\n[INIT] Loading dense vector bi-encoder: {EMBED_MODEL_NAME}...")

encoder = SentenceTransformer(EMBED_MODEL_NAME)


# ---------------------------------------------------------
# 3. DEFINE CUSTOM KNOWLEDGE BASE
# ---------------------------------------------------------

KNOWLEDGE_BASE = [
    "Apex University was established in 2024 as an AI-first research institution located in Cyber City, Hyderabad.",

    "Apex University offers undergraduate engineering degrees across three specializations: Neural Systems, Autonomous Robotics, and Quantum Machine Learning.",

    "The maximum permissible continuous assessment weightage for lab practicals at Apex University is capped at 60 percent, with 40 percent reserved for final end-term juries.",

    "To qualify for an Apex Research Fellowship, undergraduate students must maintain a minimum CGPA of 8.75 and author at least one indexed conference publication.",

    "The Central Library at Apex University operates on an automated RFID checkout protocol and stays open 24 hours daily during examination cycles.",

    "Apex University computational infrastructure includes an on-premise high-performance cluster called Nova-8 equipped with 64 Nvidia H100 Tensor Core GPUs.",

    "All graduate programs at Apex University require completing a mandatory industrial co-op internship lasting a minimum of 24 weeks.",

    "Campus dining regulations at Apex University prohibit single-use plastics and enforce a completely sustainable, zero-waste biodegradable packaging standard."
]


# ---------------------------------------------------------
# 4. GENERATE DENSE VECTOR EMBEDDINGS
# ---------------------------------------------------------

def generate_embeddings(text_corpus: List[str]) -> np.ndarray:
    """
    Converts text passages into L2-normalized dense vectors.
    """

    vectors = encoder.encode(
        text_corpus,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return vectors


# ---------------------------------------------------------
# 5. COSINE SIMILARITY AND TOP-K RETRIEVAL
# ---------------------------------------------------------

def retrieve_top_k(
    query_text: str,
    corpus: List[str],
    corpus_vectors: np.ndarray,
    k: int = 2
) -> List[Tuple[float, str]]:
    """
    Encodes the query, calculates cosine similarity,
    and returns the top-k most relevant passages.
    """

    query_vector = encoder.encode(
        [query_text],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    similarities = cosine_similarity(
        query_vector,
        corpus_vectors
    )[0]

    ranked_indices = np.argsort(similarities)[::-1][:k]

    results = [
        (float(similarities[idx]), corpus[idx])
        for idx in ranked_indices
    ]

    return results


# ---------------------------------------------------------
# 6. GROQ LLM INFERENCE
# ---------------------------------------------------------

def query_groq(prompt_payload: str) -> str:
    """
    Sends a prompt to the Groq LLM and returns its response.
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a factual, concise academic assistant."
            },
            {
                "role": "user",
                "content": prompt_payload
            }
        ],
        model=MODEL_NAME,
        temperature=0.0,
        max_tokens=256
    )

    return chat_completion.choices[0].message.content.strip()


# ---------------------------------------------------------
# 7. MAIN EXPERIMENT
# ---------------------------------------------------------

def run_experiment():

    print("\n" + "=" * 80)
    print("STEP 1: EMBEDDING KNOWLEDGE BASE PASSAGES INTO LATENT VECTOR SPACE")
    print("=" * 80)

    # Generate embeddings for all knowledge base passages
    corpus_embeddings = generate_embeddings(KNOWLEDGE_BASE)

    print(
        f"Successfully vectorized {corpus_embeddings.shape[0]} documents."
    )

    print(
        f"Embedding Dimensionality (d): {corpus_embeddings.shape[1]}"
    )

    print(
        f"Vector Space Matrix Shape: {corpus_embeddings.shape}"
    )

    # Define the user query
    query = (
        "What are the computational specifications of "
        "Apex University's HPC cluster?"
    )

    print("\n" + "=" * 80)
    print(f"STEP 2: RETRIEVAL PHASE FOR QUERY: '{query}'")
    print("=" * 80)

    # Retrieve the two most relevant knowledge passages
    top_k_matches = retrieve_top_k(
        query,
        KNOWLEDGE_BASE,
        corpus_embeddings,
        k=2
    )

    for rank, (score, chunk) in enumerate(top_k_matches, start=1):
        print(
            f"\nRank {rank} [Cosine Similarity: {score:.4f}]:"
            f"\n -> \"{chunk}\""
        )

    # Construct context from retrieved passages
    context_str = "\n".join(
        [f"- {chunk}" for _, chunk in top_k_matches]
    )

    # -----------------------------------------------------
    # 8. PURE LLM BASELINE
    # -----------------------------------------------------

    pure_prompt = (
        "Answer the following question precisely based on "
        "your internal knowledge:\n\n"
        f"Question: {query}"
    )

    print("\n" + "=" * 80)
    print("STEP 3: EXECUTING INFERENCE: BASELINE PURE LLM")
    print("=" * 80)

    pure_response = query_groq(pure_prompt)

    print("\nPure LLM Response:")
    print(pure_response)

    # -----------------------------------------------------
    # 9. RAG-AUGMENTED INFERENCE
    # -----------------------------------------------------

    rag_prompt = (
        "You are a strictly grounded AI assistant. "
        "Answer the user query using ONLY the supplied context.\n"
        "If the answer cannot be deduced from the context, "
        "state that the information is unavailable.\n\n"
        f"Context Chunks:\n{context_str}\n\n"
        f"Question: {query}\n\n"
        "Answer:"
    )

    print("\n" + "=" * 80)
    print("STEP 4: EXECUTING INFERENCE: GROUNDED RAG PIPELINE")
    print("=" * 80)

    rag_response = query_groq(rag_prompt)

    print("\nRAG-Augmented Response:")
    print(rag_response)

    print("\n" + "=" * 80)
    print("EXPERIMENT 05 COMPLETED SUCCESSFULLY")
    print("=" * 80)


# ---------------------------------------------------------
# 10. PROGRAM ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    try:
        run_experiment()

    except Exception as error:
        print(f"\n[ERROR] Experiment failed: {error}")