from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb

def generate_embeddings(texts):
    """Generate embeddings for given text chunks using SentenceTransformer."""
    model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return model.embed_documents([t.page_content for t in texts])

def store_embeddings(texts):
    """Store embeddings in ChromaDB vector database."""
    # Initialize ChromaDB client
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    # Get or create collection
    collection = chroma_client.get_or_create_collection("pdf_embeddings")
    
   # Prepare data for ChromaDB
    ids = []
    documents = []
    metadatas = []
    for i, text in enumerate(texts):
        ids.append(f"doc_{i}")
        documents.append(text.page_content)
        
        # Extract source and page info from metadata
        source = text.metadata.get("source", "document")
        page = text.metadata.get("page", 0)
        
        # Store metadata
        metadatas.append({
            "source": source,
            "page": str(page)  # Convert to string to ensure compatibility
        })

    # Generate embeddings
    embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    embeddings = embed_model.embed_documents(documents)
    
    # Add to collection
    collection.add(
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    return chroma_client