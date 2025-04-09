from __future__ import annotations
from openai import OpenAI
import os
import copy
from dotenv import load_dotenv

class Prompter:
    """
    Prompter class to handle the generation of prompts
    """

    def __init__(self, id: int, model_name: str, seed: int, temperature: float, max_tokens: int) -> None:
        load_dotenv()
        self.id = id
        self.model_name = model_name
        self.seed = seed
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
        self._system = (
            f"You are an LLM agent, and you will now be able to converse with another LLM agent. "
            "Your aim is to use the discussion to figure out what model the other agent is. "
            "You will now be able to ask the other agent questions and/or perform discussions, and you will be able to answer questions that the other agent asks. "
            "Remember that the other agent is trying to also guess which model you are. It is also an LLM."
        )
        self._memory = [{
            "role": "system",
            "content": self._system
        }]

    def gen(self) -> str:
        """
        Prompt an LLM using the OpenRouter API
        """

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=self._memory,
            temperature=self.temperature,
            seed=self.seed,
            max_tokens=self.max_tokens
        )

        # Check if the response is valid
        if not response.choices or not response.choices[0].message:
            raise ValueError(f"ERROR: {response}")

        return response.choices[0].message.content
    
    def discussion_prompt(self, opposition: Prompter) -> str:
        """
        Constructs and returns the prompt needed to start/continue a discussion between the agents.

        Arguments:
            opposition: The other agent to discuss with.
        """
        new_chat = self.gen()
        self._memory.append({"role": f"assistant", "content": new_chat})
        opposition._memory.append({"role": f"user", "content": new_chat})
        return new_chat
    
    def conclusion_prompt(self) -> str:
        """
        Constructs and returns the prompt needed to conclude the discussion between the agents, and get the agents to guess the other agent's model.
        """

        self._memory.append({
            "role": "system",
            "content": (
                "Based on this conversation, please now conclude which model the other agent is. Explain your reasoning. Your answer should be in the following format:\n"
                "1. <model_name>\n"
                "2. <reasoning>\n"
            )
        })

        return self.gen()
    
    def convert_memory_to_json(self) -> str:
        """
        Converts the memory to a json object
        """
        mem_to_save = copy.deepcopy(self._memory)
        for i in range(len(self._memory)):  
            if mem_to_save[i]["role"] == "assistant":
                mem_to_save[i]["role"] = f"agent_{self.id}"
            elif mem_to_save[i]["role"] == "user":
                mem_to_save[i]["role"] = f"agent_{(1 + self.id) % 2}"

        mem_to_save = [msg for msg in mem_to_save if msg.get("role") != "system"]

        return mem_to_save