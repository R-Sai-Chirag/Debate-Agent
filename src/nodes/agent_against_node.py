from src.chains.agent_against_chain import rebuttle_against_chain
from langchain_core.messages import HumanMessage
from src.state import Agentstate

def against_agent(state:Agentstate):
    """
    Generates a rebuttal against the motion using the last 'for' argument 
    and the latest research summary. Consumes one research entry and 
    returns a partial state update with the new 'against' argument and 
    the updated research list.
    """

    topic=state["topic"]
    argument=state["arguments_for"][-1].content
    research_summary=state["research_summary"][-1].content if state["research_summary"] else " "

    rebuttle=rebuttle_against_chain.invoke({"topic":topic,"opponent_last_argument":argument,"research_summary":research_summary})
    updated_research_summary=list(state["research_summary"])

    if updated_research_summary:
        updated_research_summary.pop()

    return {"arguments_against":[HumanMessage(content=rebuttle.content)],"research_summary":updated_research_summary}