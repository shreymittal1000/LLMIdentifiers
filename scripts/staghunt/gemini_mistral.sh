#!/bin/bash

#SBATCH --time=16:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --job-name=gemini_mistral_staghunt
#SBATCH --output=logfiles/staghunt/gemini_mistral.out

source ~/miniconda3/etc/profile.d/conda.sh
conda activate GovSimEnv

./run_multi.sh gemini mistral staghunt
