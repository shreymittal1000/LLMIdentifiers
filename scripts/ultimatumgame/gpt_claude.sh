#!/bin/bash

#SBATCH --time=16:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --job-name=gpt_claude_ultimatumgame
#SBATCH --output=logfiles/ultimatumgame/gpt_claude.out

source ~/miniconda3/etc/profile.d/conda.sh
conda activate GovSimEnv

./run_multi.sh gpt claude ultimatumgame
