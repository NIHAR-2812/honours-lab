
# Experiment No. 06

## ChromaDB Vector Store Integration for Grounded Question Answering

### 6.1 Aim

To implement an AI-powered conversational query interface integrated with ChromaDB for automated document indexing, persistent vector storage, semantic retrieval, metadata filtering, and contextual question answering.

### 6.2 Course Outcome

**CO3:** Design Retrieval-Augmented Generation (RAG) pipelines and integrate external knowledge bases to eliminate static training data boundaries.

### 6.3 Lab Outcome

**LO6:** Develop conversational vector search pipelines using dedicated vector database indices.

### 6.4 Requirements

**Hardware Requirements**
- Modern x86-64 or ARM64 computer.
- Minimum 8 GB RAM.
- Minimum 10 GB free disk space.
- Active internet connection.

**Software Requirements**
- Windows 10/11.
- Python 3.12.
- Visual Studio Code.
- ChromaDB.
- OpenAI Python SDK.
- python-dotenv.
- Groq Cloud API account.

### 6.5 Related Theory

#### 1. Vector Databases

A vector database stores high-dimensional numerical representations called embeddings. These embeddings represent the semantic meaning of text, images, or other data.

Unlike traditional databases that primarily perform exact-match or structured queries, vector databases retrieve information based on similarity between vectors.

Common distance metrics include:

- **Cosine Distance:** Measures the difference in orientation between two vectors.
- **Euclidean Distance:** Measures the straight-line distance between two vectors.
- **Inner Product:** Measures the dot product between two vectors.

Cosine distance is calculated as:

\[
D_{\text{cosine}}(u,v)
=
1-\frac{u\cdot v}{\|u\|\|v\|}
\]

A lower cosine distance indicates greater similarity.

#### 2. ChromaDB

ChromaDB is an open-source vector database used to store embeddings, documents, and associated metadata.

Its important features include:

- Persistent local storage.
- Semantic similarity search.
- Metadata filtering.
- Collection management.
- Document insertion and updating.
- Integration with embedding models and LLMs.

In this experiment, ChromaDB stores technical documents in a persistent collection named `enterprise_distributed_systems`.

#### 3. Hierarchical Navigable Small World (HNSW)

HNSW is a graph-based approximate nearest-neighbor indexing technique.

Its architecture contains multiple graph layers:

1. The bottom layer contains all vectors with dense connections.
2. Higher layers contain fewer nodes and longer-range connections.
3. Search begins at an upper layer and progressively moves toward closer nodes in lower layers.

This structure enables efficient approximate nearest-neighbor retrieval for large vector collections.

#### 4. Metadata Filtering

Metadata filtering allows vector search results to be restricted using structured conditions.

For example:

```python
where={"category": "distributed-systems"}
```

This ensures that retrieval is limited to documents belonging to the specified category.

#### 5. Retrieval-Augmented Generation

Retrieval-Augmented Generation combines information retrieval with language-model generation.

The process involves:

1. Converting documents into embeddings.
2. Storing document vectors in a vector database.
3. Converting a user query into an embedding.
4. Retrieving the most relevant documents.
5. Supplying retrieved information to the language model.
6. Generating an answer grounded in the retrieved context.

### 6.6 Procedure

1. Created the Experiment No. 06 project directory.
2. Created and activated a Python virtual environment.
3. Installed ChromaDB, OpenAI SDK, and python-dotenv.
4. Configured the Groq API key using the existing `.env` file.
5. Initialized a ChromaDB persistent client.
6. Created or accessed the `enterprise_distributed_systems` collection with cosine distance.
7. Prepared four technical documents covering consensus protocols, database isolation, vector indexing, and the CAP theorem.
8. Inserted the documents using ChromaDB's `upsert()` operation.
9. Defined a query about node failure and leader election.
10. Applied a metadata filter to retrieve only distributed-systems documents.
11. Retrieved the top two matching documents.
12. Constructed a context using the retrieved document contents and titles.
13. Sent the context and query to the Groq language model.
14. Displayed the generated grounded answer.
15. Executed the program again to verify persistent storage and record consistency.

### 6.7 Implementation and Results

**Language Model:** `openai/gpt-oss-120b`

**Embedding Model:** `all-MiniLM-L6-v2` (ChromaDB default)

**Vector Database:** ChromaDB

**Collection Name:** `enterprise_distributed_systems`

**Query:**

"How does node failure or timeout trigger state changes during leader election?"

**Metadata Filter:**

```python
{"category": "distributed-systems"}
```

**Actual Retrieval Results:**

| Match | Retrieved Document | Cosine Distance |
|---|---|---:|
| 1 | Consensus Protocols | 0.4644 |
| 2 | CAP Theorem | 0.7391 |

**Generated Response:**

The generated response explained that Raft leaders periodically send AppendEntries heartbeat RPCs to followers.

If a follower stops receiving heartbeat messages, its election timeout eventually expires. The follower then assumes that the leader is no longer reachable, increments its current term, and transitions from follower to candidate to begin a new election.

**Source:** Consensus Protocols.

**Execution Summary:**

| Parameter | Actual Result |
|---|---|
| Documents ingested | 4 |
| Collection record count | 4 |
| Metadata filter | distributed-systems |
| Retrieved documents | 2 |
| Top-1 cosine distance | 0.4644 |
| Top-2 cosine distance | 0.7391 |
| LLM provider | Groq |
| LLM model | openai/gpt-oss-120b |
| Initial execution | Successful |
| Second execution | Successful |
| Persistence verification | Successful |

### 6.8 Observation and Performance Evaluation

The following observations were recorded from the actual execution:

| Observation | Result |
|---|---|
| Document ingestion | Successful |
| Vector embedding generation | Successful |
| Persistent ChromaDB initialization | Successful |
| Collection creation/access | Successful |
| Semantic retrieval | Successful |
| Metadata filtering | Successful |
| Context construction | Successful |
| Groq API integration | Successful |
| Grounded answer generation | Successful |
| Repeated execution without duplicate records | Successful |

The Consensus Protocols document achieved the lowest cosine distance of **0.4644**, making it the closest retrieved document to the leader-election query.

The CAP Theorem document was also retrieved because it belongs to the selected category, but its higher cosine distance of **0.7391** indicates lower similarity to the query.

The second execution confirmed that the collection persisted locally and retained exactly four records.

### 6.9 Conclusion

The experiment successfully implemented a persistent vector retrieval system using ChromaDB and integrated it with Groq for contextual question answering.

Four technical documents were indexed in the vector database. Semantic search and metadata filtering were used to retrieve relevant information based on the user's query. The retrieved context was passed to the language model, which generated an accurate answer about Raft leader election and cited the relevant source.

The second execution verified that ChromaDB retained the stored collection without creating duplicate records.

Thus, the experiment demonstrated how vector databases can support semantic retrieval, persistent document storage, and grounded question answering in a Retrieval-Augmented Generation pipeline.

### 6.10 Post-Lab Viva Questions and Answers

**Q1. How does the multi-layer architecture of HNSW achieve efficient query complexity?**

**Answer:** HNSW uses multiple graph layers inspired by skip lists. Upper layers contain sparse nodes and long-range connections that help navigate quickly across the vector space. Lower layers contain denser connections that allow more precise searching. This hierarchical approach reduces the search space and supports efficient approximate nearest-neighbor retrieval.

**Q2. Why is cosine distance equivalent to Euclidean distance when embeddings are unit-normalized?**

**Answer:** For two unit-normalized vectors \(u\) and \(v\):

\[
\|u-v\|^2
=
\|u\|^2+\|v\|^2-2(u\cdot v)
\]

Since both vectors have unit magnitude:

\[
\|u-v\|^2=2-2(u\cdot v)
\]

Therefore:

\[
\|u-v\|^2=2D_{\text{cosine}}
\]

Both metrics consequently produce the same nearest-neighbor ranking for unit-normalized vectors.

**Q3. How do production vector databases manage data drift, updates, and vector deletions without degrading graph connectivity?**

**Answer:** Production vector databases use techniques such as:

- **Tombstoning:** Marks deleted vectors so they are excluded from search results.
- **Periodic compaction:** Removes deleted records and reorganizes index structures.
- **Segment merging:** Combines smaller index segments into larger structures to maintain efficient retrieval.

These techniques help maintain index quality and retrieval performance as data changes.
