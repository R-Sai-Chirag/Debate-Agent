from typing import TypedDict,Annotated,List
from langgraph.graph import add_messages

class Agentstate(TypedDict):
    topic:str
    arguments_for:Annotated[List,add_messages]
    arguments_against:Annotated[List,add_messages]
    turn_count:int
    current_turn:str
    debate_over:bool
    research_summary:Annotated[List,add_messages]
    final_judgement:str