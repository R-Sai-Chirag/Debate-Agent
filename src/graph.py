from src.nodes.agent_for_node import agent_for
from src.nodes.agent_against_node import against_agent
from src.nodes.research_for_node import research_for
from src.nodes.research_against_node import research_against
from src.nodes.judge_node import judge
from src.chains.moderator import moderator
from src.state import Agentstate
from langgraph.graph import StateGraph,START,END

builder=StateGraph(Agentstate)

def route(state:Agentstate):
    """
    Routes the graph based on the moderator's decision.
    NOW INCLUDES A ROUTE TO THE JUDGE.
    """
    if state.get("debate_over"):
        print("---ROUTER: Debate is over, routing to JUDGE---")
        return "judge"
    
    if state.get("current_turn")=="agent_for":
        print("---ROUTER: Next debater is AGENT_FOR, routing to research_for---")
        return "Research_for"

    elif state.get("current_turn")=="agent_against":
        print("---ROUTER: Next debater is AGENT_AGAINST, routing to research_against---")
        return "Research_against"


builder.add_node("agent_for",agent_for)
builder.add_node("agent_against",against_agent)
builder.add_node("moderator",moderator)
builder.add_node("Research_for",research_for)
builder.add_node("Research_against",research_against)
builder.add_node("judge",judge)

builder.add_edge(START,"agent_for")
builder.add_edge("agent_for","moderator")
builder.add_conditional_edges("moderator",route,
                              {"judge":"judge","Research_for":"Research_for","Research_against":"Research_against"})
builder.add_edge("judge",END)
builder.add_edge("Research_for","agent_for")
builder.add_edge("Research_against","agent_against")
builder.add_edge("agent_against","moderator")

agent=builder.compile()

# Corrected code for src/graph.py
mermaid_string = agent.get_graph().draw_mermaid()
with open("debate_graph.mmd", "w") as f:
    f.write(mermaid_string)