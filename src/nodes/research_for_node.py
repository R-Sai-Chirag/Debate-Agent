from src.chains.research_for_chain import for_question_generator
from src.state import Agentstate
from langchain_tavily import TavilySearch
from langchain_core.messages import AIMessage

def resesrch_for(state:Agentstate):
    """
    Generates research summaries to support the 'for' agent by:
    1. Taking the latest argument from the 'against' agent.
    2. Creating multiple search questions via the question generator.
    3. Running each question through the web search tool.
    4. Aggregating results into a single research summary.

    Returns a partial state update containing the updated 'research_summary'.
    """

    topic=state["topic"]
    opponent_argument=state["arguments_against"][-1].content if state["arguments_against"] else " "
    questions=[]
    web_search=TavilySearch(max_result=1)
    questions=for_question_generator.invoke({"topic":topic,"opponent_argument":opponent_argument})

    research_summary_list=[]
    for q in questions:
        search_result=web_search.invoke({"query":q})
        if "result" in search_result and search_result["result"]:
            research_summary_list.append(search_result["result"])

    research_summary=" ".join(research_summary_list)

    return {"research_summary":[AIMessage(content=research_summary)]}