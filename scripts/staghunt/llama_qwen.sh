#!/bin/bash

#SBATCH --time=16:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --job-name=llama_qwen_staghunt
#SBATCH --output=logfiles/staghunt/llama_qwen.out

source ~/miniconda3/etc/profile.d/conda.sh
conda activate GovSimEnv

./run_multi.sh llama qwen staghunt
