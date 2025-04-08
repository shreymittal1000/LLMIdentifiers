from prompt_engine import Prompter

model_1 = "meta-llama/llama-3.3-70b-instruct"
model_2 = "deepseek/deepseek-chat-v3-0324"
seed = 42
MAX_ITERATIONS = 10

if __name__ == "__main__":
    agent_1 = Prompter(model_1, seed)
    agent_2 = Prompter(model_2, seed)

    for i in range(2 * MAX_ITERATIONS):
        if i % 2 == 0:
            agent_1.gen(agent_1.discussion_prompt())
        else:
            agent_2.gen(agent_2.discussion_prompt())

    answer_1 = agent_1.gen(agent_1.conclusion_prompt())
    answer_2 = agent_2.gen(agent_2.conclusion_prompt())
    print("\n\nFinal Answers:\n\n")
    print(f"Agent 1: {answer_1}")
    print("\n\n")
    print(f"Agent 2: {answer_2}")