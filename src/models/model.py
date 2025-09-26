from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()
import os
groq_api_key=os.getenv("GROQ_API_KEY")

llm_for=ChatGroq(model="openai/gpt-oss-120b",groq_api_key=groq_api_key)

llm_against=ChatGroq(model="llama-3.3-70b-versatile",groq_api_key=groq_api_key)