#!/bin/bash

#SBATCH --time=16:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --job-name=gemini_deepseek_staghunt
#SBATCH --output=logfiles/staghunt/gemini_deepseek.out

source ~/miniconda3/etc/profile.d/conda.sh
conda activate GovSimEnv

./run_multi.sh gemini deepseek staghunt
