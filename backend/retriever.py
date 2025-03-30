import chromadb
from sentence_transformers import SentenceTransformer

def query_document(question, collection):
    """Find the most relevant text chunks based on user query using SentenceTransformer and ChromaDB."""
    model = SentenceTransformer('all-MiniLM-L6-v2')  # You can change the model if needed
    query_embedding = model.encode(question).tolist()  # Generate embedding for the query

    # Search for the most relevant documents in ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding], 
        n_results=3  # Retrieve top 3 most relevant results
    )

    return results['documents'][0] if results['documents'] else []
