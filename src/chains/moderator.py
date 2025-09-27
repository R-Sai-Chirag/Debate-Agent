from src.state import Agentstate

def moderator(state:Agentstate):
    """
    Controls the flow of the debate by updating the turn and checking for termination.

    Steps:
    1. Increments the current turn count.
    2. If the turn count reaches or exceeds 12, terminates the debate.
    3. Otherwise, alternates the current turn between 'agent_for' and 'agent_against'.
    4. Returns the updated state with the next turn, updated turn count, and debate_over flag.

    Args:
        state (Agentstate): The current debate state containing 'turn_count',
                            'current_turn', and other metadata.

    Returns:
        dict: Partial state update containing:
            - 'current_turn' (str): The agent whose turn is next.
            - 'turn_count' (int): Updated turn count.
            - 'debate_over' (bool): Whether the debate should terminate.
    """
    
    turn_count=state["turn_count"]
    turn_count+=1

    if turn_count==2:
        print("---DEBATE TERMINATED TURN COUNT LIMIT REACHED---")
        return {"turn_count":turn_count,"debate_over":True}
    
    next_turn= "agent_against" if state["current_turn"]=="agent_for" else "agent_for"

    print(f"---CURRENT DEBATOR {next_turn}.(TURN COUNT:{turn_count}---)")

    return {"current_turn":next_turn,"turn_count":turn_count,"debate_over":False}