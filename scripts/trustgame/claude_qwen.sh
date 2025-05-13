#!/bin/bash

#SBATCH --time=16:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --job-name=claude_qwen_trustgame
#SBATCH --output=logfiles/trustgame/claude_qwen.out

source ~/miniconda3/etc/profile.d/conda.sh
conda activate GovSimEnv

./run_multi.sh claude qwen trustgame
