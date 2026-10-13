from AI.prompts.fsm_schema import fsm_schema
from AI.prompts.functions import functions
from AI.prompts.instructions import instructions

with open("AI/prompts/system_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()