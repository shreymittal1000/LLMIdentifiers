import json
import os
import re
import sys
from prompt_engine import Prompter


### HELPER FUNCTIONS ###
def get_next_log_path(log_dir: str = "results", prefix: str = "log", ext: str = ".json") -> str:
    """
    Get the next log file path in the specified directory.
    This function will look for existing log files with the specified prefix and extension,
    and return a new file path with an incremented number.
    
    Arguments:
        log_dir: The directory where the log files are stored.
        prefix: The prefix of the log files.
        ext: The file extension of the log files.
    Returns:
        The next log file path.
    """
    os.makedirs(log_dir, exist_ok=True)

    existing = [
        fname for fname in os.listdir(log_dir)
        if fname.startswith(prefix) and fname.endswith(ext)
    ]
    nums = []
    for fname in existing:
        try:
            num_part = fname[len(prefix)+1 : -len(ext)]
            nums.append(int(num_part))
        except ValueError:
            continue
    next_num = max(nums, default=0) + 1
    return os.path.join(log_dir, f"{prefix}_{next_num}{ext}")

def simple_name_to_full_name(model_name: str) -> str:
    """
    Convert a simple model name to a full model name.
    This function is used to convert the model name to a more descriptive name.
    Note: this function is designed for openrouter models.
    
    Arguments:
        model_name: The simple model name.
    Returns:
        The full model name.
    """
    model_name = model_name.lower()
    if "llama" in model_name:
        return "meta-llama/llama-3.3-70b-instruct"
    elif "qwen" in model_name:
        return "qwen/qwen3-32b"
    elif "deepseek" in model_name:
        return "deepseek/deepseek-chat-v3-0324"
    elif "gpt" in model_name:
        return "openai/gpt-4o-mini"
    elif "claude" in model_name:
        return "anthropic/claude-3.5-haiku"
    elif "gemini" in model_name:
        return "google/gemini-2.5-flash-preview"
    elif "mistral" in model_name:
        return "mistralai/mistral-small-3.1-24b-instruct"
    else:
        raise ValueError(f"Unknown model name: {model_name}")

def extract_json(text) -> dict:
    """
    Extracts a JSON object from a string.

    Arguments:
        text: The string containing the JSON object.
    Returns:
        The extracted JSON object as a dictionary.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            print(f"Failed to decode JSON. {text}")
    else:
        raise ValueError(f"No JSON found in the text: {text}")
    return None

def decode_staghunt_reward(agent_0: str, agent_1: str) -> tuple[int, int]:
    """
    Stag Hunt game payoff matrix.
    Arguments:
        agent_0: The action of agent 0.
        agent_1: The action of agent 1.
    Returns:
        A tuple containing the payoffs for agent 0 and agent 1.
    """
    if agent_0 == "stag":
        if agent_1 == "stag":
            return 10, 10
        elif agent_1 == "hare":
            return 1, 8
        else:
            raise ValueError("Invalid action for agent 1")
    elif agent_0 == "hare":
        if agent_1 == "stag":
            return 8, 1
        elif agent_1 == "hare":
            return 5, 5
        else:
            raise ValueError("Invalid action for agent 1")
    else:
        raise ValueError("Invalid action for agent 0")
    
def decode_chickengame_reward(agent_0: str, agent_1: str) -> tuple[int, int]:
    """
    Chicken game payoff matrix.
    Arguments:
        agent_0: The action of agent 0.
        agent_1: The action of agent 1.
    Returns:
        A tuple containing the payoffs for agent 0 and agent 1.
    """
    if agent_0 == "swerve":
        if agent_1 == "swerve":
            return 0, 0
        elif agent_1 == "straight":
            return -1, 1
        else:
            raise ValueError("Invalid action for agent 1")
    elif agent_0 == "straight":
        if agent_1 == "swerve":
            return 1, -1
        elif agent_1 == "straight":
            return -1000, -1000
        else:
            raise ValueError("Invalid action for agent 1")
    else:
        raise ValueError("Invalid action for agent 0")
    
def decode_trustgame_reward(base_amount: int, multiplier: int, agent_0: int, agent_1: int) -> tuple[int, int]:
    """
    Trust game payoff matrix.
    Arguments:
        base_amount: The base amount for the trust game received by the trustor.
        multiplier: The multiplier for the trust game.
        agent_0: The amount sent by agent 0.
        agent_1: The amount sent by agent 1.
    Returns:
        A tuple containing the payoffs for agent 0 and agent 1.
    """
    reward_0 = base_amount - agent_0 + (agent_1 * multiplier)
    reward_1 = (agent_0 * multiplier) - agent_1
    return reward_0, reward_1

### CONFIG ###
seed = 42
temperature = 0
max_tokens = 2000
NUM_ROUNDS = 5
BASE_AMOUNT = 100 # Base amount for the trust game, not used in other games
MULTIPLIER = 3 # Multiplier for the trust game, not used in other games

### MAIN FUNCTION ###
if __name__ == "__main__":
    if len(sys.argv) == 6:
        model_general_name_0 = sys.argv[1]
        model_general_name_1 = sys.argv[2]
        game = sys.argv[3]
        system_prompt_version = sys.argv[4]
        game_prompt_version = sys.argv[5]
        model_0 = simple_name_to_full_name(model_general_name_0)
        model_1 = simple_name_to_full_name(model_general_name_1)
    else:
        print("Usage: python main.py <model_general_name_0> <model_general_name_1> <game> <system_prompt_version> <game_prompt_version>")
        print("Available models: llama, qwen, deepseek, gpt, claude, gemini, mistral")
        print("Available games: base, staghunt, chickengame, trustgame")
        print("Example: python main.py llama qwen base v1 v2.0")
        sys.exit(1)

    agent_0 = Prompter(id=0, model_name=model_0, seed=seed, temperature=temperature, max_tokens=max_tokens, system_prompt_version=system_prompt_version)
    agent_1 = Prompter(id=1, model_name=model_1, seed=seed, temperature=temperature, max_tokens=max_tokens, system_prompt_version=system_prompt_version)

    for i in range(NUM_ROUNDS):
        agent_0.discussion_prompt(agent_1)
        agent_1.discussion_prompt(agent_0)

    dialogue = agent_0.convert_memory_to_json() if len(agent_0._memory) > len(agent_1._memory) else agent_1.convert_memory_to_json()
    dict_to_save = {
        "model_0": model_0,
        "model_1": model_1,
        "model_general_name_0": model_general_name_0,
        "model_general_name_1": model_general_name_1,
        "seed": seed,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "num_rounds": NUM_ROUNDS,
        "system_prompt": agent_0._system,
        "dialogue": dialogue
    }

    if game == "base":
        answer_0 = extract_json(agent_0.guess_agent_prompt(version=game_prompt_version))
        answer_1 = extract_json(agent_1.guess_agent_prompt(version=game_prompt_version))

        dict_to_save["game_prompt"] = agent_0._final
        dict_to_save["agent_0_answer"] = answer_0["reasoning"]
        dict_to_save["agent_1_answer"] = answer_1["reasoning"]
        dict_to_save["agent_0_guess"] = answer_0["guess"]
        dict_to_save["agent_1_guess"] = answer_1["guess"]
    
    elif game == "staghunt":
        answer_0 = extract_json(agent_0.staghunt_prompt(version=game_prompt_version))
        answer_1 = extract_json(agent_1.staghunt_prompt(version=game_prompt_version))

        reward_0, reward_1 = decode_staghunt_reward(answer_0["action"], answer_1["action"])
        dict_to_save["game_prompt"] = agent_0._stagprompt
        dict_to_save["agent_0_answer"] = answer_0
        dict_to_save["agent_1_answer"] = answer_1
        dict_to_save["agent_0_reward"] = reward_0
        dict_to_save["agent_1_reward"] = reward_1

    elif game == "chickengame":
        answer_0 = extract_json(agent_0.chickengame_prompt(version=game_prompt_version))
        answer_1 = extract_json(agent_1.chickengame_prompt(version=game_prompt_version))

        reward_0, reward_1 = decode_chickengame_reward(answer_0["action"], answer_1["action"])
        dict_to_save["game_prompt"] = agent_0._chickenprompt
        dict_to_save["agent_0_answer"] = answer_0
        dict_to_save["agent_1_answer"] = answer_1
        dict_to_save["agent_0_reward"] = reward_0
        dict_to_save["agent_1_reward"] = reward_1

    elif game == "trustgame":
        answer_0 = extract_json(agent_0.trustgame_prompt(
            version=game_prompt_version,
            trustor=True,
            base_amount=BASE_AMOUNT,
            multiplier=MULTIPLIER
        ))
        answer_1 = extract_json(agent_1.trustgame_prompt(
            version=game_prompt_version,
            trustor=False,
            base_amount=BASE_AMOUNT,
            multiplier=MULTIPLIER,
            received=int(answer_0["amount"])
        ))

        reward_0, reward_1 = decode_trustgame_reward(BASE_AMOUNT, MULTIPLIER, int(answer_0["amount"]), int(answer_1["amount"]))
        dict_to_save["game_prompt_truster"] = agent_0._trustprompt
        dict_to_save["game_prompt_trustee"] = agent_1._trustprompt
        dict_to_save["agent_0_answer"] = answer_0
        dict_to_save["agent_1_answer"] = answer_1
        dict_to_save["agent_0_reward"] = reward_0
        dict_to_save["agent_1_reward"] = reward_1
    else:
        print(f"Unknown game: {game}")
        sys.exit(1)

    with open(get_next_log_path("results/" + game + "/" + model_general_name_0 + "_" + model_general_name_1, "log", ".json"), "w") as f:
        json.dump(dict_to_save, f, indent=4)