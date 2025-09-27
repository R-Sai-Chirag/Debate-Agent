from src.graph import agent

topic = "Pineapple belongs on pizza"

initial_state = {
    "topic": topic,
    "arguments_for": [],
    "arguments_against": [],
    "research_summaries": [],
    "turn_count": 0,
    "current_turn": "agent_for",
    "debate_over": False,
    "final_judgement": None
}

print(f"🔥 DEBATE STARTING 🔥")
print(f"Topic: {topic}\n")

# Use the .stream() method to get outputs as they happen
for event in agent.stream(initial_state, {"recursion_limit": 30}):
    node_name = list(event.keys())[0]
    node_output = event[node_name]

    print(f"--- Executing Node: {node_name} ---")

    if node_name == "agent_for":
        new_argument = node_output.get("arguments_for", [])[-1].content
        print(f"✅ FOR says: {new_argument}\n")
    
    elif node_name == "agent_against":
        new_argument = node_output.get("arguments_against", [])[-1].content
        print(f"❌ AGAINST says: {new_argument}\n")
        
    elif node_name == "judge":
        final_judgement = node_output.get("final_judgement")
        print(f"⚖️ JUDGE's Verdict: {final_judgement}\n")
    
    elif node_name == "Research_for":
        print("🧠 Researching for 'agent_for'...\n")
        
    elif node_name == "Research_against":
        print("🧠 Researching for 'agent_against'...\n")

print("🏁 DEBATE CONCLUDED 🏁")

