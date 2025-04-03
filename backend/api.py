import os
from fastapi import FastAPI, UploadFile, File
from document_loader import load_documents
from embeddings import store_embeddings
from retriever import query_document
from llm import generate_response
from fastapi.middleware.cors import CORSMiddleware
import chromadb

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Change to specific frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Ensure the data folder exists
os.makedirs("data", exist_ok=True)

documents = []
chroma_client = chromadb.PersistentClient(path="chroma_db")  # Store database persistently
collection = chroma_client.get_or_create_collection(name="pdf_embeddings")

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Uploads a PDF and processes embeddings with ChromaDB."""
    global documents, chroma_client

    # Save the uploaded PDF
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Load and store embeddings in ChromaDB
    documents = load_documents("data/")
    chroma_client = store_embeddings(documents)

    return {"message": f"{file.filename} uploaded and indexed successfully"}

@app.get("/ask/")
async def ask_question(question: str):
    """Answers user queries using the document context."""
    if not collection:
        return {"error": "No document uploaded yet"}
    
    context = query_document(question, collection)  # Fetch relevant context
    response = generate_response(question, context)  # Pass to LLM
    print(context)
    return {"answer": response}
