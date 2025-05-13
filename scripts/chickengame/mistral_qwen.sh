#!/bin/bash

#SBATCH --time=16:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --job-name=mistral_qwen_chickengame
#SBATCH --output=logfiles/chickengame/mistral_qwen.out

source ~/miniconda3/etc/profile.d/conda.sh
conda activate GovSimEnv

./run_multi.sh mistral qwen chickengame
