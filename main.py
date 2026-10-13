from AI.agent import Agent
from AI.prompts.functions import functions
from AI.fsm import FiniteStateMachine
from AI.prompts import prompts


agent = Agent(
    system_prompt=prompts.system_prompt,
    functions=functions,
    instruction_json=prompts.instructions,
    fsm=FiniteStateMachine(
        prompts.fsm_schema,
        "default"
    )
)