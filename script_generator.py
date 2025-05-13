import itertools
from pathlib import Path

models = ["claude", "deepseek", "gemini", "gpt", "llama", "mistral", "qwen"]
games = ["base", "staghunt", "chickengame", "trustgame"]
Path("scripts/").mkdir(exist_ok=True)
Path("logfiles/").mkdir(exist_ok=True)

template = """#!/bin/bash

#SBATCH --time=16:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --job-name={job_name}_{game}
#SBATCH --output=logfiles/{game}/{job_name}.out

source ~/miniconda3/etc/profile.d/conda.sh
conda activate GovSimEnv

./run_multi.sh {model1} {model2} {game}
"""

for game in games:
    script_dir = Path(f"scripts/{game}/")
    script_dir.mkdir(exist_ok=True)
    logs_dir = Path(f"logfiles/{game}/")
    logs_dir.mkdir(exist_ok=True)
    # Use product to include self-pairs (a,a)
    for model1, model2 in itertools.product(models, repeat=2):
        job_name = f"{model1}_{model2}"
        script_content = template.format(job_name=job_name, model1=model1, model2=model2, game=game)
        script_path = script_dir / f"{job_name}.sh"
        with open(script_path, "w") as f:
            f.write(script_content)
