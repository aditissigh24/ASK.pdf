import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from document_loader import load_documents
from embeddings import store_embeddings
from retriever import query_document
from llm import generate_response
from fastapi.middleware.cors import CORSMiddleware
import chromadb

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://askpdf-phi.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure the data folder exists
os.makedirs("data", exist_ok=True)

documents = []
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="pdf_embeddings")

# Keep track of whether documents have been uploaded
has_documents = False

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        """Uploads a PDF and processes embeddings with ChromaDB."""
        global documents, chroma_client, has_documents

        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        # Save the uploaded PDF
        file_path = f"data/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Load and store embeddings in ChromaDB
        documents = load_documents("data/")
        chroma_client = store_embeddings(documents)
        
        # Set flag indicating documents are available
        has_documents = True

        return {"message": f"{file.filename} uploaded and indexed successfully. You can now ask questions about this document."}
    except Exception as e:
        return {
            "error": str(e)
        }

@app.get("/ask/")
async def ask_question(question: str):
    """Answers user queries using the document context."""
    global has_documents
    
    # Check if this is the first interaction or no documents are uploaded
    if not has_documents or len(os.listdir("data")) == 0:
        return {
            "answer": {
                "content": "Welcome to the Document Assistant! Please upload a PDF document first so I can answer questions about it. Use the upload button to get started."
            }
        }
    
    # Normal processing for questions when documents are available
    context_docs = query_document(question, collection)
    
    if not context_docs:
        return {"answer": {"content": "I couldn't find relevant information in the uploaded documents to answer this question."}}
    
    response = generate_response(question, context_docs)
    
    return {"answer": response}

# Optional: Add an endpoint to check system status
@app.get("/status/")
async def check_status():
    """Check if documents have been uploaded."""
    if not has_documents or len(os.listdir("data")) == 0:
        return {"status": "waiting_for_documents", "message": "Please upload a document to get started."}
    else:
        doc_count = len(os.listdir("data"))
        return {"status": "ready", "document_count": doc_count, "message": "System is ready to answer questions."}