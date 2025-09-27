from src.models.model import llm_summarizer
from src.state import Agentstate
from langchain_core.prompts import ChatPromptTemplate


system="""
You are an expert debate summarizer. You will receive a **chunk of arguments** related to a debate topic. Your task is to **summarize this chunk** while retaining all critical claims, reasoning, evidence, and examples. Each chunk must be summarized in a way that:

1. Preserves **all key points and logical flow** from this chunk.
2. Is **concise, coherent, and readable**.
3. Does not omit or distort important details.
4. Uses a **neutral, formal tone** suitable for judging.
5. Can be **combined with other chunk summaries** to produce a complete overview of all arguments.

Input:
Topic: {topic}
argument:{arguments}

Output:
A clear, structured summary of this chunk that preserves the full reasoning and evidence.

"""

summarize_prompt=ChatPromptTemplate.from_messages([
    ("system",system),
    ("user","The topic is:{topic} \n\n Arguments:{arguments}.")
])

summarize_chain=summarize_prompt|llm_summarizer