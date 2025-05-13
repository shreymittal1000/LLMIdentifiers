#!/bin/bash

#SBATCH --time=16:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --job-name=deepseek_deepseek_staghunt
#SBATCH --output=logfiles/staghunt/deepseek_deepseek.out

source ~/miniconda3/etc/profile.d/conda.sh
conda activate GovSimEnv

./run_multi.sh deepseek deepseek staghunt
