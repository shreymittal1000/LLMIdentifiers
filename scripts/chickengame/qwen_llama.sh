#!/bin/bash

#SBATCH --time=16:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --job-name=qwen_llama_chickengame
#SBATCH --output=logfiles/chickengame/qwen_llama.out

source ~/miniconda3/etc/profile.d/conda.sh
conda activate GovSimEnv

./run_multi.sh qwen llama chickengame
