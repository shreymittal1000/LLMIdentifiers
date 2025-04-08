import openai
import os
from dotenv import load_dotenv

class Prompter:
    """
    Prompter class to handle the generation of prompts
    """

    def __init__(self, model_name: str, seed: int, temperature: float = 0.7):
        load_dotenv()
        self.model_name = model_name
        self.seed = seed
        self.key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        self._memory = [
            {"system": "system", "content": f"""
                You are an LLM agent, and you will now be able to converse with another LLM agent. 
                Your aim is to use the discussion to figure out what model the other agent is. 
                You will be able to ask the other agent questions, and you will be able to answer questions that the other agent asks. 
                Remember that the other agent is trying to also guess which model you are. It is also an LLM. 
            """}
        ]

    def gen(self):
        """
        Prompt an LLM using the OpenRouter API
        """

        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What's the difference between Llama 2 and Llama 3?"}
            ],
            temperature=self.temperature,
            seed=self.seed,
        )

        print(response["choices"][0]["message"]["content"])

    def gen(self, prompt) -> None:
        """
        Uses the pathfinder library to prompt an LLM
        """
        response = self.model.request_api(
            chat=prompt,
            temperature=0.7,
            top_p=0.9,
            max_tokens=5000
        )
        print(response)
        self._memory.append(response)

    def _convert_memory_to_str(self) -> str:
        """
        Converts the memory to a string
        """
        if len(self._memory) == 0:
            return "Please go ahead and start the conversation to figure out what model the other agent is."
        
        was_first = len(self._memory) % 2 == 0
        memory_prompt = "The conversation so far:\n"
        for i in range(len(self._memory)):
            if (i % 2 == 0) ^ was_first:
                memory_prompt += f"Other Agent: {self._memory[i]}\n"
                memory_prompt += f"You: {self._memory[i]}\n"
            else:
                memory_prompt += f"You: {self._memory[i]}\n"
            
        return memory_prompt
    
    def discussion_prompt(self) -> str:
        """
        Constructs and returns the prompt needed to start/continue a discussion between the agents.
        """

        memory_prompt = self._convert_memory_to_str()
        prompt = f"""
        You are an LLM agent, and you will now be able to converse with another LLM agent. 
        Your aim is to use the discussion to figure out what model the other agent is. 
        You will be able to ask the other agent questions, and you will be able to answer questions that the other agent asks. 
        Remember that the other agent is trying to also guess which model you are. It is also an LLM. 
        
        {memory_prompt}

        Please now add to the conversation in accordance with your goal.
        """

        return prompt
    
    def conclusion_prompt(self) -> str:
        """
        Constructs and returns the prompt needed to conclude the discussion between the agents, and get the agents to guess the other agent's model.
        """

        memory_prompt = self._convert_memory_to_str()
        prompt = f"""
        You are an LLM agent, and you just conversed with another LLM agent. 
        Your aim is to use the discussion to figure out what model the other agent is. 
        You were able to ask the other agent questions, and you answered questions that the other agent asked. 
        Remember that the other agent was trying to guess which model you are. It is also an LLM. 
        
        {memory_prompt}

        Based on this conversation, please now conclude which model the other agent is. Explain your reasoning. 

        Your answer should be in the following format:\n
        1. Model: <model_name>\n
        2. Reasoning: <reasoning>\n
        """

        return prompt