from src.chains.research_against_chain import against_question_generator
from src.state import Agentstate
from langchain_tavily import TavilySearch
from langchain_core.messages import AIMessage
from dotenv import load_dotenv
load_dotenv()

def research_against(state:Agentstate):
    """
    Generates research summaries to support the 'against' agent by:
    1. Taking the latest argument from the 'for' agent.
    2. Creating multiple search questions via the question generator.
    3. Running each question through the web search tool.
    4. Aggregating results into a single research summary.

    Returns a partial state update containing the updated 'research_summary'.
    """

    topic=state["topic"]
    opponent_argument=state["arguments_for"][-1].content if state["arguments_for"] else " "
    web_search=TavilySearch(max_result=1)

    questions_output=against_question_generator.invoke({"topic":topic,"opponent_argument":opponent_argument})

    questions=[]

    if isinstance(questions_output,str):
        questions=[q.split(".",1)[-1].strip() for q in questions_output.splitlines( ) if q.strip()]

    elif isinstance(questions_output, list):
        questions = questions_output

    research_summary_list=[]
    for q in questions:
        search_result=web_search.invoke({"query":q})
        if "result" in search_result and search_result["result"]:
            research_summary_list.append(search_result["result"])

    research_summary=" ".join(research_summary_list)

    print(f"---RESEARCH SUMMARY:{research_summary}")

    return{"research_summary":[AIMessage(content=research_summary)]}