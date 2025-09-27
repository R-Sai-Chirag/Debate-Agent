# main.py (Refined)

from src.graph import agent 


topic = "Cats are better pets than dogs."
initial_state = {
    "topic": topic,
    "arguments_for": [],
    "arguments_against": [],
    "research_summary": [], 
    "turn_count": 0,
    "current_turn": "agent_for",
    "debate_over": False,
    "final_judgement": None
}

print(f"🔥 DEBATE STARTING 🔥")
print(f"Topic: {topic}\n")


try:
    for event in agent.stream(initial_state, {"recursion_limit": 30}):
        # Each 'event' is a dictionary with the node name as the key
        node_name = list(event.keys())[0]
        node_output = event[node_name]

        print(f"--- Executing Node: {node_name} ---\n\n")

        # Handle output from the 'agent_for' node
        if node_name == "agent_for":
            if node_output.get("arguments_for"):
                new_argument = node_output.get("arguments_for")[-1].content
                print(f"✅ FOR says: {new_argument}\n\n")
        
        # Handle output from the 'agent_against' node
        elif node_name == "agent_against":
            if node_output.get("arguments_against"):
                new_argument = node_output.get("arguments_against")[-1].content
                print(f"❌ AGAINST says: {new_argument}\n\n")
            
        # Handle output from the 'judge' node
        elif node_name == "judge":
            if node_output.get("final_judgement"):
                final_judgement = node_output.get("final_judgement")
                print(f"⚖️ JUDGE's Verdict: {final_judgement}\n\n")
        
                 
        # Handle output from the 'Research_against' node
        elif "Research" in node_name:
            summary_messages = node_output.get("research_summary", [])
            if summary_messages:
                full_summary = summary_messages[0].content
                # To keep the console tidy, you might still want to print just a snippet
                print(f"🧠 Research complete. Summary generated:\n'{full_summary[:250]}...'\n\n")
            else:
                print("🧠 Research node ran, but no summary was generated.\n\n")

except Exception as e:
    print(f"\nAn error occurred during the debate: {e}")

finally:
    print("🏁 DEBATE CONCLUDED 🏁")

