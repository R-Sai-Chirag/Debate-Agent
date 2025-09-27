from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()
import os
groq_api_key=os.getenv("GROQ_API_KEY")

print("--MODELS INITIALIZED--")

llm_for=ChatGroq(model="gemma2-9b-it",groq_api_key=groq_api_key)

llm_against=ChatGroq(model="llama-3.1-8b-instant",groq_api_key=groq_api_key)

llm_search=ChatGroq(model="gemma2-9b-it",groq_api_key=groq_api_key)

llm_judge=ChatGroq(model="qwen/qwen3-32b",groq_api_key=groq_api_key)

llm_summarizer=ChatGroq(model="qwen/qwen3-32b",groq_api_key=groq_api_key)