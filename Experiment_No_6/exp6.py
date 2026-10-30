
"""
Experiment No. 06
ChromaDB Vector Store Integration for Grounded Question Answering

Features:
- Persistent ChromaDB vector storage
- Document ingestion using upsert
- Semantic search using cosine distance
- Metadata filtering
- Context-grounded answer generation using Groq
"""

import sys
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI


# ---------------------------------------------------------
# 1. Environment and Groq Client Initialization
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_PATH)

import os

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    sys.exit(
        f"Error: GROQ_API_KEY not found. Check your environment file: {ENV_PATH}"
    )

client = OpenAI(
    api_key=groq_api_key,
    base_url="https://api.groq.com/openai/v1"
)

MODEL_NAME = "openai/gpt-oss-120b"


# ---------------------------------------------------------
# 2. Persistent ChromaDB Client and Collection
# ---------------------------------------------------------

PERSIST_DIRECTORY = Path(__file__).resolve().parent / "chroma_db_store"
COLLECTION_NAME = "enterprise_distributed_systems"

chroma_client = chromadb.PersistentClient(
    path=str(PERSIST_DIRECTORY)
)

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)


# ---------------------------------------------------------
# 3. Knowledge Corpus Preparation
# ---------------------------------------------------------

raw_documents = [
    {
        "id": "doc_001",
        "title": "Consensus Protocols",
        "category": "distributed-systems",
        "content": (
            "The Raft consensus algorithm is designed to be understandable and safe. "
            "It decomposes leader election, log replication, and safety guarantees into "
            "independent subproblems. Leaders send periodic heartbeats (AppendEntries RPC) "
            "to retain authority. When a follower election timeout triggers without hearing "
            "from a leader, it increments its current term and transitions to candidate state."
        )
    },
    {
        "id": "doc_002",
        "title": "Database Isolation",
        "category": "databases",
        "content": (
            "Snapshot Isolation (SI) guarantees that all reads made in a transaction "
            "see a consistent snapshot of the database from the time the transaction started. "
            "Write-skew anomalies can still occur under standard Snapshot Isolation unless "
            "explicit two-phase locking or Serializable Snapshot Isolation (SSI) with "
            "dependency-tracking graphs is enforced across conflicting commits."
        )
    },
    {
        "id": "doc_003",
        "title": "Vector Index Structures",
        "category": "databases",
        "content": (
            "Hierarchical Navigable Small World (HNSW) graphs implement approximate nearest "
            "neighbor queries with logarithmic search performance. Upper layers maintain sparse "
            "long-range edges for coarse positioning, whereas lower layers provide dense, "
            "fine-grained exploration. Construction complexity is O(N log N) while lookup runs in O(log N)."
        )
    },
    {
        "id": "doc_004",
        "title": "CAP Theorem",
        "category": "distributed-systems",
        "content": (
            "Brewer's CAP Theorem asserts that a distributed data store can simultaneously "
            "guarantee at most two of three properties: Consistency (every read receives the "
            "most recent write or an error), Availability (every request receives a non-error response), "
            "and Partition Tolerance (the system operates despite network dropped packets)."
        )
    }
]


# ---------------------------------------------------------
# 4. Document Ingestion
# ---------------------------------------------------------

def ingest_documents():
    doc_ids = [doc["id"] for doc in raw_documents]
    doc_texts = [doc["content"] for doc in raw_documents]

    doc_metadatas = [
        {
            "title": doc["title"],
            "category": doc["category"]
        }
        for doc in raw_documents
    ]

    print(
        f"[*] Ingesting {len(raw_documents)} documents "
        f"into collection '{COLLECTION_NAME}'..."
    )

    # upsert inserts new records and updates existing IDs.
    # It avoids duplicate records when the script is rerun.
    collection.upsert(
        ids=doc_ids,
        documents=doc_texts,
        metadatas=doc_metadatas
    )

    print(
        f"[+] Ingestion complete. "
        f"Index record count: {collection.count()}\n"
    )


# ---------------------------------------------------------
# 5. Semantic Search with Metadata Filtering
# ---------------------------------------------------------

def retrieve_documents(query_text, top_k=2):
    filter_criteria = {
        "category": "distributed-systems"
    }

    print(f"[*] Query: '{query_text}'")
    print(f"[*] Metadata Filter: {filter_criteria}")

    search_results = collection.query(
        query_texts=[query_text],
        n_results=top_k,
        where=filter_criteria
    )

    retrieved_docs = search_results["documents"][0]
    retrieved_metadata = search_results["metadatas"][0]
    retrieved_distances = search_results["distances"][0]

    context_accumulator = []

    print("\n--- Retrieved Knowledge Chunks ---")

    for i in range(len(retrieved_docs)):
        distance = retrieved_distances[i]
        metadata = retrieved_metadata[i]
        chunk = retrieved_docs[i]

        print(
            f"Match [{i + 1}] | "
            f"Source: {metadata['title']} | "
            f"Cosine Distance: {distance:.4f}"
        )
        print(f"Text Snippet: {chunk}\n")

        context_accumulator.append(
            f"Source [{metadata['title']}]: {chunk}"
        )

    return "\n\n".join(context_accumulator)


# ---------------------------------------------------------
# 6. Grounded Answer Generation using Groq
# ---------------------------------------------------------

def generate_grounded_answer(query_text, context):
    system_prompt = (
        "You are a strict technical query assistant. Generate an accurate response "
        "based exclusively on the provided context below. If the information is not "
        "explicitly present, state that the context does not contain sufficient "
        "information. Always cite your source titles.\n\n"
        f"CONTEXT INFORMATION:\n{context}"
    )

    print("[*] Dispatching context-augmented payload to Groq Cloud...")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query_text}
        ],
        temperature=0.1,
        max_tokens=300
    )

    return response.choices[0].message.content


# ---------------------------------------------------------
# 7. Main Experiment
# ---------------------------------------------------------

def run_experiment():
    print("=" * 65)
    print("EXPERIMENT 06: CHROMADB VECTOR STORE INTEGRATION")
    print("=" * 65)

    print(f"[*] ChromaDB storage: {PERSIST_DIRECTORY}")
    print(f"[*] Groq model: {MODEL_NAME}\n")

    ingest_documents()

    query_text = (
        "How does node failure or timeout trigger state changes "
        "during leader election?"
    )

    context = retrieve_documents(
        query_text=query_text,
        top_k=2
    )

    if not context:
        print("[!] No relevant documents were retrieved.")
        return

    answer = generate_grounded_answer(
        query_text=query_text,
        context=context
    )

    print("\n================ GROUNDED MODEL RESPONSE ================")
    print(answer)
    print("=========================================================")

    print("\n[+] Experiment 06 completed successfully.")
    print("[+] ChromaDB collection remains saved on disk.")


if __name__ == "__main__":
    try:
        run_experiment()
    except Exception as error:
        print(f"\n[ERROR] Experiment failed: {error}")
        raise
