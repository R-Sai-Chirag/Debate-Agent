from src.state import Agentstate

def moderator(state:Agentstate):
    turn_count=state["turn_count"]
    turn_count+=1

    if turn_count>=12:
        print("---DEBATE TERMINATED TURN COUNT LIMIT REACHED---")
        return {"turn_count":turn_count,"debate_over":True}
    
    next_turn= "agent_against" if state["current_turn"]=="agent_for" else "agent_for"

    print(f"---CURRENT DEBATOR {next_turn}.(TURN COUNT:{turn_count}---)")

    return {"current_turn":next_turn,"turn_count":turn_count,"debate_over":False}