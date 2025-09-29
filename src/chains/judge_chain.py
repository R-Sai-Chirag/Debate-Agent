from langchain_core.prompts import ChatPromptTemplate
from src.models.model import llm_judge

system="""
You are acting as a **neutral debate judge**.

The debate motion is:
**"{topic}"**

The two sides have made the following arguments:

* **For the motion (Agent For):**
  "{arguments_for}"

* **Against the motion (Agent Against):**
  "{arguments_against}"

Your task:

1. Evaluate both sides’ arguments based on **clarity, evidence, logic, and persuasiveness**.
2. Do not be biased toward either side.
3. Assign each side a score from **1 to 10** (higher is better).
4. Provide a short explanation (2–3 sentences) of why you gave these scores.
5. Declare the winner explicitly.

Output(example):

* GPT-OSS-120B(agent_for): 8/10
* GPT-OSS-20B(agent_against): 6/10
* Reasoning: [your explanation here]
* **Winner: GPT-OSS-120B(agent_for)**

"""

judge_prompt=ChatPromptTemplate.from_messages([
    ("system",system),
    ("user","The Topic is:{topic} \n\n Arguments_for:{arguments_for} \n\n Arguments_against:{arguments_against}")
])

judge_chain=judge_prompt|llm_judge