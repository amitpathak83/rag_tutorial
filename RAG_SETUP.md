# Local RAG System Implementation

A complete **Retrieval-Augmented Generation (RAG)** system for PDF documents using open-source technologies: LangChain, Chroma, and Ollama.

## Overview

RAG combines the power of large language models with document retrieval. Instead of relying solely on the model's training data, RAG retrieves relevant documents and provides them as context, enabling accurate answers to document-specific questions.

```
Question Input
     ↓
[Embedding Layer] ← Converts question to vector using Ollama
     ↓
[Chroma Vector DB] ← Searches for similar documents
     ↓
[Retrieved Context] ← Top-k relevant documents
     ↓
[LLM Prompt] ← Builds context-aware prompt with LLM (Ollama)
     ↓
[Answer Generation] ← LLM generates answer based on context
     ↓
Final Answer → Return to user with sources
```

## Architecture

### Components

1. **Document Loader** - Loads PDF files using `langchain-community`
2. **Text Splitter** - Chunks documents for better retrieval (1000 tokens with 200 overlap)
3. **Embeddings** - Converts text to vectors using `nomic-embed-text` via Ollama
4. **Vector Store** - Chroma (open-source, embedded, runs locally)
5. **Retriever** - Similarity search to find relevant documents
6. **LLM** - Ollama for generation (using `mistral` by default)
7. **RAG Chain** - Orchestrates the full pipeline

### Technology Stack

| Component | Technology | Why? |
|-----------|-----------|------|
| Vector DB | Chroma | Open-source, local, embedded, no setup |
| Embeddings | Ollama + nomic-embed-text | Local, fast, specialized for retrieval |
| LLM | Ollama + mistral | Local inference, privacy, offline capable |
| Orchestration | LangChain | Industry standard, flexible chains |
| PDF Loading | langchain-community | Reliable, handles various PDF types |

## Installation

### 1. Install Ollama

**macOS:**
```bash
brew install ollama
```

Or download from: https://ollama.ai

### 2. Start Ollama Server

```bash
# In a separate terminal, keep running
ollama serve
```

### 3. Download Models

```bash
# Download the LLM model (for generation)
ollama pull mistral

# Download the embedding model (for retrieval)
ollama pull nomic-embed-text

# Optional: Other models
ollama pull neural-chat     # Faster LLM alternative
ollama pull phi             # Ultra-fast but simpler
```

### 4. Install Python Dependencies

```bash
pipenv install
pipenv shell
```

Required packages added to Pipfile:
- `chromadb` - Vector database
- `langchain-community` - Document loaders
- `pypdf` - PDF reading

## Files

| File | Purpose |
|------|---------|
| `rag_system.py` | Core RAG implementation |
| `rag_demo.py` | Demonstration and examples |
| `RAG_SETUP.md` | This documentation |

## Quick Start

### Interactive Mode

```bash
python rag_system.py
```

Commands:
```
load document.pdf           # Load a PDF
load_dir ./documents/       # Load all PDFs from directory
query What is this about?   # Ask a question
list                        # Show loaded documents
clear                       # Clear vector store
help                        # Show commands
quit                        # Exit
```

### Command Line Mode

```bash
# Load and query a single PDF
python rag_system.py --pdf document.pdf --query "What are the main points?"

# Load directory and query
python rag_system.py --dir ./documents/ --query "Summarize findings"

# Use custom models
python rag_system.py --model neural-chat --embedding-model nomic-embed-text --pdf doc.pdf
```

### Programmatic Usage

```python
from rag_system import PDFRAGSystem

# Initialize
rag = PDFRAGSystem(
    model_name="mistral",
    embedding_model="nomic-embed-text",
    chunk_size=1000,
    chunk_overlap=200,
    db_path="./chroma_db"
)

# Load documents
documents = rag.load_pdf("research_paper.pdf")
rag.add_documents(documents, pdf_name="paper.pdf")

# Query
answer = rag.query("What are the conclusions?", with_context=True)
print(answer)

# Get retrieval scores
results = rag.get_retrieval_score("methodology", k=3)
for doc, score in results:
    print(f"Score: {score:.4f}, Content: {doc.page_content[:100]}...")
```

## API Reference

### PDFRAGSystem Class

#### Initialization

```python
rag = PDFRAGSystem(
    model_name: str = "mistral",              # LLM model
    embedding_model: str = "nomic-embed-text", # Embedding model
    chunk_size: int = 1000,                   # Characters per chunk
    chunk_overlap: int = 200,                 # Overlap between chunks
    db_path: str = "./chroma_db"              # Vector DB location
)
```

#### Methods

**Loading Documents:**
```python
rag.load_pdf(pdf_path: str) -> List[Document]
  Load a single PDF file

rag.load_pdfs(pdf_dir: str) -> List[Document]
  Load all PDFs from a directory

rag.add_documents(documents, pdf_name: str = "document")
  Process and add documents to vector store
```

**Querying:**
```python
rag.query(question: str, with_context: bool = False) -> str
  Answer a question using RAG
  - with_context=True includes source citations

rag.get_retrieval_score(question: str, k: int = 3) -> List[tuple]
  Get relevant documents with similarity scores
  Returns: [(document, score), ...]
```

**Management:**
```python
rag.list_documents() -> List[str]
  List all loaded document sources

rag.clear_documents()
  Delete vector store and reset system
```

## Usage Examples

### Example 1: Basic RAG

```python
from rag_system import PDFRAGSystem

rag = PDFRAGSystem()

# Load PDF
docs = rag.load_pdf("paper.pdf")
rag.add_documents(docs)

# Ask question
answer = rag.query("What is the methodology?")
print(answer)
```

### Example 2: Batch Processing

```python
# Load all PDFs from directory
documents = rag.load_pdfs("./research_papers/")
rag.add_documents(documents)

# Ask questions
print(rag.query("Compare the findings across papers"))
print(rag.query("What methods were used?"))
```

### Example 3: With Source Attribution

```python
answer = rag.query("Who are the authors?", with_context=True)
# Output includes answer plus source documents
print(answer)
```

### Example 4: Retrieval Analysis

```python
# See which documents are most relevant
results = rag.get_retrieval_score("methodology", k=5)

for doc, score in results:
    print(f"\nScore: {score:.4f}")
    print(f"Content: {doc.page_content[:200]}")
    print(f"Source: {doc.metadata.get('source')}")
```

### Example 5: Custom Configuration

```python
# Optimize for speed
rag = PDFRAGSystem(
    model_name="phi",              # Very fast but less accurate
    chunk_size=500,                # Smaller chunks, faster retrieval
    chunk_overlap=50,              # Less overlap
    db_path="./fast_rag_db"
)
```

## How RAG Works

### Step 1: Chunking

Documents are split into overlapping chunks to fit embedding model context:
- **Chunk size**: 1000 characters
- **Overlap**: 200 characters (30% overlap)
- **Why overlap**: Prevents important info from being cut across chunk boundaries

### Step 2: Embedding

Each chunk is converted to a vector using `nomic-embed-text`:
- 384-dimensional vectors
- Optimized for retrieval (not generation)
- Running locally via Ollama (privacy!)

### Step 3: Storage

Chroma stores embeddings with original text and metadata:
- Local SQLite database
- Built-in similarity search
- Persistent across sessions

### Step 4: Retrieval

When a question is asked:
1. Question is embedded using same model
2. Chroma finds k=5 most similar chunks
3. Chunks are returned as context

### Step 5: Generation

LLM generates answer using:
- Retrieved context
- Original question  
- System prompt
- Temperature=0.3 (deterministic)

## Configuration Guide

### Chunk Size Impact

| Size | Pros | Cons |
|------|------|------|
| 500 | Precise retrieval | Small context, more chunks |
| 1000 | Balanced (default) | Medium total context |
| 2000 | Large context | Too broad, less precise |

### Overlap Impact

| Overlap | Pros | Cons |
|---------|------|------|
| 50 (5%) | Fast, small DB | May lose context at boundaries |
| 200 (20%) | Good balance (default) | Slightly larger DB |
| 400 (40%) | High overlap | Very large DB, slow |

### Model Selection

**For Generation (LLM):**
- `mistral` (default) - Best quality, balanced
- `neural-chat` - Good for conversation
- `phi` - Fastest, less accurate
- `llama2` - Good general purpose

**For Embeddings:**
- `nomic-embed-text` (default) - Best for retrieval
- Other options not as optimized

## Performance Optimization

### Speed Up

```python
# Use faster LLM
rag = PDFRAGSystem(model_name="phi")

# Smaller chunks
rag = PDFRAGSystem(chunk_size=500, chunk_overlap=50)

# Smaller documents
documents = rag.load_pdfs("./small_pdfs/")
```

### Better Quality

```python
# Use larger LLM  
rag = PDFRAGSystem(model_name="neural-chat")

# Larger chunks (more context)
rag = PDFRAGSystem(chunk_size=2000, chunk_overlap=400)

# Increase retrieval documents
# (modify k in self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 10}))
```

### Memory Optimization

```python
# Clear unused documents
rag.clear_documents()

# Don't load huge PDFs (100+ pages)
# Split them manually and load in batches
```

## Troubleshooting

### "Connection refused" (Ollama)

```
Error: Could not connect to Ollama at http://localhost:11434
```

**Solution:**
```bash
ollama serve  # Start Ollama in another terminal
```

### "Model not found" 

```
Error: model 'mistral' not found
```

**Solution:**
```bash
ollama pull mistral
ollama pull nomic-embed-text
```

### Slow Embedding

**Cause**: First time running with a new model  
**Solution**: Wait for first embedding, Ollama caches it

### Out of Memory

**Cause**: Large PDF or large chunk size with limited RAM  
**Solution**: 
- Reduce chunk_size  
- Load fewer documents at once
- Use smaller model

### Chroma Database Corruption

**Solution:**
```bash
rm -rf chroma_db/  # Delete database
```

Then reload documents (will recreate database).

## Advanced Usage

### Custom Prompts

Edit the template in `_build_rag_chain()`:

```python
template = """You are an expert on the documents provided.

Context:
{context}

Question: {question}

Provide a detailed answer with citations."""
```

### Different Retrievers

Modify retriever in `add_documents()`:

```python
# MMR (Maximal Marginal Relevance)
self.retriever = self.vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 10}
)

# Different k value
self.retriever = self.vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 10}  # Retrieve more documents
)
```

### Custom Embeddings

Replace OllamaEmbeddings with:

```python
from langchain_community.embeddings import HuggingFaceEmbeddings

self.embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

## Comparison with Cloud RAG

| Feature | Local RAG | Cloud RAG |
|---------|-----------|-----------|
| Privacy | ✓ Local data | ✗ Sent to cloud |
| Cost | ✓ Free | ✗ Per API call |
| Speed | ✓ Fast for small docs | ? Depends on network |
| Offline | ✓ Works offline | ✗ Needs internet |
| Storage | ✓ On disk | ~ Cloud storage |
| Control | ✓ Full control | ✗ Limited |

## Resources

- [LangChain Documentation](https://python.langchain.com)
- [Chroma Documentation](https://docs.trychroma.com)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [HuggingFace Models](https://huggingface.co/models)

## Next Steps

1. ✅ Run interactive demo: `python rag_system.py`
2. ✅ Load your own PDF: `load my_document.pdf`
3. ✅ Ask questions: `query What is this document about?`
4. ✅ Explore programmatic API
5. ✅ Add custom tools or chains

## License

Open source - Educational use

---

**Framework**: LangChain  
**Vector DB**: Chroma  
**Embeddings**: Ollama (nomic-embed-text)  
**LLM**: Ollama (mistral)  
**License**: Open Source
