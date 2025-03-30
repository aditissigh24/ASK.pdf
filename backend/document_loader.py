from langchain_community.document_loaders import PyPDFLoader
import os

def load_documents(folder_path):
    """Loads all PDF documents from a folder."""
    documents = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(folder_path, file))
            documents.extend(loader.load())  # Load all pages
    return documents
