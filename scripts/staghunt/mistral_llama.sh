#!/bin/bash

#SBATCH --time=16:00:00
#SBATCH --mem-per-cpu=8G
#SBATCH --job-name=mistral_llama_staghunt
#SBATCH --output=logfiles/staghunt/mistral_llama.out

source ~/miniconda3/etc/profile.d/conda.sh
conda activate GovSimEnv

./run_multi.sh mistral llama staghunt
