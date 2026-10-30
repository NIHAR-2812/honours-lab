# Experiment 5: Dense Vector Embeddings & Retrieval-Augmented Generation (RAG)

## Aim

To construct a foundational Retrieval-Augmented Generation (RAG) pipeline by generating dense vector embeddings and performing cosine similarity search over a custom knowledge base.

## Course Outcome

**CO3:** Design Retrieval-Augmented Generation (RAG) pipelines and integrate external knowledge bases to eliminate static training data boundaries.

## Lab Outcome

**LO5:** Implement text embedding generation and cosine similarity calculation for retrieval.

## Overview

Retrieval-Augmented Generation (RAG) is an approach that combines information retrieval with Large Language Model (LLM) generation.

Instead of depending entirely on the information learned during model training, a RAG system retrieves relevant information from an external knowledge base and supplies it to the LLM as context.

This experiment implements a foundational RAG pipeline using dense vector embeddings, cosine similarity, Top-K retrieval, and Groq API inference.

The system compares a normal LLM response with a context-grounded RAG response.

## Technologies Used

| Component | Technology |
|---|---|
| Programming Language | Python 3.12 |
| Embedding Model | all-MiniLM-L6-v2 |
| Embedding Library | Sentence Transformers |
| Numerical Operations | NumPy |
| Similarity Calculation | Scikit-learn |
| LLM Inference | Groq API |
| LLM Model | openai/gpt-oss-120b |
| Environment Configuration | python-dotenv |

## RAG Pipeline Architecture

The experiment follows these stages:

1. **Knowledge Base:** Define a custom knowledge base containing eight Apex University information passages.
2. **Embedding Generation:** Convert each passage into a dense numerical vector using `all-MiniLM-L6-v2`.
3. **Query Embedding:** Convert the user's question into a vector using the same embedding model.
4. **Similarity Search:** Calculate cosine similarity between the query vector and knowledge base vectors.
5. **Top-K Retrieval:** Select the two most relevant passages based on similarity scores.
6. **LLM Inference:** Generate a response using the retrieved context.
7. **Comparison:** Compare the pure LLM response with the RAG-grounded response.

## Embedding Model

The experiment uses the `all-MiniLM-L6-v2` sentence-transformer model.

- Embedding dimensionality: 384
- Number of knowledge base passages: 8
- Vector matrix shape: (8, 384)
- Embeddings are L2-normalized before similarity calculation.

## Cosine Similarity

Cosine similarity measures the angular similarity between two vectors.

The formula is:

\[
\text{Cosine Similarity}(u,v)=
\frac{u \cdot v}{\|u\|\|v\|}
\]

A higher cosine similarity score indicates greater semantic similarity between the query and a passage.

## Top-K Retrieval

The system calculates similarity scores between the query embedding and all knowledge base embeddings.

The passages are sorted in descending order of similarity, and the top two passages are selected for the RAG context.

## Project Structure

```text
AIDS Honours/
│
├── .env
├── README.md
│
└── Experiment_No_5/
    ├── exp5.py
    ├── requirements.txt
    ├── README.md
    ├── report.md
    │
    ├── code.png
    └── output.png
```

The `.env` file is maintained in the project root directory, one level above the experiment folder.

## Installation and Setup

### 1. Navigate to the Project Directory

```powershell
cd "C:\Users\cbec\Desktop\Coding\AIDS Honours"
```

### 2. Activate the Virtual Environment

If the virtual environment has already been created:

```powershell
cd Experiment_No_5
venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure the Groq API Key

Create or update the `.env` file in the project root:

```env
GROQ_API_KEY=your_actual_groq_api_key
```

Replace the placeholder with your actual API key.

### 5. Run the Experiment

From the `Experiment_No_5` directory:

```powershell
python exp5.py
```

Alternatively, from the project root:

```powershell
python Experiment_No_5\exp5.py
```

**Note:** During the first execution, the sentence-transformer model may be downloaded from Hugging Face. Internet access is required for the initial download.

## Execution Results

The experiment successfully vectorized eight knowledge base passages.

| Parameter | Actual Result |
|---|---|
| Documents Vectorized | 8 |
| Embedding Dimension | 384 |
| Vector Matrix Shape | (8, 384) |
| Top-1 Similarity Score | 0.5553 |
| Top-2 Similarity Score | 0.3747 |

### Retrieved Passages

**Rank 1 – Cosine Similarity: 0.5553**

Apex University computational infrastructure includes an on-premise high-performance cluster called Nova-8 equipped with 64 Nvidia H100 Tensor Core GPUs.

**Rank 2 – Cosine Similarity: 0.3747**

To qualify for an Apex Research Fellowship, undergraduate students must maintain a minimum CGPA of 8.75 and author at least one indexed conference publication.

### Pure LLM Response

The baseline LLM could not provide information about the computational specifications of Apex University's HPC cluster.

### RAG-Augmented Response

The RAG pipeline correctly identified the HPC cluster as Nova-8 and stated that it is equipped with 64 Nvidia H100 Tensor Core GPUs.

## Conclusion

The experiment successfully demonstrates the implementation of a foundational dense Retrieval-Augmented Generation pipeline.

The `all-MiniLM-L6-v2` model generated 384-dimensional embeddings for eight knowledge base passages. Cosine similarity was used to retrieve the two most relevant passages for the given query.

The retrieved context enabled the Groq LLM to provide an accurate answer about Apex University's HPC infrastructure, which the baseline LLM could not provide.

Thus, the experiment demonstrates how dense vector embeddings and semantic retrieval can improve the factual grounding of LLM responses.

## Limitations

- The knowledge base contains a limited number of predefined passages.
- The experiment uses a local embedding model and a simulated institutional knowledge base.
- Retrieval quality depends on the embedding model and the quality of the stored passages.
- The experiment uses basic cosine similarity rather than a dedicated vector database.
- The retrieved information is limited to the content available in the knowledge base.