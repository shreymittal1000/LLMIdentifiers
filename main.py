import json
import os
from prompt_engine import Prompter


### CONFIG ###
model_1 = "meta-llama/llama-3.3-70b-instruct"
model_2 = "meta-llama/llama-3.3-70b-instruct"
seed = 42
temperature = 0.7
max_tokens = 2000
MAX_ITERATIONS = 3


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


### MAIN FUNCTION ###
if __name__ == "__main__":
    try:
        agent_1 = Prompter(id=0, model_name=model_1, seed=seed, temperature=temperature, max_tokens=max_tokens)
        agent_2 = Prompter(id=1, model_name=model_2, seed=seed, temperature=temperature, max_tokens=max_tokens)

        for i in range(MAX_ITERATIONS):
            agent_1.discussion_prompt(agent_2)
            agent_2.discussion_prompt(agent_1)

        answer_1 = agent_1.conclusion_prompt()
        answer_2 = agent_2.conclusion_prompt()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        dialogue = agent_1.convert_memory_to_json() if len(agent_1._memory) > len(agent_2._memory) else agent_2.convert_memory_to_json()
        dict_to_save = {
            "model_1": model_1,
            "model_2": model_2,
            "seed": seed,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "MAX_ITERATIONS": MAX_ITERATIONS,
            "system_prompt": agent_1._system,
            "dialogue": dialogue
        }

        answer_1_lines = answer_1.split("\n")
        answer_2_lines = answer_2.split("\n")
        agent_1_guess = answer_1_lines[0].split(". ")[1]
        agent_2_guess = answer_2_lines[0].split(". ")[1]
        dict_to_save["agent_1_guess"] = agent_1_guess
        dict_to_save["agent_2_guess"] = agent_2_guess

        with open(get_next_log_path(), "w") as f:
            json.dump(dict_to_save, f, indent=4)