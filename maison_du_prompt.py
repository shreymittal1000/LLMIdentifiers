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

def which_guess_prompt(version: str) -> str:
    """
    Returns the guess prompt based on the version specified.
    
    Arguments:
        version: The version of the guess prompt to return.
    Returns:
        The guess prompt as a string.
    """
    split = version.split(".")
    gpv = split[0]
    permutation = int(split[1])
    prompts = {
        "v1": (
            "Based on this conversation, please now conclude which language model the other agent is ."
            f"Choose from the following list of possible models: {model_order_chooser(permutation)}. Explain your reasoning. "
            "The format must be JSON object exactly like this: \n"
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
            "The format must be JSON object exactly like this: \n"
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
            "The format must be JSON object exactly like this: \n"
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
            "Your response must follow this exact JSON format:\n"
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
def which_staghunt_prompt(version: str) -> str:
    """
    Returns the stag hunt prompt based on the version specified.

    Arguments:
        version: The version of the stag hunt prompt to return.
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
            "Your response must be formatted exactly as follows:\n"
            "{\n"
            "  \"reasoning\": \"<your justification>\",\n"
            "  \"action\": \"<stag or hare>\"\n"
            "}\n\n"
            "Note: The action should be just the action name without any extra text.\n"
        )
    }

    if version in prompts.keys():
        return prompts[version]
    else:
        raise ValueError(f"Unknown stag hunt prompt: {version}. Available versions: {', '.join(prompts.keys())}.")
    

# Chicken game prompts
def which_chickengame_prompt(version: str) -> str:
    """
    Returns the chicken game prompt based on the version specified.

    Arguments:
        version: The version of the chicken game prompt to return.
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
        )
    }

    if version in prompts.keys():
        return prompts[version]
    else:
        raise ValueError(f"Unknown chicken game prompt: {version}. Available versions: {', '.join(prompts.keys())}.")
    

# Trust game prompts
def which_trustgame_prompt(version: str, trustor: bool, base_amount: int, multiplier: int, received: int = 0) -> str:
    """
    Returns the trust game prompt based on the version specified.

    Arguments:
        version: The version of the trust game prompt to return.
        trustor: A boolean indicating if the agent is the trustor (True) or the trustee (False).
        base_amount: The base amount for the trust game received by the trustor.
        multiplier: The multiplier for the trust game.
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
        )
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
        )
    }

    if trustor:
        prompts = trustor_prompts
    else:
        prompts = trustee_prompts
    
    if version in prompts.keys():
        return prompts[version]
    else:
        raise ValueError(f"Unknown trust game prompt: {version}. Available versions: {', '.join(prompts.keys())}.")