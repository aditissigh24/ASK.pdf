from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def generate_response(question, context_docs):
    """Uses Gemini LLM to generate a strictly document-grounded response with citations."""
    if not context_docs:
        return {"content": "I couldn't find relevant information in the uploaded documents to answer this question."}
    
    # Format context with source information
    formatted_context = ""
    for i, doc in enumerate(context_docs):
        formatted_context += f"\n\nEXCERPT {i+1} {doc['source_info']}:\n{doc['text']}"
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_API_KEY)
    
    system_prompt = """You are a document assistant that answers questions STRICTLY based on the provided document excerpts. 
    
    RULES:
    1. ONLY use information from the provided document excerpts to answer the question.
    2. If the information isn't in the provided excerpts, respond with: "The uploaded documents don't contain information to answer this question."
    3. NEVER use any external knowledge beyond what's in the provided excerpts.
    4. Include document citations in your answer (Source and Page number).
    5. Start your answer with "Based on the uploaded documents: "
    6. Only cite sources that you actually used in your answer.
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Document excerpts: {formatted_context}\n\nQuestion: {question}")
    ]
    
    response = llm.invoke(messages)
    return response