#!/bin/bash

#SBATCH --time=16:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --job-name=llama_llama_trustgame
#SBATCH --output=logfiles/trustgame/llama_llama.out

source ~/miniconda3/etc/profile.d/conda.sh
conda activate GovSimEnv

./run_multi.sh llama llama trustgame
