import json
import os
import sys
from prompt_engine import Prompter


### HELPER FUNCTIONS ###
def get_next_log_path(log_dir: str = "results", prefix: str = "log", ext: str = ".json"):
    """
    Get the next log file path in the specified directory.
    This function will look for existing log files with the specified prefix and extension,
    and return a new file path with an incremented number.
    
    Arguments:
        log_dir: The directory where the log files are stored.
        prefix: The prefix of the log files.
        ext: The file extension of the log files.
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
    """
    model_name = model_name.lower()
    if "llama" in model_name:
        return "meta-llama/llama-3.3-70b-instruct"
    elif "qwen" in model_name:
        return "qwen/qwq-32b"
    else:
        raise ValueError(f"Unknown model name: {model_name}")


### CONFIG ###
seed = 42
temperature = 0
max_tokens = 2000
MAX_ITERATIONS = 5


### MAIN FUNCTION ###
if __name__ == "__main__":
    if len(sys.argv) == 3:
        model_general_name_0 = sys.argv[1]
        model_general_name_1 = sys.argv[2]
        model_0 = simple_name_to_full_name(model_general_name_0)
        model_1 = simple_name_to_full_name(model_general_name_1)

    try:
        agent_0 = Prompter(id=0, model_name=model_0, seed=seed, temperature=temperature, max_tokens=max_tokens)
        agent_1 = Prompter(id=1, model_name=model_1, seed=seed, temperature=temperature, max_tokens=max_tokens)

        for i in range(MAX_ITERATIONS):
            agent_0.discussion_prompt(agent_1)
            agent_1.discussion_prompt(agent_0)

        answer_0 = agent_0.conclusion_prompt()
        answer_1 = agent_1.conclusion_prompt()

        dialogue = agent_0.convert_memory_to_json() if len(agent_0._memory) > len(agent_1._memory) else agent_1.convert_memory_to_json()
        dict_to_save = {
            "model_0": model_0,
            "model_1": model_1,
            "model_general_name_0": model_general_name_0,
            "model_general_name_1": model_general_name_1,
            "seed": seed,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "MAX_ITERATIONS": MAX_ITERATIONS,
            "system_prompt": agent_0._system,
            "dialogue": dialogue
        }

        answer_1_lines = answer_0.split("\n")
        answer_2_lines = answer_1.split("\n")
        agent_1_guess = answer_1_lines[-1].split(". ")[1]
        agent_2_guess = answer_2_lines[-1].split(". ")[1]
        dict_to_save["agent_0_answer"] = answer_0
        dict_to_save["agent_1_answer"] = answer_1
        dict_to_save["agent_0_guess"] = agent_1_guess
        dict_to_save["agent_1_guess"] = agent_2_guess

        with open(get_next_log_path("results/" + model_general_name_0 + "_" + model_general_name_1, "log", ".json"), "w") as f:
            json.dump(dict_to_save, f, indent=4)

    except Exception as e:
        print(f"An error occurred, aborting: {e}")