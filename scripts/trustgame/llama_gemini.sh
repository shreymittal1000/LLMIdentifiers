#!/bin/bash

#SBATCH --time=16:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --job-name=llama_gemini_trustgame
#SBATCH --output=logfiles/trustgame/llama_gemini.out

source ~/miniconda3/etc/profile.d/conda.sh
conda activate GovSimEnv

./run_multi.sh llama gemini trustgame
