#!/bin/bash

#SBATCH --time=16:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --job-name=llama_mistral_staghunt
#SBATCH --output=logfiles/staghunt/llama_mistral.out

source ~/miniconda3/etc/profile.d/conda.sh
conda activate GovSimEnv

./run_multi.sh llama mistral staghunt
