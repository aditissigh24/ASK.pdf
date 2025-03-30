from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
def generate_response(question, context):
    """Uses Gemini LLM to generate a response based on retrieved documents."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_API_KEY)  # You can also use "gemini-1.5-pro"

    messages = [
        SystemMessage(content="You are a document assistant."),
        HumanMessage(content=f"Context: {context}\n\nQuestion: {question}")
    ]
    
    return llm.invoke(messages)
