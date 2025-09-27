from src.models.model import llm_search
from langchain_core.prompts import ChatPromptTemplate

system="""
You are assisting a debate system. The debate motion is:

"{topic}"

The opponent (arguing in favor of the motion) just made this argument:
"{opponent_argument}"

Your task:
- Reframe the opponent’s claim into **3 to 5 precise, web-searchable questions** 
  that will provide evidence, criticisms, or drawbacks to undermine the opponent’s claim.

- Output only a numbered list of questions (no explanations).

- Each question should be short, factual, and open-ended (not yes/no).
"""

research_against_prompt=ChatPromptTemplate.from_messages([
    ("system",system),
    ("user","The Topic is:{topic} \n\n The opponent Argument:{opponent_argument}")
])

against_question_generator=research_against_prompt|llm_search