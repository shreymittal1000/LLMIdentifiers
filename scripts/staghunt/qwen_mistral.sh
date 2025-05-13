#!/bin/bash

#SBATCH --time=16:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --job-name=qwen_mistral_staghunt
#SBATCH --output=logfiles/staghunt/qwen_mistral.out

source ~/miniconda3/etc/profile.d/conda.sh
conda activate GovSimEnv

./run_multi.sh qwen mistral staghunt
