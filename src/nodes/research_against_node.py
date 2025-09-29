from src.state import Agentstate
from langchain_tavily import TavilySearch
from langchain_core.messages import AIMessage
import re
from src.chains.research_against_chain import against_question_generator 

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

def research_against(state: Agentstate):
    """
    Generates research summaries to support the 'against' agent.
    """
    print("--- INSIDE research_against NODE ---")
    topic = state["topic"]
    opponent_argument = state["arguments_for"][-1].content if state["arguments_for"] else " "
    
    # Changed to get more results per query
    web_search = TavilySearch(max_results=2)

    # 1. Generate search questions
    questions_output = against_question_generator.invoke({
        "topic": topic,
        "opponent_argument": opponent_argument
    })

    questions = []
    if isinstance(questions_output, str):
        questions = [q.split(".", 1)[-1].strip() for q in questions_output.splitlines() if q.strip()]
    elif isinstance(questions_output, list):
        questions = questions_output

    
    questions_against= [q for q in questions if '?' in q]
    
    
    print(f"\n[DEBUG] Generated Questions: {questions_against}\n")

    
    research_summary_list = []
    if questions_against:
        for q in questions_against:
            
            search_result = web_search.invoke({"query": q})
            
            # DEBUG STEP 2: Check the raw search result
            
            
            if "results" in search_result and isinstance(search_result["results"], list):
                for res in search_result["results"]:
                    if res.get("content"):
                        cleaned_text=clean_text(res["content"])
                        research_summary_list.append(cleaned_text)

    # 3. Aggregate the results
    research_summary = "\n\n".join(research_summary_list)
    
    # DEBUG STEP 3: Check the final aggregated summary
    print(f"\n[DEBUG] Final Aggregated Summary: '{research_summary}'\n")

    return {"research_summary": [AIMessage(content=research_summary)],"research_against_questions":questions_against}