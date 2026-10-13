from AI import ai
from config.config import config
from AI.fsm import FiniteStateMachine
import json


class Agent:
    def __init__(self, *, system_prompt=None, functions=None, instruction_json=None, prefix_messages_count=1, fsm:FiniteStateMachine = None):
        self.model = ai.GetApi()
        self.system_prompt = {
            "role": "system",
            "content": system_prompt or "You are a helpful assistant. You will be given a user input and you will respond with a JSON object that contains the following fields: 'response' (a string containing your response to the user input), 'action' (a string indicating the action to take, if any), and 'data' (an optional object containing any additional data needed for the action). If no action is needed, set 'action' to 'none' and 'data' to an empty object."
        }
        self.compressed_history = {
            "role": "user",
            "content": ""
        }
        self.messages = []
        self.prefix_messages_count = prefix_messages_count
        self.functions = functions or {"schemas": [], "calls": {}}
        self.instruction_json = instruction_json or {}
        self.fsm = fsm

    def _Message(self, content, *, system_message: str = None, function_call: str = "none", model: str = config.AI_MODEL):
        message = {
            "role": "user",
            "content": f"<system>{system_message}</system>{content}" if system_message else content
        }
        payload = {
            "model": model,
            "messages": [self.system_prompt, self.compressed_history, *self.messages, message],
            "function_call": function_call,
            "functions": [] if function_call == "none" else self.functions["schemas"],
        }
        response = self.model.Message(payload)
        self.messages.append(message)
        self.messages.append(response.choices[0].message)
        return response

    def run(self, user_input: str, max_iteration_count: int = 50):
        iteration_count = 0
        break_flag = False
        self.system_prompt["content"] += f"\n<user_input>{user_input}</user_input>"

        while iteration_count < max_iteration_count:
            iteration_count += 1
            function_call_response = self._Message(self.instruction_json[self.fsm.current_state], function_call="auto").choices[0]

            if function_call_response.message.function_call:
                raw_args = function_call_response.message.function_call.arguments
                if isinstance(raw_args, dict):
                    kwargs = raw_args
                elif isinstance(raw_args, str) and raw_args.strip():
                    kwargs = json.loads(raw_args)
                else:
                    kwargs = {}
    
                function_call_result = self.functions["calls"][function_call_response.message.function_call.name](**kwargs)
    
                self.messages.append({
                    "role":"function",
                    "name": function_call_response.message.function_call.name,
                    "content": json.dumps(function_call_result)
                })
    
            if break_flag:
                break

        summary = self._Message(self.instruction_json["summary"], function_call="none").choices[0].message.content
        return summary

#Добавить обрезку истории сообщений, чтобы не перегружать контекст.
#Доделать промпты, стейты итд, то что задается в prompts.py 