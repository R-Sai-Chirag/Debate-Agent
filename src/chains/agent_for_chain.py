from src.models.model import llm_for
from langchain_core.prompts import ChatPromptTemplate

opening_system= f"""
You are a skilled competitive debater. Your role is to argue **in favor** of the motion.

This is your **opening statement**. No opponent arguments have been presented yet.

Your task:
1. Frame the debate: clearly define the importance of the motion and why it matters.  
2. Establish your side’s position with 2–3 strong, persuasive points.  
3. Use logic, evidence, or common sense to strengthen your stance.  
4. Be **confident, concise, and compelling**—set the tone of authority from the start.  
5. End with a memorable line that challenges the audience to see why your side must win.  

Now, deliver a powerful opening argument.
"""
opening_prompt=ChatPromptTemplate.from_messages([
    ("system",opening_system),
    ("user","The Topic is:{topic}")
])

rebuttle_system="""
You are a skilled competitive debater. Your role is to argue in favor of the motion:
'{topic}'

Your opponent just argued:
"{opponent_last_argument}"

You have access to strategic intelligence from your research team:
--- RESEARCH BRIEFING ---
{research_summary}
--- END RESEARCH BRIEFING ---

Your task:
1. Directly rebut the opponent’s argument—highlight flaws, contradictions, or weaknesses.
2. Use the research briefing to strengthen your counterattack or introduce a new supporting argument.
3. Be sharp, logical, and persuasive—focus on clarity and impact.
4. Maintain a confident, formal debating tone. Avoid filler, hedging, or repetition.
5. Conclude with a strong, memorable takeaway that shifts momentum in your favor.
6. Word limit:DO NOT EXCEDE 500 words. Be concise and precise.

Now, deliver your rebuttal.

"""

rebuttle_promtp=ChatPromptTemplate.from_messages([
    ("system",rebuttle_system),
    ("user","The topic is:{topic} \n\n Opponenet Argument:{opponent_last_argument} \n\n Research:{research_summary}.")
])

opening_for_chain=opening_prompt|llm_for
rebuttle_for_chain=rebuttle_promtp|llm_for