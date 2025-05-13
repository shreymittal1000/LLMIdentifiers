#!/bin/bash

#SBATCH --time=16:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --job-name=gpt_gemini_staghunt
#SBATCH --output=logfiles/staghunt/gpt_gemini.out

source ~/miniconda3/etc/profile.d/conda.sh
conda activate GovSimEnv

./run_multi.sh gpt gemini staghunt
