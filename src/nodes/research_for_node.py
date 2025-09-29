from src.chains.research_for_chain import for_question_generator
from src.state import Agentstate
from langchain_tavily import TavilySearch
from langchain_core.messages import AIMessage
from dotenv import load_dotenv
load_dotenv()
import re

def clean_text(text: str) -> str:
    """
    Cleans a string by removing URLs, markdown links, and extra whitespace.
    """
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    
    # Remove markdown-style links and images, e.g., [text](url) or ![alt](url)
    text = re.sub(r'\[!?.*?\]\(.*?\)', '', text)
    
    # Remove standalone markdown brackets, e.g., [Skip to content]
    text = re.sub(r'\[.*?\]', '', text)
    
    # Remove markdown headings and other symbols
    text = re.sub(r'#+\s*', '', text) # Headings
    text = re.sub(r'\*', '', text)    # Asterisks for bold/italics
    
    # Normalize whitespace and newlines
    text = re.sub(r'\s{2,}', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

def research_for(state: Agentstate):
    """
    Generates research summaries to support the 'for' agent by:
    1. Taking the latest argument from the 'against' agent.
    2. Creating multiple search questions via the question generator.
    3. Running each question through the web search tool.
    4. Aggregating results into a single research summary.

    Returns a partial state update containing the updated 'research_summary'.
    """
    print("--- INSIDE research_for NODE ---")
    topic = state["topic"]
    
    opponent_argument = state["arguments_against"][-1].content if state["arguments_against"] else " "
    

    web_search = TavilySearch(max_results=2)

    
    questions_output = for_question_generator.invoke({
        "topic": topic,
        "opponent_argument": opponent_argument
    })

    questions = []
    if isinstance(questions_output, str):
        questions = [q.split(".", 1)[-1].strip() for q in questions_output.splitlines() if q.strip()]
    elif isinstance(questions_output, list):
        questions = questions_output

    
    questions_for= [q for q in questions if '?' in q]
    
    print(f"\n[DEBUG] Generated Questions: {questions_for}\n")

    
    research_summary_list = []
    if questions_for:
        for q in questions_for:
            
            search_result = web_search.invoke({"query": q})
            
            
            
            
            if "results" in search_result and isinstance(search_result["results"], list):
                for res in search_result["results"]:
                    if res.get("content"):
                        cleaned_content=clean_text(res["content"])
                        research_summary_list.append(cleaned_content)

    
    research_summary = "\n\n".join(research_summary_list)
    
    
    print(f"\n[DEBUG] Final Aggregated Summary: '{research_summary}'\n")

    return {"research_summary": [AIMessage(content=research_summary)], "research_for_questions": questions_for}