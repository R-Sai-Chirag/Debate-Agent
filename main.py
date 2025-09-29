from src.graph import agent 
import streamlit as st
import time

st.set_page_config(layout="wide", page_title="AI Debate Application")

st.title("🤖 LM Debate Arena")

topic = st.text_input("Enter The Debate Topic:", "Which is better: Marvel or DC?")
num_of_turns_per_side = st.slider("Enter The Number Of Turns Per Side:", min_value=1, max_value=3, value=2)

# --- Initialize Session State ---
if "debate_transcript" not in st.session_state:
    st.session_state.debate_transcript = []
if "for_questions" not in st.session_state:
    st.session_state.for_questions = []
if "against_questions" not in st.session_state:
    st.session_state.against_questions = []
if "verdict" not in st.session_state:
    st.session_state.verdict = None # Initialize as None

# --- UI Layout ---
col1, col2, col3 = st.columns([1, 2.5, 1])

with col1:
    st.header("FOR ✅ \nRESEARCH QUESTIONS:")
    for_sidebar = st.container(height=600, border=True)

with col2:
    st.header("Debate Arena!")
    debate_area = st.container(height=600, border=True)
    debate_placeholder = debate_area.empty()

with col3:
    st.header("AGAINST ❌ \nRESEARCH QUESTIONS:")
    against_sidebar = st.container(height=600, border=True)

# --- Main Logic ---
if st.button("Start Debate", type="primary"):
    # Clear state from previous runs
    st.session_state.debate_transcript = []
    st.session_state.for_questions = []
    st.session_state.against_questions = []
    st.session_state.verdict = None
    debate_placeholder.empty()
    for_sidebar.empty()
    against_sidebar.empty()

    initial_state = {
        "topic": topic,
        "arguments_for": [],
        "arguments_against": [],
        "research_summary": [],
        "current_turn": "agent_for",
        "turn_count": 0,
        "max_turns": num_of_turns_per_side,
        "final_judgement": "",
        "research_for_questions": [],
        "research_against_questions": [],
    }

    with st.spinner("The Debate is in progress..."):
        try:
            for event in agent.stream(initial_state, {"recursion_limit": 30}):
                node_name = list(event.keys())[0]
                node_output = event[node_name]

                print(f"--- Event from Node: {node_name} ---")
                print(f"Node Output: {node_output}\n")

                if "Research_for" in node_name:
                    questions = node_output.get("research_for_questions", [])
                    st.session_state.for_questions.extend(questions)
                    with for_sidebar:
                        st.expander("Research Questions:", expanded=True).markdown("\n".join(f"- {q}" for q in st.session_state.for_questions))

                elif "Research_against" in node_name:
                    questions = node_output.get("research_against_questions", [])
                    st.session_state.against_questions.extend(questions)
                    with against_sidebar:
                        st.expander("Research Questions:", expanded=True).markdown("\n".join(f"- {q}" for q in st.session_state.against_questions))

                elif "agent_for" in node_name:
                    if node_output.get("arguments_for"):
                        new_argument = node_output.get("arguments_for")[-1].content
                        st.session_state.debate_transcript.append(f"**✅ FOR says:**\n\n{new_argument}")
                        # --- PROBLEM CODE REMOVED ---
                        time.sleep(1)

                elif "agent_against" in node_name:
                    if node_output.get("arguments_against"):
                        new_argument = node_output.get("arguments_against")[-1].content
                        st.session_state.debate_transcript.append(f"**❌ AGAINST says:**\n\n{new_argument}")
                        # --- PROBLEM CODE REMOVED ---
                        time.sleep(1)

                elif "judge" in node_name:
                    if node_output.get("final_judgement"):
                        st.session_state.verdict = node_output.get("final_judgement")

                # This is the ONLY update call for the main debate area.
                # It runs after every event to keep the display in sync.
                debate_placeholder.markdown("\n\n---\n\n".join(st.session_state.debate_transcript), unsafe_allow_html=True)

            st.success("Debate Concluded!")
        
        except Exception as e:
            st.error(f"An error occurred during the debate: {e}")

    with st.spinner("Evaluating The Winner..."):
        if st.session_state.verdict:
            st.success(f"**⚖️ JUDGE's Verdict:**\n\n{st.session_state.verdict}")