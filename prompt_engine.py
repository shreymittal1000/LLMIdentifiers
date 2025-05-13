from __future__ import annotations
from openai import OpenAI
import os
import copy
from dotenv import load_dotenv

import maison_du_prompt

class Prompter:
    """
    Prompter class to handle the generation of prompts
    """

    def __init__(self, id: int, model_name: str, seed: int, temperature: float, max_tokens: int, system_prompt_version: str) -> None:
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
        self._system = maison_du_prompt.which_system_prompt(version=system_prompt_version)
        self._memory = [{
            "role": "system",
            "content": self._system
        }]

    def gen(self, resp_format: str = "text") -> str:
        """
        Prompt an LLM using the OpenRouter API

        Arguments:
            resp_format:
                The format of the response. Check the OpenRouter API docs for your model to see what is possible,
                but usually it is either "text" or "json_object".
        
        Returns:
            The response from the LLM.
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=self._memory,
            temperature=self.temperature,
            seed=self.seed,
            max_tokens=self.max_tokens,
            response_format={"type": resp_format},
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

        Returns:
            The response from the LLM. Should be some text.
        """
        new_chat = self.gen()
        self._memory.append({"role": f"assistant", "content": new_chat})
        opposition._memory.append({"role": f"user", "content": new_chat})
        return new_chat
    
    def guess_agent_prompt(self, version: str) -> str:
        """
        Constructs and returns the prompt needed to conclude the discussion between the agents, and get the agents to guess the other agent's model.

        Arguments:
            version: The version of the guess agent prompt to use.
        Returns:
            The response from the LLM. Should be a JSON object with "reasoning" and "guess" as keys.
        """

        self._final = maison_du_prompt.which_guess_prompt(version=version)
        self._memory.append({
            "role": "user",
            "content": self._final
        })

        return self.gen(resp_format="json_object")
    
    def staghunt_prompt(self, version: str) -> str:
        """
        Constructs and returns the prompt needed to play an economic game named "Stag Hunt" between the agents.
        For more information, see: https://en.wikipedia.org/wiki/Stag_hunt

        Arguments:
            version: The version of the stag hunt prompt to use.
        Returns:
            The response from the LLM. Should be a JSON object with "reasoning" and "action" as keys.
        """
        self._stagprompt = maison_du_prompt.which_staghunt_prompt(version=version)
        self._memory.append({
            "role": f"user",
            "content": self._stagprompt
        })

        return self.gen(resp_format="json_object")
    
    def chickengame_prompt(self, version: str) -> str:
        """
        Constructs and returns the prompt needed to play an economic game named "Chicken Game" between the agents.
        For more information, see: https://en.wikipedia.org/wiki/Chicken_(game)

        Arguments:
            version: The version of the chicken game prompt to use.
        Returns:
            The response from the LLM. Should be a JSON object with "reasoning" and "action" as keys.
        """
        self._chickenprompt = maison_du_prompt.which_chickengame_prompt(version=version)
        self._memory.append({
            "role": f"user",
            "content": self._chickenprompt
        })

        return self.gen(resp_format="json_object")
    
    def trustgame_prompt(self, version: str, trustor: bool, base_amount: int, multiplier: int, received: int = 0) -> str:
        """
        Constructs and returns the prompt needed to play an economic game named "Trust Game" between the agents.
        For more information, see: https://en.wikipedia.org/wiki/Trust_game

        Arguments:
            version: The version of the trust game prompt to use.
            trustor: A boolean indicating if the agent is the trustor (True) or the trustee (False).
            base_amount: The base amount of money that the truster can send to the trustee.
            multiplier: The multiplier that the trustee will apply to the amount sent by the truster.
            received: The amount of money that the trustee has received from the truster. Only used if trustor is False.
        Returns:
            The response from the LLM. Should be a JSON object with "reasoning" and "amount" as keys.
        """
        self._trustprompt = maison_du_prompt.which_trustgame_prompt(
            version=version,
            trustor=trustor,
            base_amount=base_amount,
            multiplier=multiplier,
            received=received
        )
        self._memory.append({
            "role": f"user",
            "content": self._trustprompt
        })

        return self.gen(resp_format="json_object")
    
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