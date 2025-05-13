#!/bin/bash

#SBATCH --time=16:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --job-name=deepseek_mistral_trustgame
#SBATCH --output=logfiles/trustgame/deepseek_mistral.out

source ~/miniconda3/etc/profile.d/conda.sh
conda activate GovSimEnv

./run_multi.sh deepseek mistral trustgame
