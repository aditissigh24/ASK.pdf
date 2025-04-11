from langchain_community.document_loaders import PyPDFLoader
import os

def load_documents(folder_path):
    """Loads all PDF documents from a folder with page information."""
    documents = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            file_path = os.path.join(folder_path, file)
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            
            # Add source filename to metadata
            for page in pages:
                page.metadata["source"] = file
                page.metadata["page_number"] = page.metadata.get("page", 0) + 1
                
            documents.extend(pages)
    return documents