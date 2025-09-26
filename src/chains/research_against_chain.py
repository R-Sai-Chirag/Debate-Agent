from src.models.model import llm_search
from langchain_core.prompts import ChatPromptTemplate

system="""
You are assisting a debate system. The debate motion is:

"{topic}"

The opponent (arguing in favor of the motion) just made this argument:
"{opponent_argument}"

Your task:
- Reframe the opponent’s claim into a **search question** that will yield 
  information useful for building counter-arguments **against the motion**.  
- The question must explicitly target **evidence, criticisms, or drawbacks** that undermine 
  the opponent’s claim.  
- Generate 3 to 5 precise, web-searchable questions targeting evidence,or drawbacks
  that weaken the opponent's argument. Output as a numbered list only.  
- Keep it short, factual, and open-ended (not yes/no).  

Output only the question.
"""

research_against_prompt=ChatPromptTemplate.from_messages([
    ("system",system),
    ("user","The Topic is:{topic} \n\n The opponent Argument:{opponent_argument}")
])

against_question_generator=research_against_prompt|llm_search