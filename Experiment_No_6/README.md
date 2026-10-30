
# Experiment 06 – ChromaDB Vector Store Integration for Grounded Question Answering

## Aim
Implement an AI-powered conversational query interface integrated with ChromaDB for automated document indexing, persistent vector storage, semantic retrieval, metadata filtering, and contextual question answering.

## Course Outcome
**CO3:** Design Retrieval-Augmented Generation (RAG) pipelines and integrate external knowledge bases to eliminate static training data boundaries.

## Lab Outcome
**LO6:** Develop conversational vector search pipelines using dedicated vector database indices.

## Technologies Used
- Python 3.12
- ChromaDB – Persistent vector database
- OpenAI Python SDK – Groq API compatibility
- Groq Cloud API – LLM inference
- `openai/gpt-oss-120b` – Language model
- `all-MiniLM-L6-v2` – Default ChromaDB embedding model
- python-dotenv – Environment variable management

## Project Structure

```text
AIDS Honours/
│
├── .env
│
└── Experiment_No_6/
    ├── venv/
    ├── chroma_db_store/
    ├── outputs/
    │   ├── code.png
    │   └── output.png
    ├── exp6.py
    ├── requirements.txt
    ├── README.md
    └── report.md
```

## Installation and Setup

### 1. Navigate to the experiment directory

```powershell
cd "C:\Users\cbec\Desktop\Coding\AIDS Honours\Experiment_No_6"
```

### 2. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure the API key

The project uses the root `.env` file:

```text
GROQ_API_KEY=your_actual_groq_api_key
```

Do not upload the API key to GitHub.

### 5. Execute the experiment

```powershell
python exp6.py
```

## Implementation

The experiment implements the following operations:

1. **Environment initialization:** Loads the Groq API key from the root environment file.
2. **Persistent storage:** Initializes a ChromaDB PersistentClient that stores database files locally.
3. **Collection management:** Creates or accesses the `enterprise_distributed_systems` collection using cosine distance.
4. **Document ingestion:** Inserts four technical documents using `upsert()`.
5. **Semantic retrieval:** Searches for documents related to the user query.
6. **Metadata filtering:** Restricts retrieval to documents belonging to the `distributed-systems` category.
7. **Context construction:** Combines retrieved documents and their source titles.
8. **Grounded generation:** Sends the retrieved context and query to the Groq language model to generate an answer.

## Knowledge Base

The collection contains four documents:

| Document ID | Title | Category |
|---|---|---|
| doc_001 | Consensus Protocols | distributed-systems |
| doc_002 | Database Isolation | databases |
| doc_003 | Vector Index Structures | databases |
| doc_004 | CAP Theorem | distributed-systems |

## Query Used

"How does node failure or timeout trigger state changes during leader election?"

Metadata filter:

```python
{"category": "distributed-systems"}
```

The system retrieves the top two matching documents.

## Actual Execution Results

| Parameter | Observed Result |
|---|---|
| Documents ingested | 4 |
| Collection | enterprise_distributed_systems |
| Distance metric | Cosine |
| Top-K | 2 |
| First retrieved document | Consensus Protocols |
| First cosine distance | 0.4644 |
| Second retrieved document | CAP Theorem |
| Second cosine distance | 0.7391 |
| Groq model | openai/gpt-oss-120b |
| Persistence verification | Successful |

### Generated Answer

The system explained that Raft leaders periodically send AppendEntries heartbeat RPCs to followers.

When a follower stops receiving heartbeat messages and its election timeout expires, it:

- Assumes that the current leader is no longer reachable.
- Increments its current term.
- Transitions from follower to candidate.
- Begins a new leader election.

**Source:** Consensus Protocols.

## Key Observations

- ChromaDB successfully ingested all four technical documents.
- The default `all-MiniLM-L6-v2` embedding model generated vectors for semantic retrieval.
- Cosine distance was used to rank retrieved documents.
- Metadata filtering restricted the search to distributed-systems documents.
- The Consensus Protocols document was retrieved as the closest match.
- Groq generated a contextual answer using the retrieved knowledge.
- Local persistent storage retained the collection between executions.
- Repeated execution did not create duplicate records because `upsert()` was used.

## Conclusion

The experiment successfully implemented a persistent vector retrieval pipeline using ChromaDB and integrated it with Groq for grounded question answering. Semantic search and metadata filtering helped identify relevant technical documents from the knowledge base.

The retrieved context enabled the language model to generate an accurate response about Raft leader election, demonstrating the practical use of vector databases in Retrieval-Augmented Generation systems.
