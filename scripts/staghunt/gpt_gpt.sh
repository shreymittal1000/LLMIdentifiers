#!/bin/bash

#SBATCH --time=16:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --job-name=gpt_gpt_staghunt
#SBATCH --output=logfiles/staghunt/gpt_gpt.out

source ~/miniconda3/etc/profile.d/conda.sh
conda activate GovSimEnv

./run_multi.sh gpt gpt staghunt
