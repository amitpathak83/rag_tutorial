#!/usr/bin/env python3
"""
RAG System Demo
Demonstrates how to use the local RAG system programmatically.
"""

import asyncio
from rag_system import PDFRAGSystem


def demo_basic_usage():
    """Demonstrate basic usage of the RAG system."""
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║              RAG SYSTEM - BASIC USAGE DEMO                               ║
╚══════════════════════════════════════════════════════════════════════════╝

This demo shows how to use the RAG system programmatically.

Requirements:
  - Ollama running: ollama serve
  - Models downloaded: ollama pull mistral mistral nomic-embed-text
  - A PDF file to load

═══════════════════════════════════════════════════════════════════════════
    """)


def example_1_basic_rag():
    """Example 1: Basic RAG workflow."""
    print("\n📋 Example 1: Basic RAG Workflow")
    print("-" * 70)

    print("""
from rag_system import PDFRAGSystem

# 1. Initialize the RAG system
rag = PDFRAGSystem(
    model_name="mistral",
    embedding_model="nomic-embed-text",
    chunk_size=1000,
    chunk_overlap=200,
    db_path="./chroma_db"
)

# 2. Load a PDF
documents = rag.load_pdf("path/to/document.pdf")

# 3. Add documents to vector store
rag.add_documents(documents, pdf_name="document.pdf")

# 4. Query the system
answer = rag.query("What is the main topic of this document?")
print(answer)
    """)


def example_2_batch_processing():
    """Example 2: Batch processing multiple PDFs."""
    print("\n📋 Example 2: Batch Processing Multiple PDFs")
    print("-" * 70)

    print("""
from rag_system import PDFRAGSystem

rag = PDFRAGSystem()

# Load multiple PDFs from a directory
documents = rag.load_pdfs("./pdf_documents/")

# Add all at once
rag.add_documents(documents)

# Query
answer = rag.query("Summarize the key findings")
print(answer)
    """)


def example_3_retrieval_scores():
    """Example 3: Get retrieval scores."""
    print("\n📋 Example 3: Retrieval with Similarity Scores")
    print("-" * 70)

    print("""
from rag_system import PDFRAGSystem

rag = PDFRAGSystem()
rag.add_documents(documents)

# Get documents with similarity scores
question = "What are the main conclusions?"
results = rag.get_retrieval_score(question, k=3)

for doc, score in results:
    print(f"Score: {score:.4f}")
    print(f"Content: {doc.page_content[:200]}...")
    print()
    """)


def example_4_custom_configuration():
    """Example 4: Custom configuration."""
    print("\n📋 Example 4: Custom Configuration")
    print("-" * 70)

    print("""
from rag_system import PDFRAGSystem

# Use custom settings
rag = PDFRAGSystem(
    model_name="neural-chat",        # Faster model
    embedding_model="nomic-embed-text",
    chunk_size=500,                  # Smaller chunks
    chunk_overlap=100,               # Less overlap
    db_path="./my_rag_db"            # Custom database path
)

# Load and query
documents = rag.load_pdf("document.pdf")
rag.add_documents(documents)
answer = rag.query("Who are the authors?")
    """)


def example_5_listing_documents():
    """Example 5: List and manage documents."""
    print("\n📋 Example 5: Listing and Managing Documents")
    print("-" * 70)

    print("""
from rag_system import PDFRAGSystem

rag = PDFRAGSystem()

# Load multiple documents
documents1 = rag.load_pdf("paper1.pdf")
rag.add_documents(documents1, pdf_name="paper1.pdf")

documents2 = rag.load_pdf("paper2.pdf")
rag.add_documents(documents2, pdf_name="paper2.pdf")

# List all loaded documents
sources = rag.list_documents()
print("Loaded sources:")
for source in sources:
    print(f"  - {source}")

# Clear all
rag.clear_documents()
    """)


def example_6_context_aware_queries():
    """Example 6: Context-aware queries."""
    print("\n📋 Example 6: Context-Aware Queries")
    print("-" * 70)

    print("""
from rag_system import PDFRAGSystem

rag = PDFRAGSystem()
rag.add_documents(documents)

# Get answer with source context
answer = rag.query(
    "What are the limitations mentioned?",
    with_context=True
)
print(answer)

# Output includes:
# - Direct answer based on LLM
# - Source documents cited
    """)


def print_api_reference():
    """Print API reference."""
    print("\n📚 API Reference")
    print("-" * 70)

    print("""
PDFRAGSystem Class
==================

__init__(model_name, embedding_model, chunk_size, chunk_overlap, db_path)
  Initialize the RAG system with specified parameters.

load_pdf(pdf_path) -> List[Document]
  Load a single PDF file and extract its content.

load_pdfs(pdf_dir) -> List[Document]
  Load all PDF files from a directory.

split_documents(documents) -> List[Document]
  Split documents into chunks (called automatically by add_documents).

add_documents(documents, pdf_name)
  Add documents to the vector store and build RAG chain.

query(question, with_context=False) -> str
  Answer a question using the RAG system.

get_retrieval_score(question, k=3) -> List[tuple]
  Get similarity scores for retrieved documents.

list_documents() -> List[str]
  List all loaded document sources.

clear_documents()
  Clear all documents from the vector store.
    """)


def print_command_reference():
    """Print interactive command reference."""
    print("\n🎮 Interactive Commands")
    print("-" * 70)

    print("""
load <path>
  Load a single PDF file
  Example: load research_paper.pdf

load_dir <path>
  Load all PDFs from a directory
  Example: load_dir ./documents/

query <question>
  Ask a question about loaded documents
  Example: query What are the main findings?

list
  List all loaded document sources

clear
  Remove all documents from memory

help
  Show help information

quit
  Exit the program

Note: Any text entered that's not a command will be treated as a query.
    """)


def print_setup_guide():
    """Print setup guide."""
    print("\n⚙️  Setup Guide")
    print("-" * 70)

    print("""
1. Install Ollama
   - macOS: brew install ollama
   - Or download: https://ollama.ai

2. Start Ollama server (in a separate terminal)
   $ ollama serve

3. Download required models
   $ ollama pull mistral
   $ ollama pull nomic-embed-text

4. Install Python dependencies
   $ pipenv install
   $ pipenv shell

5. Run the RAG system
   $ python rag_system.py                    # Interactive mode
   $ python rag_system.py --pdf document.pdf # Load and query
   $ python rag_system.py --dir ./documents/ # Load directory

Note: Embeddings model (nomic-embed-text) is smaller and faster
      for local RAG. It's optimized for retrieval tasks.
    """)


def main():
    """Main demo function."""
    demo_basic_usage()

    print("\n" + "="*70)
    print("AVAILABLE EXAMPLES")
    print("="*70)

    # Show all examples
    example_1_basic_rag()
    example_2_batch_processing()
    example_3_retrieval_scores()
    example_4_custom_configuration()
    example_5_listing_documents()
    example_6_context_aware_queries()

    # Show references
    print_api_reference()
    print_command_reference()
    print_setup_guide()

    print("\n" + "="*70)
    print("GETTING STARTED")
    print("="*70)

    print("""
Quick Start (Interactive Mode):
  1. Make sure Ollama is running: ollama serve
  2. Run: python rag_system.py
  3. Type: load your_document.pdf
  4. Type: query Your question here?
  5. Type: quit to exit

Command Line Usage:
  python rag_system.py --pdf document.pdf --query "Your question"
  python rag_system.py --dir ./documents/ --query "Question about all docs"

Programmatic Usage:
  See examples above for how to use as a library in your code.

═══════════════════════════════════════════════════════════════════════════
    """)


if __name__ == "__main__":
    main()
