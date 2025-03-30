from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb

def generate_embeddings(texts):
    """Generate embeddings for given text chunks using SentenceTransformer."""
    model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return model.embed_documents([t.page_content for t in texts])

def store_embeddings(texts):
    """Store embeddings in ChromaDB vector database."""
    embeddings = generate_embeddings(texts)

    # Initialize ChromaDB client
    chroma_client = chromadb.PersistentClient(path="./chroma_db")

    # Create Chroma vector store
    vector_store = Chroma(collection_name="pdf_rag", embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"), client=chroma_client)

    # Add embeddings to the ChromaDB collection
    vector_store.add_texts(texts=[t.page_content for t in texts], embeddings=embeddings)

    return vector_store
