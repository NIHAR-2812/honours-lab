# Experiment No. 05
# Dense Vector Embeddings & Retrieval-Augmented Generation (RAG)

## 5.1 Aim

To construct a foundational Retrieval-Augmented Generation (RAG) pipeline by generating dense vector embeddings and performing cosine similarity search over a custom knowledge base.

## 5.2 Course Outcome

**CO3:** Design Retrieval-Augmented Generation (RAG) pipelines and integrate external knowledge bases to eliminate static training data boundaries.

## 5.3 Lab Outcome

**LO5:** Implement text embedding generation and cosine similarity calculation for retrieval.

## 5.4 Requirements

### Hardware Requirements

- Modern desktop or laptop with an x86-64 or ARM64 processor (minimum 4 cores).
- 8 GB system RAM minimum (16 GB recommended for local embedding model caching).
- Stable broadband internet connection for downloading pretrained weights and connecting to API endpoints.

### Software Requirements

- Operating System: Windows 10/11.
- Python Environment: CPython 3.11.x or 3.12.x.
- Development Environment: Visual Studio Code with the official Python extension.
- Core Libraries: sentence-transformers, numpy, scikit-learn, groq, python-dotenv.
- Cloud Credentials: Valid Groq Cloud API access key configured through environment variables.

## 5.5 Related Theory

### A. Dense Vector Embeddings in Latent Semantic Space

Dense vector embeddings represent text as numerical vectors in a continuous multidimensional space.

Traditional approaches such as Bag-of-Words and TF-IDF generate sparse representations and may not capture semantic relationships effectively.

Dense embedding models map sentences and passages into a latent vector space:

\[
f:S\rightarrow \mathbb{R}^{d}
\]

Where:

- S represents the input text.
- d represents the embedding dimensionality.
- Each text passage is represented by a numerical vector.

In this experiment, the `all-MiniLM-L6-v2` model generates vectors with 384 dimensions.

Semantically related passages are generally positioned closer together in the embedding space.

### B. Distance Metrics: Dot Product and Cosine Similarity

**1. Dot Product**

The dot product measures the product of corresponding vector components.

\[
u\cdot v=\sum_{i=1}^{d}u_iv_i
\]

It measures both vector magnitude and directional alignment.

**2. Cosine Similarity**

Cosine similarity measures the angular similarity between two vectors.

\[
\text{Cosine Similarity}(u,v)=
\frac{u\cdot v}{\|u\|\|v\|}
\]

Where:

- u and v are embedding vectors.
- \(u\cdot v\) is their dot product.
- \(\|u\|\) and \(\|v\|\) are their Euclidean norms.

Cosine similarity is useful for comparing semantic representations independently of their magnitudes.

Since the embeddings in this experiment are L2-normalized, cosine similarity is equivalent to their dot product.

### C. Vector Search Mechanics and Top-K Retrieval

The knowledge base is divided into textual passages called chunks.

Each passage is converted into an embedding vector using the same encoder model.

The resulting knowledge base embedding matrix is:

\[
M\in\mathbb{R}^{N\times d}
\]

Where:

- N is the number of passages.
- d is the embedding dimensionality.

During retrieval:

1. The user query is converted into a vector.
2. Cosine similarity is calculated between the query vector and every knowledge base vector.
3. The similarity scores are sorted in descending order.
4. The top-K most relevant passages are selected.

In this experiment, K = 2.

### D. LLM Context Window Augmentation

Retrieval-Augmented Generation combines external knowledge retrieval with LLM text generation.

The retrieved passages are inserted into the LLM prompt as context.

The model then generates an answer using the supplied information.

RAG helps address limitations associated with relying only on pretrained model knowledge, particularly when answering questions about private, specialised, or updated information.

## 5.6 Procedure – Configuration and Environment Setup

The following steps were performed to configure the experiment.

**Step 1: Navigate to the project directory**

```powershell
cd "C:\Users\cbec\Desktop\Coding\AIDS Honours"
```

**Step 2: Navigate to the experiment folder**

```powershell
cd Experiment_No_5
```

**Step 3: Create a Python virtual environment**

```powershell
python -m venv venv
```

**Step 4: Activate the virtual environment**

```powershell
venv\Scripts\activate
```

**Step 5: Upgrade pip and install dependencies**

```powershell
python -m pip install --upgrade pip

pip install numpy scikit-learn sentence-transformers groq python-dotenv
```

**Step 6: Configure the Groq API key**

The API key is stored in the root `.env` file.

```env
GROQ_API_KEY=your_actual_groq_api_key
```

**Step 7: Create the source code file**

```powershell
New-Item exp5.py -ItemType File
```

**Step 8: Execute the experiment**

```powershell
python exp5.py
```

## 5.7 Coding & Results

### Python Source Code

The implementation is provided in the file `exp5.py`.

The program consists of the following main components:

**1. Environment Configuration**

The `python-dotenv` library loads the Groq API key from the project root `.env` file.

**2. Model Initialisation**

The experiment initialises:

- Groq client for LLM inference.
- `all-MiniLM-L6-v2` for dense embedding generation.

The Groq model used is `openai/gpt-oss-120b`.

**3. Knowledge Base**

A custom knowledge base containing eight Apex University information passages is defined.

The passages cover:

- University establishment and location.
- Engineering specialisations.
- Assessment weightage.
- Research fellowship eligibility.
- Central Library facilities.
- HPC infrastructure.
- Industrial internship requirements.
- Campus dining regulations.

**4. Embedding Generation**

The `generate_embeddings()` function converts all knowledge base passages into L2-normalized numerical vectors.

**5. Cosine Similarity Retrieval**

The `retrieve_top_k()` function:

- Generates an embedding for the query.
- Calculates cosine similarity against all knowledge base vectors.
- Sorts the similarity scores.
- Returns the two highest-ranked passages.

**6. Groq Inference**

The `query_groq()` function sends prompts to the Groq API and returns the generated response.

**7. Baseline and RAG Comparison**

The program executes two inference approaches:

- Pure LLM inference without external context.
- RAG inference using retrieved knowledge base passages.

### Experimental Query

The query used for retrieval was:

"What are the computational specifications of Apex University's HPC cluster?"

### Step 1: Embedding Generation

Actual execution output:

```text
STEP 1: EMBEDDING KNOWLEDGE BASE PASSAGES INTO LATENT VECTOR SPACE

Successfully vectorized 8 documents.
Embedding Dimensionality (d): 384
Vector Space Matrix Shape: (8, 384)
```

This confirms that all eight knowledge base passages were successfully converted into 384-dimensional embeddings.

### Step 2: Retrieval Phase

Actual retrieval results:

| Rank | Cosine Similarity | Retrieved Passage |
|---|---:|---|
| 1 | 0.5553 | HPC cluster named Nova-8 with 64 Nvidia H100 GPUs |
| 2 | 0.3747 | Apex Research Fellowship eligibility requirements |

The first passage received the highest similarity score and was correctly identified as the most relevant passage for the query.

### Step 3: Pure LLM Inference

The baseline LLM was asked to answer the question using its internal knowledge without supplying external context.

Actual response:

```text
I’m sorry, but I don’t have information on the computational
specifications of Apex University’s HPC cluster.
```

The model could not provide the private institutional information.

### Step 4: Grounded RAG Inference

The two retrieved passages were supplied to the LLM as context.

The model was instructed to answer using only the provided context.

Actual response:

```text
Apex University’s on-premise high-performance cluster,
named Nova-8, is equipped with 64 Nvidia H100 Tensor Core GPUs.
```

The RAG pipeline successfully generated the correct answer using the retrieved knowledge base information.

### Observation and Pipeline Comparison Table

| Evaluation Parameter | Pure LLM Inference | RAG-Augmented Inference |
|---|---|---|
| External Knowledge Access | No external context supplied | Retrieved knowledge base passages supplied |
| Private Institutional Information | Could not provide the information | Correctly retrieved and used the information |
| Cluster Name | Not available | Nova-8 |
| Hardware Specifications | Not available | 64 Nvidia H100 Tensor Core GPUs |
| Retrieval Score | Not applicable | Top-1: 0.5553 |
| Answer Grounding | No external grounding | Grounded in retrieved context |

### Overall Observation

The experiment demonstrates that the baseline LLM could not answer a question about information absent from its available knowledge.

After retrieving the relevant passage through dense vector similarity search, the RAG pipeline provided the correct answer.

The top-ranked passage had a cosine similarity score of 0.5553, while the second-ranked passage had a score of 0.3747.

The reference similarity scores in the laboratory manual may differ because of model and environment variations. The values above represent the actual execution results.

## 5.8 Conclusion

In this laboratory experiment, a foundational dense Retrieval-Augmented Generation pipeline was successfully constructed and evaluated.

Using the Sentence Transformers model `all-MiniLM-L6-v2`, eight knowledge base passages were converted into 384-dimensional dense vector embeddings.

Cosine similarity was used to compare the query embedding against the knowledge base embeddings and retrieve the top two relevant passages.

The top-ranked passage achieved a similarity score of 0.5553 and correctly identified the Nova-8 HPC cluster equipped with 64 Nvidia H100 Tensor Core GPUs.

The pure LLM baseline could not provide this private institutional information. However, after supplying the retrieved context, the RAG pipeline generated an accurate response.

Thus, the experiment demonstrates how dense vector embeddings, semantic retrieval, and LLM context augmentation can improve factual question answering using external knowledge sources.

## 5.9 Post-Lab Viva Questions & Answers

### Question 1: What role does embedding dimensionality play in vector retrieval, and what trade-offs exist between lower-dimensional and higher-dimensional models?

**Answer:**

Embedding dimensionality determines the number of numerical values used to represent a text passage in vector space.

- **Higher-dimensional models:** Can represent more detailed semantic information but require more memory and computational resources.
- **Lower-dimensional models:** Require less storage and computation but may lose some semantic information.

In this experiment, `all-MiniLM-L6-v2` generates 384-dimensional embeddings, providing a compact representation suitable for semantic retrieval.

### Question 2: Contrast Bi-Encoders and Cross-Encoders in terms of architecture, retrieval latency, and ranking precision.

**Answer:**

**Bi-Encoders:**

- Encode the query and document independently.
- Document embeddings can be generated and stored in advance.
- Retrieval is fast because it uses vector similarity calculations.
- Suitable for searching large collections of documents.

**Cross-Encoders:**

- Process the query and document together.
- Use interactions between query and document tokens.
- Usually provide more precise relevance scoring.
- Require additional computation for every query-document pair.

Bi-Encoders are commonly used for initial retrieval, while Cross-Encoders can be used to rerank the retrieved results.

### Question 3: How does passage chunk size and chunk overlap affect the accuracy and performance of a RAG pipeline?

**Answer:**

**Chunk Size:**

- Very small chunks may lack sufficient context to represent the complete meaning of a passage.
- Very large chunks may combine unrelated information and reduce retrieval specificity.
- Appropriate chunk sizes help preserve meaningful information.

**Chunk Overlap:**

- Overlap preserves contextual continuity between neighbouring chunks.
- It prevents important sentences or related information from being separated at chunk boundaries.
- Typical overlap values may be around 10% to 20% of the chunk length, depending on the application.

Proper chunk size and overlap improve retrieval relevance and the quality of generated responses.