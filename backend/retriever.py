import chromadb
from sentence_transformers import SentenceTransformer

def query_document(question, collection):
    """Find the most relevant text chunks based on user query with metadata."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode(question).tolist()
    
    # Query the collection
    results = collection.query(
        query_embeddings=[query_embedding], 
        n_results=5
    )
    
    # Debug
    print("Query results:", results.keys())
    if 'metadatas' in results:
        print("First metadata entry:", results['metadatas'][0][0] if results['metadatas'][0] else "No metadata")
    
    documents = []
    
    if results['documents'] and len(results['documents'][0]) > 0:
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            
            # Extract metadata if available
            meta = {}
            if 'metadatas' in results and results['metadatas'] and len(results['metadatas'][0]) > i:
                meta = results['metadatas'][0][i]
            
            # Create source info string
            source = meta.get('source', 'document') if meta else 'document'
            page = meta.get('page', 'unknown') if meta else 'unknown'
            source_info = f"[Source: {source}, Page: {page}]"
            
            # Calculate relevance score if available
            relevance = 1.0
            if 'distances' in results and results['distances'] and len(results['distances'][0]) > i:
                distance = results['distances'][0][i]
                relevance = 1.0 - min(distance, 1.0)
            
            documents.append({
                "text": doc, 
                "source_info": source_info, 
                "relevance": relevance
            })
    
    # Sort by relevance
    documents.sort(key=lambda x: x["relevance"], reverse=True)
    
    return documents