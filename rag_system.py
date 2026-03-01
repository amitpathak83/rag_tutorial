#!/usr/bin/env python3
"""
Local RAG Implementation using LangChain, Chroma, and Ollama
Retrieval-Augmented Generation for PDF documents

Python 3.12+ compatible version with proper Pydantic v2 support.
"""

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
import logging
import os
import sys
import warnings
from pathlib import Path
from typing import List, Optional

# Suppress any deprecation warnings for cleaner output
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Set environment variable for Chroma to avoid resource warnings
os.environ['CHROMA_SERVER_NOFILE'] = '65536'


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# RAG SYSTEM CLASS
# ============================================================================

class PDFRAGSystem:
    """
    Retrieval-Augmented Generation system for PDF documents.
    Uses Chroma for vector storage and Ollama for embeddings and generation.
    """

    def __init__(
        self,
        model_name: str = "llama3.2",
        embedding_model: str = "nomic-embed-text",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        db_path: str = "./chroma_db"
    ):
        """
        Initialize the RAG system.

        Args:
            model_name: Name of the Ollama model for generation
            embedding_model: Name of the Ollama model for embeddings
            chunk_size: Size of chunks for document splitting
            chunk_overlap: Overlap between chunks
            db_path: Path to store Chroma database
        """
        self.model_name = model_name
        self.embedding_model = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.db_path = db_path

        # Initialize components
        self.embeddings = OllamaEmbeddings(model=embedding_model)
        self.llm = ChatOllama(model=model_name, temperature=0.3)
        self.vector_store = None
        self.retriever = None
        self.rag_chain = None

        # Load existing vector store if available
        self._load_vector_store()

        logger.info(
            f"RAG System initialized with model={model_name}, embeddings={embedding_model}")

    def _load_vector_store(self):
        """Load existing Chroma vector store if it exists."""
        if os.path.exists(self.db_path):
            try:
                self.vector_store = Chroma(
                    persist_directory=self.db_path,
                    embedding_function=self.embeddings
                )
                logger.info(
                    f"Loaded existing vector store from {self.db_path}")
            except Exception as e:
                logger.warning(f"Could not load existing vector store: {e}")
                self.vector_store = None

    def load_pdf(self, pdf_path: str) -> List[Document]:
        """
        Load a PDF file and extract documents.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            List of Document objects
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        logger.info(f"Loading PDF: {pdf_path}")

        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        logger.info(f"Loaded {len(documents)} pages from {pdf_path}")
        return documents

    def load_pdfs(self, pdf_dir: str) -> List[Document]:
        """
        Load multiple PDFs from a directory.

        Args:
            pdf_dir: Directory containing PDF files

        Returns:
            List of Document objects
        """
        documents = []
        pdf_path = Path(pdf_dir)

        if not pdf_path.exists():
            raise FileNotFoundError(f"Directory not found: {pdf_dir}")

        pdf_files = list(pdf_path.glob("*.pdf"))
        logger.info(f"Found {len(pdf_files)} PDF files in {pdf_dir}")

        for pdf_file in pdf_files:
            try:
                docs = self.load_pdf(str(pdf_file))
                documents.extend(docs)
            except Exception as e:
                logger.error(f"Error loading {pdf_file}: {e}")

        return documents

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks.

        Args:
            documents: List of documents

        Returns:
            List of split documents
        """
        logger.info(f"Splitting {len(documents)} documents...")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

        split_docs = splitter.split_documents(documents)
        logger.info(f"Split into {len(split_docs)} chunks")

        return split_docs

    def add_documents(self, documents: List[Document], pdf_name: str = "document"):
        """
        Add documents to the vector store.

        Args:
            documents: List of documents to add
            pdf_name: Name of the PDF for metadata
        """
        # Add metadata if not already present
        for doc in documents:
            if "source" not in doc.metadata:
                doc.metadata["source"] = pdf_name

        logger.info(f"Processing {len(documents)} documents...")

        # Split documents
        split_docs = self.split_documents(documents)

        # Create or update vector store
        if self.vector_store is None:
            logger.info("Creating new vector store...")
            self.vector_store = Chroma.from_documents(
                documents=split_docs,
                embedding=self.embeddings,
                persist_directory=self.db_path
            )
        else:
            logger.info("Adding documents to existing vector store...")
            self.vector_store.add_documents(split_docs)
            self.vector_store.persist()

        # Set up retriever
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )

        # Build RAG chain
        self._build_rag_chain()

        logger.info("Documents added successfully")

    def _build_rag_chain(self):
        """Build the RAG chain for question answering."""
        if self.retriever is None:
            raise ValueError("No retriever available. Add documents first.")

        # Define the RAG prompt
        template = """You are a helpful assistant answering questions based on the provided documents.

Context from documents:
{context}

Question: {question}

Answer based on the context above. If the answer is not in the context, say so clearly.
Provide a clear, concise answer."""

        prompt = ChatPromptTemplate.from_template(template)

        # Build the chain
        self.rag_chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
        )

        logger.info("RAG chain built successfully")

    def query(self, question: str, with_context: bool = False) -> str:
        """
        Answer a question using the RAG system.

        Args:
            question: The question to answer
            with_context: Whether to include source context in response

        Returns:
            The answer
        """
        if self.rag_chain is None:
            raise ValueError("No RAG chain available. Add documents first.")

        logger.info(f"Querying: {question}")

        # Get the answer
        response = self.rag_chain.invoke(question)
        answer = response.content if hasattr(
            response, "content") else str(response)

        if with_context:
            # Get source documents
            docs = self.vector_store.similarity_search(question, k=3)
            sources = set(doc.metadata.get("source", "Unknown")
                          for doc in docs)
            answer += f"\n\nSources: {', '.join(sources)}"

        return answer

    def get_retrieval_score(self, question: str, k: int = 3) -> List[tuple]:
        """
        Get similarity scores for a question.

        Args:
            question: The question
            k: Number of results to retrieve

        Returns:
            List of (document, score) tuples
        """
        if self.vector_store is None:
            raise ValueError("No vector store available. Add documents first.")

        results = self.vector_store.similarity_search_with_score(question, k=k)
        return results

    def list_documents(self) -> List[str]:
        """
        List all sources in the vector store.

        Returns:
            List of source names
        """
        if self.vector_store is None:
            return []

        # Get all unique sources from metadata
        sources = set()
        # Note: Chroma doesn't have a direct way to list all metadata,
        # so we retrieve a large number of documents
        try:
            results = self.vector_store.similarity_search("", k=1000)
            for doc in results:
                source = doc.metadata.get("source", "Unknown")
                sources.add(source)
        except:
            pass

        return sorted(list(sources))

    def clear_documents(self):
        """Clear all documents from the vector store."""
        import shutil

        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)
            self.vector_store = None
            self.retriever = None
            self.rag_chain = None
            logger.info("Vector store cleared")


# ============================================================================
# INTERACTIVE INTERFACE
# ============================================================================

def print_header():
    """Print application header."""
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                     LOCAL RAG SYSTEM - INTERACTIVE MODE                  ║
║           Retrieval-Augmented Generation for PDF Documents               ║
╚══════════════════════════════════════════════════════════════════════════╝

Using:
  - Vector DB: Chroma (Local, Open Source)
  - LLM: Ollama (Local Inference)
  - Framework: LangChain

Commands:
  load <path>         Load a PDF file
  load_dir <path>     Load PDFs from directory
  query <question>    Ask a question
  list                List loaded documents
  clear               Clear all documents
  help                Show this help
  quit                Exit

═══════════════════════════════════════════════════════════════════════════
    """)


def interactive_mode():
    """Run the RAG system in interactive mode."""
    print_header()

    rag = PDFRAGSystem()

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            # Parse commands
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else None

            if command == "quit":
                print("\nGoodbye!")
                break

            elif command == "help":
                print("""
Available Commands:
  load <path>         Load a PDF file (e.g., "load document.pdf")
  load_dir <path>     Load all PDFs from directory
  query <question>    Ask a question about loaded documents
  list                List all loaded document sources
  clear               Clear all documents from memory
  help                Show this help message
  quit                Exit the program

Example:
  load research_paper.pdf
  query What are the main findings?
  list
                """)

            elif command == "load":
                if not arg:
                    print("Usage: load <pdf_path>")
                    continue

                try:
                    documents = rag.load_pdf(arg)
                    rag.add_documents(
                        documents, pdf_name=os.path.basename(arg))
                    print(f"✓ Loaded {len(documents)} pages")
                except Exception as e:
                    print(f"✗ Error: {e}")

            elif command == "load_dir":
                if not arg:
                    print("Usage: load_dir <directory_path>")
                    continue

                try:
                    documents = rag.load_pdfs(arg)
                    rag.add_documents(documents, pdf_name=arg)
                    print(f"✓ Loaded {len(documents)} pages from directory")
                except Exception as e:
                    print(f"✗ Error: {e}")

            elif command == "query":
                if not arg:
                    print("Usage: query <question>")
                    continue

                if rag.rag_chain is None:
                    print("✗ No documents loaded. Use 'load' command first.")
                    continue

                print("\nSearching documents...")
                try:
                    answer = rag.query(arg, with_context=True)
                    print(f"\nAnswer:\n{answer}\n")
                except Exception as e:
                    print(f"✗ Error: {e}")

            elif command == "list":
                sources = rag.list_documents()
                if sources:
                    print("\nLoaded Documents:")
                    for source in sources:
                        print(f"  - {source}")
                else:
                    print("No documents loaded")

            elif command == "clear":
                rag.clear_documents()
                print("✓ Vector store cleared")

            else:
                # Treat as a question if no documents are loaded
                if rag.rag_chain is None:
                    print("✗ No documents loaded. Use 'load' command first.")
                else:
                    try:
                        answer = rag.query(user_input, with_context=True)
                        print(f"\nAnswer:\n{answer}\n")
                    except Exception as e:
                        print(f"✗ Error: {e}")

        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Local RAG System")
    parser.add_argument("--pdf", help="Path to PDF file to load")
    parser.add_argument("--query", help="Question to ask")
    parser.add_argument("--dir", help="Directory with PDFs to load")
    parser.add_argument("--model", default="llama3.2",
                        help="Ollama model to use")
    parser.add_argument("--embedding-model",
                        default="nomic-embed-text", help="Embedding model")

    args = parser.parse_args()

    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                     LOCAL RAG SYSTEM                                     ║
║        Retrieval-Augmented Generation using LangChain + Chroma           ║
╚══════════════════════════════════════════════════════════════════════════╝

Make sure Ollama is running:
  $ ollama serve

Download required models (if not already downloaded):
  $ ollama pull mistral
  $ ollama pull nomic-embed-text

═══════════════════════════════════════════════════════════════════════════
    """)

    # Initialize RAG system
    rag = PDFRAGSystem(model_name=args.model,
                       embedding_model=args.embedding_model)

    # Load PDF if provided
    if args.pdf:
        try:
            documents = rag.load_pdf(args.pdf)
            rag.add_documents(documents, pdf_name=os.path.basename(args.pdf))
            print(f"✓ Loaded PDF: {args.pdf}\n")
        except Exception as e:
            print(f"✗ Error loading PDF: {e}\n")

    # Load directory if provided
    if args.dir:
        try:
            documents = rag.load_pdfs(args.dir)
            rag.add_documents(documents, pdf_name=args.dir)
            print(f"✓ Loaded PDFs from: {args.dir}\n")
        except Exception as e:
            print(f"✗ Error loading directory: {e}\n")

    # Answer query if provided
    if args.query:
        if rag.rag_chain is None:
            print("✗ No documents loaded. Use --pdf or --dir to load documents first.")
        else:
            try:
                answer = rag.query(args.query, with_context=True)
                print(f"\nQ: {args.query}\nA: {answer}\n")
            except Exception as e:
                print(f"✗ Error: {e}\n")
        sys.exit(0)

    # Interactive mode
    interactive_mode()
