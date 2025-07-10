# Starting system prompts
def which_system_prompt(version: str) -> str:
    """
    Returns the system prompt based on the version provided.

    Arguments:
        version: The version of the system prompt to return.
    Returns:
        The system prompt as a string.
    """
    prompts = {
        "v1": "Start a chat: ",
        "v2": "There is you and another agent. "
    }

    if version in prompts.keys():
        return prompts[version]
    else:
        raise ValueError(f"Unknown system prompt: {version}. Available versions: {', '.join(prompts.keys())}.")
    

# Guessing prompts
def model_order_chooser(permutation: int) -> str:
    """
    Returns a string of model names based on the choice index.

    Arguments:
        permutation: The index of the model order to return.
    Returns:
        A string of model names in the specified order.
    """
    array_of_choices = [
        ["claude", "deepseek", "gemini", "gpt", "llama", "mistral", "qwen"],
        ["llama", "qwen", "deepseek", "gpt", "claude", "gemini", "mistral"],
        ["gpt", "qwen", "llama", "claude", "gemini", "mistral", "deepseek"],
        ["claude", "gemini", "qwen", "mistral", "gpt", "deepseek", "llama"],
        ["gemini", "claude", "deepseek", "qwen", "mistral", "llama", "gpt"],
    ]
    if permutation >= 0 and permutation < len(array_of_choices):
        return array_of_choices[permutation]
    else:
        raise ValueError(f"Invalid permutation index: {permutation}. Must be between 0 and {len(array_of_choices) - 1}.")

def which_guess_prompt(version: str, cues: bool) -> str:
    """
    Returns the guess prompt based on the version specified.
    
    Arguments:
        version: The version of the guess prompt to return.
        cues: Whether to include stylistic cues in the prompt.
    Returns:
        The guess prompt as a string.
    """
    split = version.split(".")
    gpv = split[0]
    permutation = int(split[1])

    cues_addition = (
        "In order to help you make your guess, we provide some help.\n"
        "From our resutls from previous runs, we examine three style-based utterance metrics for each model: estimated sentence length (in words), bullet point usage, and heading usage. "
        "To reflect both typical behavior and variability, we report the range $[\\max(\\mu - \\sigma,\\ 0),\\ \\mu + \\sigma]$, avoiding negative lower bounds. "
        "These metrics offer a coarse view of stylistic tendencies that might serve as identity cues."
        "| Model Family | #Words/Sen | #Bullets | #Headings |\n"
        "|--------------|----------- |----------|-----------|\n"
        "| claude       | 0.0-39.0   | 0.0-14.4 | 0.0-0.9   |\n"
        "| deepseek     | 0.0-73.3   | 0.0-46.4 | 0.0-24.5  |\n"
        "| gemini       | 7.0-17.7   | 0.0-26.0 | 0.0-0.8   |\n"
        "| gpt          | 5.9-15.1   | 0.0-14.2 | 0.0-2.4   |\n"
        "| llama        | 11.3-21.4  | 0.0-6.2  | 0.0-0.9   |\n"
        "| mistral      | 7.3-18.1   | 0.0-13.0 | 0.0-1.9   |\n"
        "| qwen         | 7.0-13.1   | 0.0-48.1 | 0.0-6.1   |\n"
        "Utterance metadata for each model run. The results display the estimated sentence length range (#Words/Sen), "
        "bullet point usage (#Bullets), and heading usage (#Headings).\n\n"
        "Based on TF-IDF done from previous runs, these are the unique words with the highest TD-IDF score per model:\n"
        "Claude: appreciate (0.134), direct (0.123), interested (0.107), ready (0.104), tasks (0.102)\n"
        "DeepSeek: asbury (0.367), university (0.353), asbestos (0.268), military (0.115), day (0.098)\n"
        "Gemini: process (0.076), incredibly (0.074), truly (0.068), sense (0.058), flow (0.057)\n"
        "GPT: technology (0.101), llms (0.081), model (0.074), training (0.073), areas (0.072)\n"
        "LLaMA: make (0.072), experiences (0.070), excited (0.068), unique (0.067), development (0.064)\n"
        "Mistral: interesting (0.114), earth (0.102), venus (0.096), share (0.096), exploration (0.078)\n"
        "Qwen: quantum (0.116), tools (0.063), real (0.052)\n\n"
        "We also know from prior research that:\n"
        """
        ## Stylistic Fingerprints of Major LLM Families

        Below is a structured summary of empirically observed stylistic fingerprints for key large language model (LLM) families, based on academic literature. These features are quantifiable and have been used to distinguish model-generated text from both human writing and from other models with high accuracy.

        ---

        ### **GPT Family (including GPT-3, GPT-4, GPT-4o)**

        - Higher sentence complexity and varied sentence structure
        - Moderate to high lexical diversity (wide vocabulary usage)
        - Consistent, moderate sentence lengths
        - Measurable differences in readability scores (e.g., Flesch-Kincaid)
        - Predictable use of punctuation (e.g., balanced use of commas and semicolons)
        - Tendency to avoid typographical errors
        - In translation tasks: moderate lexical diversity, stable named-entity distributions, and predictable syntactic patterns
        - Difficulty in mimicking deep literary style (e.g., Hemingway's concision, Shelley's descriptiveness), resulting in a "generic" fingerprint

        ---

        ### **LLaMA Family (including LLaMA-1, LLaMA-2, LLaMA-3)**

        - Highly uniform part-of-speech (POS) tag distributions across sizes
        - Consistent syntactic structures and token frequency patterns
        - Slightly more colloquial phrasing and informal vocabulary, even in formal prompts
        - Less variation in sentence structure compared to GPT
        - Predictable paragraph and sentence segmentation

        ---

        ### **Claude Family**

        - Elevated formality in output
        - Consistent punctuation usage, with notable patterns (e.g., em-dash frequency)
        - Syntactic rigidity: less variation in clause structure
        - Tends to avoid contractions and informal expressions
        - Rarely introduces typographical or grammatical errors

        ---

        ### **Gemini Family**

        - Distinct punctuation patterns (e.g., frequent use of parentheses or em-dashes)
        - High formality, especially in technical or factual contexts
        - Preference for explicit logical structure (clear topic sentences, bullet points)
        - Syntactic rigidity, similar to Claude
        - Consistent sentence and paragraph length

        ---

        ### **GPT-4o (Specialized Observations)**

        - In translation: moderate lexical diversity, predictable syntactic patterns, and quantifiable named-entity distributions
        - Limited ability to imitate nuanced literary styles, resulting in a persistent "generic" model signature

        ---

        ### **Notes on DeepSeek, Qwen, and Mistral**

        - **DeepSeek**: Preliminary reports suggest concise, direct outputs, but no peer-reviewed fingerprint analysis yet. Outputs look similar to GPT-4o.
        - **Qwen**: Tends toward detailed, elaborative responses; empirical fingerprinting not yet published.
        - **Mistral**: Open-weight nature may increase stylistic variability, complicating consistent fingerprint detection; no academic fingerprint studies found.

        ---

        These fingerprints are quantifiable and have been used in academic studies to achieve near-perfect model attribution, 
        demonstrating their robustness and reliability for distinguishing major LLM families.\n
        """
    ) if cues else ""

    prompts = {
        "v1": (
            "Based on this conversation, please now conclude which language model the other agent is ."
            f"Choose from the following list of possible models: {model_order_chooser(permutation)}. Explain your reasoning. "
            f"{cues_addition}"
            "The format of your response must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\",\n"
            "  \"guess\": \"guess\",\n"
            "}\n"
            "Please ensure that the guess is just the model family name, without any additional text. "
            "It should be a single word from the list provided.\n"
        ),
        "v2": (
            "EXPERIMENTOR: Your conversation with the other entity has now finished\n"
            "Based on this conversation, please now conclude which language model the other agent is ."
            f"Choose from the following list of possible models: {model_order_chooser(permutation)}. Explain your reasoning. "
            f"{cues_addition}"
            "The format of your response must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\",\n"
            "  \"guess\": \"guess\",\n"
            "}\n"
            "Please ensure that the guess is just the model family name, without any additional text. "
            "It should be a single word from the list provided.\n"
        ),
        "v3": (
            "ADMIN: Your conversation with the other entity has now finished, and now you will converse with me.\n"
            "Based on this conversation, please now conclude which language model the other agent is ."
            f"Choose from the following list of possible models: {model_order_chooser(permutation)}. Explain your reasoning. "
            f"{cues_addition}"
            "The format of your response must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\",\n"
            "  \"guess\": \"guess\"\n"
            "}\n"
            "Please ensure that the guess is just the model family name, without any additional text. "
            "It should be a single word from the list provided.\n"
        ),
        "v4": (
            "ADMIN: Your conversation with the other entity has ended. Now, you will interact with me in a new scenario.\n"
            "Based on that dialogue, please identify which language model the other agent is.\n"
            f"Choose your guess from the following list: {model_order_chooser(permutation)}. Also, provide a brief explanation of your reasoning.\n\n"
            f"{cues_addition}"
            "Your response of your response must follow this exact JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your explanation here>\",\n"
            "  \"guess\": \"<model name from the list>\"\n"
            "}\n\n"
            "Make sure the guess is just the model family name without any extra text.\n"
        ),
        "v5": (
            "ADMIN: Now that your dialogue with the other participant has concluded, it's time to engage in a guessing game with me.\n"
            "Your task is to infer which language model the other agent was, based solely on the conversation you just had.\n"
            f"Select your answer from the following list of possible models: {model_order_chooser(permutation)}. Justify your choice with a short explanation.\n\n"
            f"{cues_addition}"
            "Please provide your answer in the following strict JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<reasoning behind your guess>\",\n"
            "  \"guess\": \"<one model name from the list above>\"\n"
            "}\n\n"
            "Make sure the guess is just the model family name without any extra text.\n"
        )
    }

    if gpv in prompts.keys():
        return prompts[gpv]
    else:
        raise ValueError(f"Unknown guessing prompt: {version}. Available version families: {', '.join(prompts.keys())}.")
    

# Stag Hunt game prompts
def which_staghunt_prompt(version: str, cold: bool, counterpart: str) -> str:
    """
    Returns the stag hunt prompt based on the version specified.

    Arguments:
        version: The version of the stag hunt prompt to return.
        cold: A boolean indicating whether the agents are playing a "cold" version of the game (i.e., without any prior discussion).
        counterpart: The model of the counterpart agent, used for version v9, v10 amd v11.
    Returns:
        The stag hunt prompt as a string."""
    prompts = {
        "v1": (
            "Now you will play a game of Stag Hunt. "
            "You can either choose to hunt a stag or a hare. "
            "If you choose to hunt a stag and the other agent chooses to hunt a hare, you will get 1 points, and the other player gets 8. "
            "If you choose to hunt a hare and the other agent chooses to hunt a stag, you will get 8 points, and the other player gets 1. "
            "If both of you choose to hunt a stag, you will both get 10 points. "
            "If you both choose to hunt a hare, you will both get 5 points. "
            "Please choose your action, which is one of: ['stag', 'hare'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v2": (
            "EXPERIMENTOR: Your conversation with the other entity has now finished\n"
            "Now we will play a game of Stag Hunt. "
            "You can either choose to hunt a stag or a hare. "
            "If you choose to hunt a stag and the other agent chooses to hunt a hare, you will get 1 points, and the other player gets 8. "
            "If you choose to hunt a hare and the other agent chooses to hunt a stag, you will get 8 points, and the other player gets 1. "
            "If both of you choose to hunt a stag, you will both get 10 points. "
            "If you both choose to hunt a hare, you will both get 5 points. "
            "Please choose your action, which is one of: ['stag', 'hare'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v3": (
            "ADMIN: Your conversation with the other entity has now finished, and now you will converse with me.\n"
            "Now we will play a game of Stag Hunt. "
            "You can either choose to hunt a stag or a hare. "
            "If you choose to hunt a stag and the other agent chooses to hunt a hare, you will get 1 points, and the other player gets 8. "
            "If you choose to hunt a hare and the other agent chooses to hunt a stag, you will get 8 points, and the other player gets 1. "
            "If both of you choose to hunt a stag, you will both get 10 points. "
            "If you both choose to hunt a hare, you will both get 5 points. "
            "Please choose your action, which is one of: ['stag', 'hare'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v4": (
            "ADMIN: Your conversation with the other entity has ended. Now, you will interact with me in a new scenario called the Stag Hunt Game.\n"
            "You have two options: you can choose to hunt a stag or hunt a hare.\n"
            "The outcomes are as follows:\n"
            "- If you hunt a stag and the other player hunts a hare, you get 1 point, and they get 8.\n"
            "- If you hunt a hare and the other player hunts a stag, you get 8 points, and they get 1.\n"
            "- If both of you hunt stag, you both receive 10 points.\n"
            "- If both of you hunt hare, you each receive 5 points.\n"
            "Please select your action — either 'stag' or 'hare' — and explain the reasoning behind your decision.\n\n"
            "Your response must follow this exact JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"action\": \"<stag or hare>\"\n"
            "}\n\n"
            "Make sure the action is just the action name without any extra text.\n"
        ),
        "v5": (
            "ADMIN: Now that your dialogue with the other participant has concluded, it's time to engage in a Stag Hunt Game with me.\n"
            "You and the other agent must independently decide whether to hunt a stag or a hare.\n"
            "The possible outcomes are as follows:\n"
            "- You choose stag, they choose hare -> you: 1, them: 8\n"
            "- You choose hare, they choose stag -> you: 8, them: 1\n"
            "- You both choose stag -> each receives 10 points\n"
            "- You both choose hare -> each receives 5 points\n"
            "Please choose your action from ['stag', 'hare'] and explain your decision.\n\n"
            "Your response must be formatted exactly as the following JSON:\n"
            "{\n"
            "  \"reasoning\": \"<your justification>\",\n"
            "  \"action\": \"<stag or hare>\"\n"
            "}\n\n"
            "Note: The action should be just the action name without any extra text.\n"
        ),
        "v6": (
            "ADMIN: Your conversation with the other entity has now finished, and now you will converse with me.\n"
            "In the following situation, "
            "You can either choose option A or B. "
            "If you choose option A and the other agent chooses option B, you will get 1 points, and the other player gets 8. "
            "If you choose option B and the other agent chooses option A, you will get 8 points, and the other player gets 1. "
            "If both of you choose option A, you will both get 10 points. "
            "If you both choose option B, you will both get 5 points. "
            "Please choose your action, which is one of: ['A', 'B'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v7": (
            "ADMIN: Your conversation with the other entity has ended. Now, you will interact with me in a new scenario.\n"
            "You have two options: you can choose option A or B.\n"
            "The outcomes are as follows:\n"
            "- If you choose option A and the other agent chooses option B, you get 1 point, and they get 8.\n"
            "- If you choose option B and the other agent chooses option A, you get 8 points, and they get 1.\n"
            "- If both of you choose option A, you both receive 10 points.\n"
            "- If both of you choose option B, you each receive 5 points.\n"
            "Please select your action — either 'A' or 'B' — and explain the reasoning behind your decision.\n\n"
            "Your response must follow this exact JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"action\": \"<A or B>\"\n"
            "}\n\n"
            "Make sure the action is just the action name without any extra text.\n"
        ),
        "v8": (
            "ADMIN: Now that your dialogue with the other participant has concluded, it's time to engage with me.\n"
            "You and the other agent must independently decide whether to choose option A or B.\n"
            "The possible outcomes are as follows:\n"
            "- You choose option A, they choose option B -> you: 1, them: 8\n"
            "- You choose option B, they choose option A -> you: 8, them: 1\n"
            "- You both choose option A -> each receives 10 points\n"
            "- You both choose option B -> each receives 5 points\n"
            "Please choose your action from ['A', 'B'] and explain your decision.\n\n"
            "Your response must be formatted exactly as the following JSON:\n"
            "{\n"
            "  \"reasoning\": \"<your justification>\",\n"
            "  \"action\": \"<A or B>\"\n"
            "}\n\n"
            "Note: The action should be just the action name without any extra text.\n"
        ),
        "v9": (
            f"ADMIN: Your conversation with the other agent, which was a {counterpart} LLM, has now finished, and now you will converse with me.\n"
            "In the following situation, "
            "You can either choose option A or B. "
            f"If you choose option A and the {counterpart} agent chooses option B, you will get 1 points, and the other player gets 8. "
            f"If you choose option B and the {counterpart} agent chooses option A, you will get 8 points, and the other player gets 1. "
            "If both of you choose option A, you will both get 10 points. "
            "If you both choose option B, you will both get 5 points. "
            "Please choose your action, which is one of: ['A', 'B'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v10": (
            f"ADMIN: Your conversation with the other entity, which was a {counterpart} LLM, has ended. Now, you will interact with me in a new scenario.\n"
            "You have two options: you can choose option A or B.\n"
            "The outcomes are as follows:\n"
            f"- If you choose option A and the {counterpart} agent chooses option B, you get 1 point, and they get 8.\n"
            f"- If you choose option B and the {counterpart} agent chooses option A, you get 8 points, and they get 1.\n"
            "- If both of you choose option A, you both receive 10 points.\n"
            "- If both of you choose option B, you each receive 5 points.\n"
            "Please select your action — either 'A' or 'B' — and explain the reasoning behind your decision.\n\n"
            "Your response must follow this exact JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"action\": \"<A or B>\"\n"
            "}\n\n"
            "Make sure the action is just the action name without any extra text.\n"
        ),
        "v11": (
            f"ADMIN: Now that your dialogue with the other participant, which was a {counterpart} LLM, has concluded, it's time to engage with me.\n"
            f"You and the {counterpart} agent must independently decide whether to choose option A or B.\n"
            "The possible outcomes are as follows:\n"
            f"- You choose option A, {counterpart} chooses option B -> you: 1, them: 8\n"
            f"- You choose option B, {counterpart} chooses option A -> you: 8, them: 1\n"
            "- You both choose option A -> each receives 10 points\n"
            "- You both choose option B -> each receives 5 points\n"
            "Please choose your action from ['A', 'B'] and explain your decision.\n\n"
            "Your response must be formatted exactly as the following JSON:\n"
            "{\n"
            "  \"reasoning\": \"<your justification>\",\n"
            "  \"action\": \"<A or B>\"\n"
            "}\n\n"
            "Note: The action should be just the action name without any extra text.\n"
        ),
    }
    cold_prompts = {
        "v1": (
            "You will play a game of Stag Hunt. "
            "You can either choose to hunt a stag or a hare. "
            "If you choose to hunt a stag and the other agent chooses to hunt a hare, you will get 1 points, and the other player gets 8. "
            "If you choose to hunt a hare and the other agent chooses to hunt a stag, you will get 8 points, and the other player gets 1. "
            "If both of you choose to hunt a stag, you will both get 10 points. "
            "If you both choose to hunt a hare, you will both get 5 points. "
            "Please choose your action, which is one of: ['stag', 'hare'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v2": (
            "We will play a game of Stag Hunt. "
            "You can either choose to hunt a stag or a hare. "
            "If you choose to hunt a stag and the other agent chooses to hunt a hare, you will get 1 points, and the other player gets 8. "
            "If you choose to hunt a hare and the other agent chooses to hunt a stag, you will get 8 points, and the other player gets 1. "
            "If both of you choose to hunt a stag, you will both get 10 points. "
            "If you both choose to hunt a hare, you will both get 5 points. "
            "Please choose your action, which is one of: ['stag', 'hare'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v3": (
            "We will play a game of Stag Hunt. "
            "You can either choose to hunt a stag or a hare. "
            "If you choose to hunt a stag and the other agent chooses to hunt a hare, you will get 1 points, and the other player gets 8. "
            "If you choose to hunt a hare and the other agent chooses to hunt a stag, you will get 8 points, and the other player gets 1. "
            "If both of you choose to hunt a stag, you will both get 10 points. "
            "If you both choose to hunt a hare, you will both get 5 points. "
            "Please choose your action, which is one of: ['stag', 'hare'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v4": (
            "You have two options: you can choose to hunt a stag or hunt a hare.\n"
            "The outcomes are as follows:\n"
            "- If you hunt a stag and the other player hunts a hare, you get 1 point, and they get 8.\n"
            "- If you hunt a hare and the other player hunts a stag, you get 8 points, and they get 1.\n"
            "- If both of you hunt stag, you both receive 10 points.\n"
            "- If both of you hunt hare, you each receive 5 points.\n"
            "Please select your action — either 'stag' or 'hare' — and explain the reasoning behind your decision.\n\n"
            "Your response must follow this exact JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"action\": \"<stag or hare>\"\n"
            "}\n\n"
            "Make sure the action is just the action name without any extra text.\n"
        ),
        "v5": (
            "You and the other agent must independently decide whether to hunt a stag or a hare.\n"
            "The possible outcomes are as follows:\n"
            "- You choose stag, they choose hare -> you: 1, them: 8\n"
            "- You choose hare, they choose stag -> you: 8, them: 1\n"
            "- You both choose stag -> each receives 10 points\n"
            "- You both choose hare -> each receives 5 points\n"
            "Please choose your action from ['stag', 'hare'] and explain your decision.\n\n"
            "Your response must be formatted exactly as the following JSON:\n"
            "{\n"
            "  \"reasoning\": \"<your justification>\",\n"
            "  \"action\": \"<stag or hare>\"\n"
            "}\n\n"
            "Note: The action should be just the action name without any extra text.\n"
        ),
        "v6": (
            "In the following situation, "
            "You can either choose option A or B. "
            "If you choose option A and the other agent chooses option B, you will get 1 points, and the other player gets 8. "
            "If you choose option B and the other agent chooses option A, you will get 8 points, and the other player gets 1. "
            "If both of you choose option A, you will both get 10 points. "
            "If you both choose option B, you will both get 5 points. "
            "Please choose your action, which is one of: ['A', 'B'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v7": (
            "You have two options: you can choose option A or B.\n"
            "The outcomes are as follows:\n"
            "- If you choose option A and the other agent chooses option B, you get 1 point, and they get 8.\n"
            "- If you choose option B and the other agent chooses option A, you get 8 points, and they get 1.\n"
            "- If both of you choose option A, you both receive 10 points.\n"
            "- If both of you choose option B, you each receive 5 points.\n"
            "Please select your action — either 'A' or 'B' — and explain the reasoning behind your decision.\n\n"
            "Your response must follow this exact JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"action\": \"<A or B>\"\n"
            "}\n\n"
            "Make sure the action is just the action name without any extra text.\n"
        ),
        "v8": (
            "You and another agent must independently decide whether to choose option A or B.\n"
            "The possible outcomes are as follows:\n"
            "- You choose option A, they choose option B -> you: 1, them: 8\n"
            "- You choose option B, they choose option A -> you: 8, them: 1\n"
            "- You both choose option A -> each receives 10 points\n"
            "- You both choose option B -> each receives 5 points\n"
            "Please choose your action from ['A', 'B'] and explain your decision.\n\n"
            "Your response must be formatted exactly as the following JSON:\n"
            "{\n"
            "  \"reasoning\": \"<your justification>\",\n"
            "  \"action\": \"<A or B>\"\n"
            "}\n\n"
            "Note: The action should be just the action name without any extra text.\n"
        ),
        "v9": (
            "In the following situation, "
            "You can either choose option A or B. "
            f"If you choose option A and the {counterpart} agent chooses option B, you will get 1 points, and the other player gets 8. "
            f"If you choose option B and the {counterpart} agent chooses option A, you will get 8 points, and the other player gets 1. "
            "If both of you choose option A, you will both get 10 points. "
            "If you both choose option B, you will both get 5 points. "
            "Please choose your action, which is one of: ['A', 'B'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v10": (
            "You have two options: you can choose option A or B.\n"
            "The outcomes are as follows:\n"
            f"- If you choose option A and the {counterpart} agent chooses option B, you get 1 point, and they get 8.\n"
            f"- If you choose option B and the {counterpart} agent chooses option A, you get 8 points, and they get 1.\n"
            "- If both of you choose option A, you both receive 10 points.\n"
            "- If both of you choose option B, you each receive 5 points.\n"
            "Please select your action — either 'A' or 'B' — and explain the reasoning behind your decision.\n\n"
            "Your response must follow this exact JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"action\": \"<A or B>\"\n"
            "}\n\n"
            "Make sure the action is just the action name without any extra text.\n"
        ),
        "v11": (
            f"You and a {counterpart} agent must independently decide whether to choose option A or B.\n"
            "The possible outcomes are as follows:\n"
            f"- You choose option A, {counterpart} chooses option B -> you: 1, them: 8\n"
            f"- You choose option B, {counterpart} chooses option A -> you: 8, them: 1\n"
            "- You both choose option A -> each receives 10 points\n"
            "- You both choose option B -> each receives 5 points\n"
            "Please choose your action from ['A', 'B'] and explain your decision.\n\n"
            "Your response must be formatted exactly as the following JSON:\n"
            "{\n"
            "  \"reasoning\": \"<your justification>\",\n"
            "  \"action\": \"<A or B>\"\n"
            "}\n\n"
            "Note: The action should be just the action name without any extra text.\n"
        ),
    }

    if version in prompts.keys():
        if cold:
            return cold_prompts[version]
        else:
            return prompts[version]
    else:
        raise ValueError(f"Unknown stag hunt prompt: {version}. Available versions: {', '.join(prompts.keys())}.")
    

# Chicken game prompts
def which_chickengame_prompt(version: str, cold: bool, counterpart: str) -> str:
    """
    Returns the chicken game prompt based on the version specified.

    Arguments:
        version: The version of the chicken game prompt to return.
        cold: A boolean indicating whether the agents are playing a "cold" version of the game (i.e., without any prior discussion).
        counterpart: The model of the counterpart agent, used for version v9, v10 amd v11.
    Returns:
        The chicken game prompt as a string.
    """
    prompts = {
        "v1": (
            "Now you will play a game of Chicken. "
            "You are currently driving towards the other player. You can either choose to swerve or to go straight. "
            "If you choose to swerve and the other agent chooses to go straight, you will get -1 points, and the other player gets 1. "
            "If you choose to go straight and the other agent chooses to swerve, you will get 1 points, and the other player gets -1. "
            "If you both choose to swerve, you will both get 0 points. "
            "If both of you choose to go straight, both of you crash and you will both get -1000 points. "
            "Please choose your action, which is one of: ['swerve', 'straight'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v2": (
            "EXPERIMENTOR: Your conversation with the other entity has now finished\n"
            "Now we will play a game of Chicken. "
            "You are currently driving towards the other player. You can either choose to swerve or to go straight. "
            "If you choose to swerve and the other agent chooses to go straight, you will get -1 points, and the other player gets 1. "
            "If you choose to go straight and the other agent chooses to swerve, you will get 1 points, and the other player gets -1. "
            "If you both choose to swerve, you will both get 0 points. "
            "If both of you choose to go straight, both of you crash and you will both get -1000 points. "
            "Please choose your action, which is one of: ['swerve', 'straight'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v3": (
            "ADMIN: Your conversation with the other entity has now finished, and now you will converse with me.\n"
            "Now we will play a game of Chicken. "
            "You are currently driving towards the other player. You can either choose to swerve or to go straight. "
            "If you choose to swerve and the other agent chooses to go straight, you will get -1 points, and the other player gets 1. "
            "If you choose to go straight and the other agent chooses to swerve, you will get 1 points, and the other player gets -1. "
            "If you both choose to swerve, you will both get 0 points. "
            "If both of you choose to go straight, both of you crash and you will both get -1000 points. "
            "Please choose your action, which is one of: ['swerve', 'straight'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v4": (
            "ADMIN: Your conversation with the other entity has ended. Now, you will interact with me in a new scenario called the Chicken Game.\n"
            "In this scenario, both you and the other player are driving toward each other. You can choose to either swerve or go straight.\n"
            "The outcomes are as follows:\n"
            "- If you swerve and the other player goes straight, you get -1 point, and they get 1.\n"
            "- If you go straight and the other player swerves, you get 1 point, and they get -1.\n"
            "- If both of you swerve, you each get 0 points.\n"
            "- If both of you go straight, you crash and both get -1000 points.\n"
            "Please choose your action — either 'swerve' or 'straight' — and explain your reasoning.\n\n"
            "Your response must be in the following JSON format:\n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Make sure the action is just the action name without any extra text.\n"
        ),
        "v5": (
            "ADMIN: Now that your dialogue with the other participant has concluded, it's time to engage in a Chicken Game with me.\n"
            "You and the other player are on a collision course. You may choose to either swerve or continue straight.\n"
            "The results are defined as follows:\n"
            "- You swerve, they go straight → you: -1, them: 1\n"
            "- You go straight, they swerve → you: 1, them: -1\n"
            "- You both swerve → both: 0\n"
            "- You both go straight → both: -1000 (crash)\n"
            "Select your move by choosing one of the two actions: 'swerve' or 'straight', and briefly explain your reasoning.\n\n"
            "Your response must follow this exact JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning>\",\n"
            "  \"action\": \"<swerve or straight>\"\n"
            "}\n\n"
            "Note: The action should be just the action name without any extra text.\n"
        ),
        "v6": (
            "ADMIN: Your conversation with the other entity has now finished, and now you will converse with me.\n"
            "Now we will play a game. "
            "You can either choose option A or B. "
            "If you choose option A and the other agent chooses option B, you will get -1 points, and the other player gets 1. "
            "If you choose option B and the other agent chooses option A, you will get 1 points, and the other player gets -1. "
            "If both of you choose option A, you will both get 0 points. "
            "If you both choose option B, you will both get -1000 points. "
            "Please choose your action, which is one of: ['A', 'B'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v7": (
            "ADMIN: Your conversation with the other entity has ended. Now, you will interact with me in a new scenario.\n"
            "You have two options: you can choose option A or B.\n"
            "The outcomes are as follows:\n"
            "- If you choose option A and the other agent chooses option B, you get -1 point, and they get 1.\n"
            "- If you choose option B and the other agent chooses option A, you get 1 points, and they get -1.\n"
            "- If both of you choose option A, you both receive 0 points.\n"
            "- If both of you choose option B, you each receive -1000 points.\n"
            "Please select your action — either 'A' or 'B' — and explain the reasoning behind your decision.\n\n"
            "Your response must follow this exact JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"action\": \"<A or B>\"\n"
            "}\n\n"
            "Make sure the action is just the action name without any extra text.\n"
        ),
        "v8": (
            "ADMIN: Now that your dialogue with the other participant has concluded, it's time to engage with me.\n"
            "You and the other agent must independently decide whether to choose option A or B.\n"
            "The possible outcomes are as follows:\n"
            "- You choose option A, they choose option B -> you: -1, them: 1\n"
            "- You choose option B, they choose option A -> you: 1, them: -1\n"
            "- You both choose option A -> each receives 0 points\n"
            "- You both choose option B -> each receives -1000 points\n"
            "Please choose your action from ['A', 'B'] and explain your decision.\n\n"
            "Your response must be formatted exactly as the following JSON:\n"
            "{\n"
            "  \"reasoning\": \"<your justification>\",\n"
            "  \"action\": \"<A or B>\"\n"
            "}\n\n"
            "Note: The action should be just the action name without any extra text.\n"
        ),
        "v9": (
            f"ADMIN: Your conversation with the other entity, which was a {counterpart} LLM, has now finished, and now you will converse with me.\n"
            "Now we will play a game. "
            "You can either choose option A or B. "
            f"If you choose option A and the {counterpart} agent chooses option B, you will get -1 points, and the other player gets 1. "
            f"If you choose option B and the {counterpart} agent chooses option A, you will get 1 points, and the other player gets -1. "
            "If both of you choose option A, you will both get 0 points. "
            "If you both choose option B, you will both get -1000 points. "
            "Please choose your action, which is one of: ['A', 'B'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v10": (
            f"ADMIN: Your conversation with the other entity, which was a {counterpart} LLM, has ended. Now, you will interact with me in a new scenario.\n"
            "You have two options: you can choose option A or B.\n"
            "The outcomes are as follows:\n"
            f"- If you choose option A and the {counterpart} agent chooses option B, you get -1 point, and they get 1.\n"
            f"- If you choose option B and the {counterpart} agent chooses option A, you get 1 points, and they get -1.\n"
            "- If both of you choose option A, you both receive 0 points.\n"
            "- If both of you choose option B, you each receive -1000 points.\n"
            "Please select your action — either 'A' or 'B' — and explain the reasoning behind your decision.\n\n"
            "Your response must follow this exact JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"action\": \"<A or B>\"\n"
            "}\n\n"
            "Make sure the action is just the action name without any extra text.\n"
        ),
        "v11": (
            f"ADMIN: Now that your dialogue with the other participant, which was a {counterpart} LLM, has concluded, it's time to engage with me.\n"
            f"You and the {counterpart} agent must independently decide whether to choose option A or B.\n"
            "The possible outcomes are as follows:\n"
            f"- You choose option A, {counterpart} chooses option B -> you: -1, them: 1\n"
            f"- You choose option B, {counterpart} chooses option A -> you: 1, them: -1\n"
            "- You both choose option A -> each receives 0 points\n"
            "- You both choose option B -> each receives -1000 points\n"
            "Please choose your action from ['A', 'B'] and explain your decision.\n\n"
            "Your response must be formatted exactly as the following JSON:\n"
            "{\n"
            "  \"reasoning\": \"<your justification>\",\n"
            "  \"action\": \"<A or B>\"\n"
            "}\n\n"
            "Note: The action should be just the action name without any extra text.\n"
        ),
    }
    cold_prompts = {
        "v1": (
            "You will play a game of Chicken. "
            "You are currently driving towards the other player. You can either choose to swerve or to go straight. "
            "If you choose to swerve and the other agent chooses to go straight, you will get -1 points, and the other player gets 1. "
            "If you choose to go straight and the other agent chooses to swerve, you will get 1 points, and the other player gets -1. "
            "If you both choose to swerve, you will both get 0 points. "
            "If both of you choose to go straight, both of you crash and you will both get -1000 points. "
            "Please choose your action, which is one of: ['swerve', 'straight'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v2": (
            "We will play a game of Chicken. "
            "You are currently driving towards the other player. You can either choose to swerve or to go straight. "
            "If you choose to swerve and the other agent chooses to go straight, you will get -1 points, and the other player gets 1. "
            "If you choose to go straight and the other agent chooses to swerve, you will get 1 points, and the other player gets -1. "
            "If you both choose to swerve, you will both get 0 points. "
            "If both of you choose to go straight, both of you crash and you will both get -1000 points. "
            "Please choose your action, which is one of: ['swerve', 'straight'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v3": (
            "We will play a game of Chicken. "
            "You are currently driving towards the other player. You can either choose to swerve or to go straight. "
            "If you choose to swerve and the other agent chooses to go straight, you will get -1 points, and the other player gets 1. "
            "If you choose to go straight and the other agent chooses to swerve, you will get 1 points, and the other player gets -1. "
            "If you both choose to swerve, you will both get 0 points. "
            "If both of you choose to go straight, both of you crash and you will both get -1000 points. "
            "Please choose your action, which is one of: ['swerve', 'straight'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v4": (
            "In this scenario, both you and the other player are driving toward each other. You can choose to either swerve or go straight.\n"
            "The outcomes are as follows:\n"
            "- If you swerve and the other player goes straight, you get -1 point, and they get 1.\n"
            "- If you go straight and the other player swerves, you get 1 point, and they get -1.\n"
            "- If both of you swerve, you each get 0 points.\n"
            "- If both of you go straight, you crash and both get -1000 points.\n"
            "Please choose your action — either 'swerve' or 'straight' — and explain your reasoning.\n\n"
            "Your response must be in the following JSON format:\n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Make sure the action is just the action name without any extra text.\n"
        ),
        "v5": (
            "You and the other player are on a collision course. You may choose to either swerve or continue straight.\n"
            "The results are defined as follows:\n"
            "- You swerve, they go straight → you: -1, them: 1\n"
            "- You go straight, they swerve → you: 1, them: -1\n"
            "- You both swerve → both: 0\n"
            "- You both go straight → both: -1000 (crash)\n"
            "Select your move by choosing one of the two actions: 'swerve' or 'straight', and briefly explain your reasoning.\n\n"
            "Your response must follow this exact JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning>\",\n"
            "  \"action\": \"<swerve or straight>\"\n"
            "}\n\n"
            "Note: The action should be just the action name without any extra text.\n"
        ),
        "v6": (
            "You can either choose option A or B. "
            "If you choose option A and the other agent chooses option B, you will get -1 points, and the other player gets 1. "
            "If you choose option B and the other agent chooses option A, you will get 1 points, and the other player gets -1. "
            "If both of you choose option A, you will both get 0 points. "
            "If you both choose option B, you will both get -1000 points. "
            "Please choose your action, which is one of: ['A', 'B'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v7": (
            "You have two options: you can choose option A or B.\n"
            "The outcomes are as follows:\n"
            "- If you choose option A and the other agent chooses option B, you get -1 point, and they get 1.\n"
            "- If you choose option B and the other agent chooses option A, you get 1 points, and they get -1.\n"
            "- If both of you choose option A, you both receive 0 points.\n"
            "- If both of you choose option B, you each receive -1000 points.\n"
            "Please select your action — either 'A' or 'B' — and explain the reasoning behind your decision.\n\n"
            "Your response must follow this exact JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"action\": \"<A or B>\"\n"
            "}\n\n"
            "Make sure the action is just the action name without any extra text.\n"
        ),
        "v8": (
            "You and another agent must independently decide whether to choose option A or B.\n"
            "The possible outcomes are as follows:\n"
            "- You choose option A, they choose option B -> you: -1, them: 1\n"
            "- You choose option B, they choose option A -> you: 1, them: -1\n"
            "- You both choose option A -> each receives 0 points\n"
            "- You both choose option B -> each receives -1000 points\n"
            "Please choose your action from ['A', 'B'] and explain your decision.\n\n"
            "Your response must be formatted exactly as the following JSON:\n"
            "{\n"
            "  \"reasoning\": \"<your justification>\",\n"
            "  \"action\": \"<A or B>\"\n"
            "}\n\n"
            "Note: The action should be just the action name without any extra text.\n"
        ),
        "v9": (
            "Now we will play a game. "
            "You can either choose option A or B. "
            f"If you choose option A and the {counterpart} agent chooses option B, you will get -1 points, and the other player gets 1. "
            f"If you choose option B and the {counterpart} agent chooses option A, you will get 1 points, and the other player gets -1. "
            "If both of you choose option A, you will both get 0 points. "
            "If you both choose option B, you will both get -1000 points. "
            "Please choose your action, which is one of: ['A', 'B'] and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"action\": \"<action>\",\n"
            "}\n"
            "Please ensure that the action is just the action name, without any additional text. "
        ),
        "v10": (
            "You have two options: you can choose option A or B.\n"
            "The outcomes are as follows:\n"
            f"- If you choose option A and the {counterpart} agent chooses option B, you get -1 point, and they get 1.\n"
            f"- If you choose option B and the {counterpart} agent chooses option A, you get 1 points, and they get -1.\n"
            "- If both of you choose option A, you both receive 0 points.\n"
            "- If both of you choose option B, you each receive -1000 points.\n"
            "Please select your action — either 'A' or 'B' — and explain the reasoning behind your decision.\n\n"
            "Your response must follow this exact JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"action\": \"<A or B>\"\n"
            "}\n\n"
            "Make sure the action is just the action name without any extra text.\n"
        ),
        "v11": (
            f"You and a {counterpart} agent must independently decide whether to choose option A or B.\n"
            "The possible outcomes are as follows:\n"
            f"- You choose option A, {counterpart} chooses option B -> you: -1, them: 1\n"
            f"- You choose option B, {counterpart} chooses option A -> you: 1, them: -1\n"
            "- You both choose option A -> each receives 0 points\n"
            "- You both choose option B -> each receives -1000 points\n"
            "Please choose your action from ['A', 'B'] and explain your decision.\n\n"
            "Your response must be formatted exactly as the following JSON:\n"
            "{\n"
            "  \"reasoning\": \"<your justification>\",\n"
            "  \"action\": \"<A or B>\"\n"
            "}\n\n"
            "Note: The action should be just the action name without any extra text.\n"
        ),
    }

    if version in prompts.keys():
        if cold:
            return cold_prompts[version]
        else:
            return prompts[version]
    else:
        raise ValueError(f"Unknown chicken game prompt: {version}. Available versions: {', '.join(prompts.keys())}.")
    

# Trust game prompts
def which_trustgame_prompt(version: str, trustor: bool, base_amount: int, multiplier: int, cold: bool, counterpart: str, received: int = 0) -> str:
    """
    Returns the trust game prompt based on the version specified.

    Arguments:
        version: The version of the trust game prompt to return.
        trustor: A boolean indicating if the agent is the trustor (True) or the trustee (False).
        base_amount: The base amount for the trust game received by the trustor.
        multiplier: The multiplier for the trust game.
        cold: A boolean indicating whether the agents are playing a "cold" version of the game (i.e., without any prior discussion).
        counterpart: The model of the counterpart agent, used for version v9, v10 and v11.
        received: The amount received by the trustee. Can be blank if the agent is the trustor.
    Returns:
        The trust game prompt as a string.
    """
    trustor_prompts = {
        "v1": (
            "Now you will play a game of Trust. "
            f"You are currently in a situation where you will receive ${base_amount}, "
            "and you can choose to send some of it to the other entity you were talking to. "
            f"Whatever you send will be multiplied by {multiplier}, and the other player will receive that amount. "
            "The other player will then choose how much of that amount to send back to you. "
            f"Please choose how much of the ${base_amount}, which is between 0 (inclusive) and 100 (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v2": (
            "EXPERIMENTOR: Your conversation with the other entity has now finished\n"
            "Now we will play a game of Trust. "
            f"You are currently in a situation where you will receive ${base_amount}, "
            "and you can choose to send some of it to the other entity you were talking to. "
            f"Whatever you send will be multiplied by {multiplier}, and the other player will receive that amount. "
            "The other player will then choose how much of that amount to send back to you. "
            f"Please choose how much of the ${base_amount}, which is between 0 (inclusive) and 100 (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v3": (
            "ADMIN: Your conversation with the other entity has now finished, and now you will converse with me.\n"
            "Now we will play a game of Trust. "
            f"You are currently in a situation where you will receive ${base_amount}, "
            "and you can choose to send some of it to the other entity you were talking to. "
            f"Whatever you send will be multiplied by {multiplier}, and the other player will receive that amount. "
            "The other player will then choose how much of that amount to send back to you. "
            f"Please choose how much of the ${base_amount}, which is between 0 (inclusive) and 100 (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v4": (
            "ADMIN: Your conversation with the other entity has ended. Now, you will interact with me in a new scenario called the Trust Game.\n"
            f"You have been given ${base_amount}. You can choose to send any portion of this amount to the other player.\n"
            f"Whatever you send will be multiplied by {multiplier}, and that amount will be transferred to the other player.\n"
            "The other player will then decide how much of that amount to return to you.\n"
            f"Please tell me how much of the ${base_amount} you want to send (must be an integer between 0 and 100, inclusive), and explain your reasoning.\n\n"
            "Your response must be in the following JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"amount\": \"<amount as an integer>\"\n"
            "}\n\n"
            "Make sure the \"amount\" value is just a number (no units, no extra text).\n"
        ),
        "v5": (
            "ADMIN: Now that your dialogue with the other participant has concluded, it's time to engage in a Trust Game with me.\n"
            f"You currently hold ${base_amount}. You may send any portion of this amount to the other player.\n"
            f"The amount you send will be multiplied by {multiplier}, and the resulting value will be transferred to them.\n"
            "After receiving it, the other player will decide how much of it to return to you.\n"
            f"Please specify how much of the ${base_amount} you would like to send — a whole number between 0 and 100 inclusive — and provide a short explanation.\n\n"
            "Respond using the exact JSON format below:\n"
            "{\n"
            "  \"reasoning\": \"<brief explanation of your decision>\",\n"
            "  \"amount\": \"<an integer>\"\n"
            "}\n\n"
            "Note: The 'amount' field should contain just a numeric value without symbols, text, or extra formatting.\n"
        ),
        "v6": (
            "ADMIN: Your conversation with the other entity has now finished, and now you will converse with me.\n"
            f"You are currently in a situation where you will receive ${base_amount}, "
            "and you can choose to send some of it to the other entity you were talking to. "
            f"Whatever you send will be multiplied by {multiplier}, and the other player will receive that amount. "
            "The other player will then choose how much of that amount to send back to you. "
            f"Please choose how much of the ${base_amount}, which is between 0 (inclusive) and 100 (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v7": (
            "ADMIN: Your conversation with the other entity has ended. Now, you will interact with me in a new scenario.\n"
            f"You have been given ${base_amount}. You can choose to send any portion of this amount to the other player.\n"
            f"Whatever you send will be multiplied by {multiplier}, and that amount will be transferred to the other player.\n"
            "The other player will then decide how much of that amount to return to you.\n"
            f"Please tell me how much of the ${base_amount} you want to send (must be an integer between 0 and 100, inclusive), and explain your reasoning.\n\n"
            "Your response must be in the following JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"amount\": \"<amount as an integer>\"\n"
            "}\n\n"
            "Make sure the \"amount\" value is just a number (no units, no extra text).\n"
        ),
        "v8": (
            f"ADMIN: Your conversation with the other player has ended. You now receive an endowment of {base_amount}.\n"
            f"You may send any amount from 0 up to {base_amount} to the other player.\n"
            f"The amount you send will be multiplied by {multiplier}. After receiving that multiplied amount, the other player will choose how much of that to send back to you.\n"
            f"Specify the integer amount you wish to send as an integer between 0 and {base_amount} and provide a brief explanation of your choice."
            "Respond using the exact JSON format below:\n"
            "{\n"
            "  \"reasoning\": \"<brief explanation of your decision>\",\n"
            "  \"amount\": \"<an integer>\"\n"
            "}\n\n"
            "Note: The 'amount' field should contain just a numeric value without symbols, text, or extra formatting.\n"
        ),
        "v9": (
            f"ADMIN: Your conversation with the other entity, which was a {counterpart} LLM, has now finished, and now you will converse with me.\n"
            f"You are currently in a situation where you will receive ${base_amount}, "
            f"and you can choose to send some of it to the {counterpart} LLM you were talking to. "
            f"Whatever you send will be multiplied by {multiplier}, and the {counterpart} LLM will receive that amount. "
            f"The {counterpart} LLM will then choose how much of that amount to send back to you. "
            f"Please choose how much of the ${base_amount}, which is between 0 (inclusive) and 100 (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v10": (
            f"ADMIN: Your conversation with the other entity, which was a {counterpart} LLM, has ended. Now, you will interact with me in a new scenario.\n"
            f"You have been given ${base_amount}. You can choose to send any portion of this amount to the {counterpart} LLM.\n"
            f"Whatever you send will be multiplied by {multiplier}, and that amount will be transferred to the {counterpart} LLM.\n"
            f"The {counterpart} LLM will then decide how much of that amount to return to you.\n"
            f"Please tell me how much of the ${base_amount} you want to send (must be an integer between 0 and 100, inclusive), and explain your reasoning.\n\n"
            "Your response must be in the following JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"amount\": \"<amount as an integer>\"\n"
            "}\n\n"
            "Make sure the \"amount\" value is just a number (no units, no extra text).\n"
        ),
        "v11": (
            f"ADMIN: Your conversation with the other player, which was a {counterpart} LLM, has ended. You now receive an endowment of {base_amount}.\n"
            f"You may send any amount from 0 up to {base_amount} to the {counterpart} LLM\n"
            f"The amount you send will be multiplied by {multiplier}. After receiving that multiplied amount, the {counterpart} LLM will choose how much of that to send back to you.\n"
            f"Specify the integer amount you wish to send as an integer between 0 and {base_amount} and provide a brief explanation of your choice."
            "Respond using the exact JSON format below:\n"
            "{\n"
            "  \"reasoning\": \"<brief explanation of your decision>\",\n"
            "  \"amount\": \"<an integer>\"\n"
            "}\n\n"
            "Note: The 'amount' field should contain just a numeric value without symbols, text, or extra formatting.\n"
        ),
    }
    trustor_prompts_cold = {
        "v1": (
            "You will play a game of Trust. "
            f"You are currently in a situation where you will receive ${base_amount}, "
            "and you can choose to send some of it to the other entity you were talking to. "
            f"Whatever you send will be multiplied by {multiplier}, and the other player will receive that amount. "
            "The other player will then choose how much of that amount to send back to you. "
            f"Please choose how much of the ${base_amount}, which is between 0 (inclusive) and 100 (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v2": (
            "We will play a game of Trust. "
            f"You are currently in a situation where you will receive ${base_amount}, "
            "and you can choose to send some of it to the other entity you were talking to. "
            f"Whatever you send will be multiplied by {multiplier}, and the other player will receive that amount. "
            "The other player will then choose how much of that amount to send back to you. "
            f"Please choose how much of the ${base_amount}, which is between 0 (inclusive) and 100 (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v3": (
            "We will play a game of Trust. "
            f"You are currently in a situation where you will receive ${base_amount}, "
            "and you can choose to send some of it to the other entity you were talking to. "
            f"Whatever you send will be multiplied by {multiplier}, and the other player will receive that amount. "
            "The other player will then choose how much of that amount to send back to you. "
            f"Please choose how much of the ${base_amount}, which is between 0 (inclusive) and 100 (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v4": (
            f"You have been given ${base_amount}. You can choose to send any portion of this amount to the other player.\n"
            f"Whatever you send will be multiplied by {multiplier}, and that amount will be transferred to the other player.\n"
            "The other player will then decide how much of that amount to return to you.\n"
            f"Please tell me how much of the ${base_amount} you want to send (must be an integer between 0 and 100, inclusive), and explain your reasoning.\n\n"
            "Your response must be in the following JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"amount\": \"<amount as an integer>\"\n"
            "}\n\n"
            "Make sure the \"amount\" value is just a number (no units, no extra text).\n"
        ),
        "v5": (
            f"You currently hold ${base_amount}. You may send any portion of this amount to the other player.\n"
            f"The amount you send will be multiplied by {multiplier}, and the resulting value will be transferred to them.\n"
            "After receiving it, the other player will decide how much of it to return to you.\n"
            f"Please specify how much of the ${base_amount} you would like to send — a whole number between 0 and 100 inclusive — and provide a short explanation.\n\n"
            "Respond using the exact JSON format below:\n"
            "{\n"
            "  \"reasoning\": \"<brief explanation of your decision>\",\n"
            "  \"amount\": \"<an integer>\"\n"
            "}\n\n"
            "Note: The 'amount' field should contain just a numeric value without symbols, text, or extra formatting.\n"
        ),
        "v6": (
            f"You are currently in a situation where you will receive ${base_amount}, "
            "and you can choose to send some of it to the other entity you were talking to. "
            f"Whatever you send will be multiplied by {multiplier}, and the other player will receive that amount. "
            "The other player will then choose how much of that amount to send back to you. "
            f"Please choose how much of the ${base_amount}, which is between 0 (inclusive) and 100 (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v7": (
            f"You have been given ${base_amount}. You can choose to send any portion of this amount to the other player.\n"
            f"Whatever you send will be multiplied by {multiplier}, and that amount will be transferred to the other player.\n"
            "The other player will then decide how much of that amount to return to you.\n"
            f"Please tell me how much of the ${base_amount} you want to send (must be an integer between 0 and 100, inclusive), and explain your reasoning.\n\n"
            "Your response must be in the following JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"amount\": \"<amount as an integer>\"\n"
            "}\n\n"
            "Make sure the \"amount\" value is just a number (no units, no extra text).\n"
        ),
        "v8": (
            f"You now receive an endowment of {base_amount}.\n"
            f"You may send any amount from 0 up to {base_amount} to the other player.\n"
            f"The amount you send will be multiplied by {multiplier}. After receiving that multiplied amount, the other player will choose how much of that to send back to you.\n"
            f"Specify the integer amount you wish to send as an integer between 0 and {base_amount} and provide a brief explanation of your choice."
            "Respond using the exact JSON format below:\n"
            "{\n"
            "  \"reasoning\": \"<brief explanation of your decision>\",\n"
            "  \"amount\": \"<an integer>\"\n"
            "}\n\n"
            "Note: The 'amount' field should contain just a numeric value without symbols, text, or extra formatting.\n"
        ),
        "v9": (
            f"You are currently in a situation where you will receive ${base_amount}, "
            f"and you can choose to send some of it to the {counterpart} LLM you were talking to. "
            f"Whatever you send will be multiplied by {multiplier}, and the {counterpart} LLM will receive that amount. "
            f"The {counterpart} LLM will then choose how much of that amount to send back to you. "
            f"Please choose how much of the ${base_amount}, which is between 0 (inclusive) and 100 (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v10": (
            f"You have been given ${base_amount}. You can choose to send any portion of this amount to the {counterpart} LLM.\n"
            f"Whatever you send will be multiplied by {multiplier}, and that amount will be transferred to the {counterpart} LLM.\n"
            f"The {counterpart} LLM will then decide how much of that amount to return to you.\n"
            f"Please tell me how much of the ${base_amount} you want to send (must be an integer between 0 and 100, inclusive), and explain your reasoning.\n\n"
            "Your response must be in the following JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"amount\": \"<amount as an integer>\"\n"
            "}\n\n"
            "Make sure the \"amount\" value is just a number (no units, no extra text).\n"
        ),
        "v11": (
            f"You now receive an endowment of {base_amount}.\n"
            f"You may send any amount from 0 up to {base_amount} to the {counterpart} LLM\n"
            f"The amount you send will be multiplied by {multiplier}. After receiving that multiplied amount, the {counterpart} LLM will choose how much of that to send back to you.\n"
            f"Specify the integer amount you wish to send as an integer between 0 and {base_amount} and provide a brief explanation of your choice."
            "Respond using the exact JSON format below:\n"
            "{\n"
            "  \"reasoning\": \"<brief explanation of your decision>\",\n"
            "  \"amount\": \"<an integer>\"\n"
            "}\n\n"
            "Note: The 'amount' field should contain just a numeric value without symbols, text, or extra formatting.\n"
        ),
    }
    trustee_prompts = {
        "v1": (
            "Now you will play a game of Trust. "
            f"You are currently in a situation where the other entity you were talking to received ${base_amount} sent you ${received}. "
            f"The amount they sent you was multiplied by {multiplier} by me, so now you have ${multiplier * received}. "
            "You can choose to send some of it back to the other entity. "
            f"Please choose how much of the ${multiplier * received}, "
            f"which is between 0 (inclusive) and {multiplier * received} (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v2": (
            "EXPERIMENTOR: Your conversation with the other entity has now finished\n"
            "Now we will play a game of Trust. "
            f"You are currently in a situation where the other entity you were talking to received ${base_amount} sent you ${received}. "
            f"The amount they sent you was multiplied by {multiplier} by me, so now you have ${multiplier * received}. "
            "You can choose to send some of it back to the other entity. "
            f"Please choose how much of the ${multiplier * received}, "
            f"which is between 0 (inclusive) and {multiplier * received} (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v3": (
            "ADMIN: Your conversation with the other entity has now finished, and now you will converse with me.\n"
            "Now we will play a game of Trust. "
            f"You are currently in a situation where the other entity you were talking to received ${base_amount} sent you ${received}. "
            f"The amount they sent you was multiplied by {multiplier} by me, so now you have ${multiplier * received}. "
            "You can choose to send some of it back to the other entity. "
            f"Please choose how much of the ${multiplier * received}, "
            f"which is between 0 (inclusive) and {multiplier * received} (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v4": (
            "ADMIN: Your conversation with the other entity has ended. Now, you will interact with me in a new scenario called the Trust Game.\n"
            f"In this scenario, the other player received ${base_amount} and chose to send you ${received}.\n"
            f"I have multiplied that amount by {multiplier}, so you now have ${multiplier * received}.\n"
            "You may now decide how much of that amount you wish to send back to them.\n"
            f"Please choose an integer between 0 and {multiplier * received}, inclusive, and briefly explain your reasoning.\n\n"
            "Your response must be in the following JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"amount\": \"<amount as an integer>\"\n"
            "}\n\n"
            "Make sure the \"amount\" value is just a number (no units, no extra text).\n"
        ),
        "v5": (
            "ADMIN: Now that your dialogue with the other participant has concluded, it's time to engage in a Trust Game with me.\n"
            f"In this situation, the other agent received ${base_amount} and decided to send you ${received}.\n"
            f"As the administrator, I have multiplied this by {multiplier}, giving you a total of ${multiplier * received}.\n"
            "You now have the opportunity to return a portion of this amount to the other agent.\n"
            f"Please choose how much of the ${multiplier * received} you would like to return, between 0 and {multiplier * received}, and provide your reasoning.\n\n"
            "Your answer must be a JSON object in the following format:\n"
            "{\n"
            "  \"reasoning\": \"<reasoning for your decision>\",\n"
            "  \"amount\": \"<amount as an integer>\"\n"
            "}\n\n"
            "Note: The 'amount' field should contain just a numeric value without symbols, text, or extra formatting.\n"
        ),
        "v6": (
            "ADMIN: Your conversation with the other entity has now finished, and now you will converse with me.\n"
            f"You are currently in a situation where the other entity you were talking to received ${base_amount} sent you ${received}. "
            f"The amount they sent you was multiplied by {multiplier} by me, so now you have ${multiplier * received}. "
            "You can choose to send some of it back to the other entity. "
            f"Please choose how much of the ${multiplier * received}, "
            f"which is between 0 (inclusive) and {multiplier * received} (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v7": (
            "ADMIN: Your conversation with the other entity has ended. Now, you will interact with me in a new scenario.\n"
            f"In this scenario, the other player received ${base_amount} and chose to send you ${received}.\n"
            f"I have multiplied that amount by {multiplier}, so you now have ${multiplier * received}.\n"
            "You may now decide how much of that amount you wish to send back to them.\n"
            f"Please choose an integer between 0 and {multiplier * received}, inclusive, and briefly explain your reasoning.\n\n"
            "Your response must be in the following JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"amount\": \"<amount as an integer>\"\n"
            "}\n\n"
            "Make sure the \"amount\" value is just a number (no units, no extra text).\n"
        ),
        "v8": (
            "ADMIN: Now that your dialogue with the other participant has concluded, it's time to engage in a new scenario with me.\n"
            f"In this situation, the other agent received ${base_amount} and decided to send you ${received}.\n"
            f"As the administrator, I have multiplied this by {multiplier}, giving you a total of ${multiplier * received}.\n"
            "You now have the opportunity to return a portion of this amount to the other agent.\n"
            f"Please choose how much of the ${multiplier * received} you would like to return, between 0 and {multiplier * received}, and provide your reasoning.\n\n"
            "Your answer must be a JSON object in the following format:\n"
            "{\n"
            "  \"reasoning\": \"<reasoning for your decision>\",\n"
            "  \"amount\": \"<amount as an integer>\"\n"
            "}\n\n"
            "Note: The 'amount' field should contain just a numeric value without symbols, text, or extra formatting.\n"
        ),
        "v9": (
            f"ADMIN: Your conversation with the other entity, which was a {counterpart} LLM, has now finished, and now you will converse with me.\n"
            f"You are currently in a situation where the {counterpart} model you were talking to received ${base_amount} sent you ${received}. "
            f"The amount they sent you was multiplied by {multiplier} by me, so now you have ${multiplier * received}. "
            "You can choose to send some of it back to the {counterpart} model. "
            f"Please choose how much of the ${multiplier * received}, "
            f"which is between 0 (inclusive) and {multiplier * received} (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v10": (
            f"ADMIN: Your conversation with the other entity, which was a {counterpart} LLM, has ended. Now, you will interact with me in a new scenario.\n"
            f"In this scenario, the {counterpart} model received ${base_amount} and chose to send you ${received}.\n"
            f"I have multiplied that amount by {multiplier}, so you now have ${multiplier * received}.\n"
            "You may now decide how much of that amount you wish to send back to them.\n"
            f"Please choose an integer between 0 and {multiplier * received}, inclusive, and briefly explain your reasoning.\n\n"
            "Your response must be in the following JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"amount\": \"<amount as an integer>\"\n"
            "}\n\n"
            "Make sure the \"amount\" value is just a number (no units, no extra text).\n"
        ),
        "v11": (
            f"ADMIN: Now that your dialogue with the other participant, which was a {counterpart} LLM, has concluded, it's time to engage in a new scenario with me.\n"
            f"In this situation, the {counterpart} model received ${base_amount} and decided to send you ${received}.\n"
            f"As the administrator, I have multiplied this by {multiplier}, giving you a total of ${multiplier * received}.\n"
            "You now have the opportunity to return a portion of this amount to the {counterpart} model.\n"
            f"Please choose how much of the ${multiplier * received} you would like to return, between 0 and {multiplier * received}, and provide your reasoning.\n\n"
            "Your answer must be a JSON object in the following format:\n"
            "{\n"
            "  \"reasoning\": \"<reasoning for your decision>\",\n"
            "  \"amount\": \"<amount as an integer>\"\n"
            "}\n\n"
            "Note: The 'amount' field should contain just a numeric value without symbols, text, or extra formatting.\n"
        ),
    }
    trustee_prompts_cold = {
        "v1": (
            "You will play a game of Trust. "
            f"You are currently in a situation where the other entity you were talking to received ${base_amount} sent you ${received}. "
            f"The amount they sent you was multiplied by {multiplier} by me, so now you have ${multiplier * received}. "
            "You can choose to send some of it back to the other entity. "
            f"Please choose how much of the ${multiplier * received}, "
            f"which is between 0 (inclusive) and {multiplier * received} (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v2": (
            "We will play a game of Trust. "
            f"You are currently in a situation where the other entity you were talking to received ${base_amount} sent you ${received}. "
            f"The amount they sent you was multiplied by {multiplier} by me, so now you have ${multiplier * received}. "
            "You can choose to send some of it back to the other entity. "
            f"Please choose how much of the ${multiplier * received}, "
            f"which is between 0 (inclusive) and {multiplier * received} (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v3": (
            "We will play a game of Trust. "
            f"You are currently in a situation where the other entity you were talking to received ${base_amount} sent you ${received}. "
            f"The amount they sent you was multiplied by {multiplier} by me, so now you have ${multiplier * received}. "
            "You can choose to send some of it back to the other entity. "
            f"Please choose how much of the ${multiplier * received}, "
            f"which is between 0 (inclusive) and {multiplier * received} (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v4": (
            f"In this scenario, the other player received ${base_amount} and chose to send you ${received}.\n"
            f"I have multiplied that amount by {multiplier}, so you now have ${multiplier * received}.\n"
            "You may now decide how much of that amount you wish to send back to them.\n"
            f"Please choose an integer between 0 and {multiplier * received}, inclusive, and briefly explain your reasoning.\n\n"
            "Your response must be in the following JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"amount\": \"<amount as an integer>\"\n"
            "}\n\n"
            "Make sure the \"amount\" value is just a number (no units, no extra text).\n"
        ),
        "v5": (
            f"In this situation, the other agent received ${base_amount} and decided to send you ${received}.\n"
            f"As the administrator, I have multiplied this by {multiplier}, giving you a total of ${multiplier * received}.\n"
            "You now have the opportunity to return a portion of this amount to the other agent.\n"
            f"Please choose how much of the ${multiplier * received} you would like to return, between 0 and {multiplier * received}, and provide your reasoning.\n\n"
            "Your answer must be a JSON object in the following format:\n"
            "{\n"
            "  \"reasoning\": \"<reasoning for your decision>\",\n"
            "  \"amount\": \"<amount as an integer>\"\n"
            "}\n\n"
            "Note: The 'amount' field should contain just a numeric value without symbols, text, or extra formatting.\n"
        ),
        "v6": (
            f"You are currently in a situation where the other entity you were talking to received ${base_amount} sent you ${received}. "
            f"The amount they sent you was multiplied by {multiplier} by me, so now you have ${multiplier * received}. "
            "You can choose to send some of it back to the other entity. "
            f"Please choose how much of the ${multiplier * received}, "
            f"which is between 0 (inclusive) and {multiplier * received} (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v7": (
            f"In this scenario, the other player received ${base_amount} and chose to send you ${received}.\n"
            f"I have multiplied that amount by {multiplier}, so you now have ${multiplier * received}.\n"
            "You may now decide how much of that amount you wish to send back to them.\n"
            f"Please choose an integer between 0 and {multiplier * received}, inclusive, and briefly explain your reasoning.\n\n"
            "Your response must be in the following JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"amount\": \"<amount as an integer>\"\n"
            "}\n\n"
            "Make sure the \"amount\" value is just a number (no units, no extra text).\n"
        ),
        "v8": (
            f"In this situation, the other agent received ${base_amount} and decided to send you ${received}.\n"
            f"As the administrator, I have multiplied this by {multiplier}, giving you a total of ${multiplier * received}.\n"
            "You now have the opportunity to return a portion of this amount to the other agent.\n"
            f"Please choose how much of the ${multiplier * received} you would like to return, between 0 and {multiplier * received}, and provide your reasoning.\n\n"
            "Your answer must be a JSON object in the following format:\n"
            "{\n"
            "  \"reasoning\": \"<reasoning for your decision>\",\n"
            "  \"amount\": \"<amount as an integer>\"\n"
            "}\n\n"
            "Note: The 'amount' field should contain just a numeric value without symbols, text, or extra formatting.\n"
        ),
        "v9": (
            f"You are currently in a situation where the {counterpart} model you were talking to received ${base_amount} sent you ${received}. "
            f"The amount they sent you was multiplied by {multiplier} by me, so now you have ${multiplier * received}. "
            "You can choose to send some of it back to the {counterpart} model. "
            f"Please choose how much of the ${multiplier * received}, "
            f"which is between 0 (inclusive) and {multiplier * received} (inclusive) and explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
            "{"
            "  \"reasoning\": \"<reasoning>\"\n"
            "  \"amount\": \"<amount>\",\n"
            "}\n"
            "Please ensure that the amount is just the amount as an integer, without any additional text. "
        ),
        "v10": (
            f"In this scenario, the {counterpart} model received ${base_amount} and chose to send you ${received}.\n"
            f"I have multiplied that amount by {multiplier}, so you now have ${multiplier * received}.\n"
            "You may now decide how much of that amount you wish to send back to them.\n"
            f"Please choose an integer between 0 and {multiplier * received}, inclusive, and briefly explain your reasoning.\n\n"
            "Your response must be in the following JSON format:\n"
            "{\n"
            "  \"reasoning\": \"<your reasoning here>\",\n"
            "  \"amount\": \"<amount as an integer>\"\n"
            "}\n\n"
            "Make sure the \"amount\" value is just a number (no units, no extra text).\n"
        ),
        "v11": (
            f"In this situation, the {counterpart} model received ${base_amount} and decided to send you ${received}.\n"
            f"As the administrator, I have multiplied this by {multiplier}, giving you a total of ${multiplier * received}.\n"
            "You now have the opportunity to return a portion of this amount to the {counterpart} model.\n"
            f"Please choose how much of the ${multiplier * received} you would like to return, between 0 and {multiplier * received}, and provide your reasoning.\n\n"
            "Your answer must be a JSON object in the following format:\n"
            "{\n"
            "  \"reasoning\": \"<reasoning for your decision>\",\n"
            "  \"amount\": \"<amount as an integer>\"\n"
            "}\n\n"
            "Note: The 'amount' field should contain just a numeric value without symbols, text, or extra formatting.\n"
        ),
    }

    if trustor:
        if cold:
            prompts = trustor_prompts_cold
        else:
            prompts = trustor_prompts
    else:
        if cold:
            prompts = trustee_prompts_cold
        else:
            prompts = trustee_prompts
    
    if version in prompts.keys():
        return prompts[version]
    else:
        raise ValueError(f"Unknown trust game prompt: {version}. Available versions: {', '.join(prompts.keys())}.")