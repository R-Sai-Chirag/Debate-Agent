from src.chains.agent_for_chain import opening_for_chain,rebuttle_for_chain
from src.state import Agentstate
from langchain_core.messages import HumanMessage

def agent_for(state:Agentstate):
    """
    Generates an argument for the topic, either an opening statement or a rebuttal.
    It leverages the latest research summary if available and addresses the opponent's last argument.
    """
    topic=state["topic"]

    research_summary_content=""
    if state["research_summary"]:
        research_summary_content=state["research_summary"][-1].content

    opponent_last_argument=""
    if state["arguments_against"]:
        opponent_last_argument=state["arguments_against"][-1].content
    


    if opponent_last_argument:
        rebuttle=rebuttle_for_chain.invoke({"topic":topic,"opponent_last_argument":opponent_last_argument,"research_summary":research_summary_content})

    
    else:
        rebuttle=opening_for_chain.invoke({"topic":topic})

    updated_arguments_for = state["arguments_for"] + [HumanMessage(content=rebuttle.content)]

    return {"arguments_for":updated_arguments_for,"research_summary":[]}