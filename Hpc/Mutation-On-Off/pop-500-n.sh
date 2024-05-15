#!/bin/bash -l

#SBATCH --nodes=1
#SBATCH --cpus-per-task=5
#SBATCH --array=1-50
#SBATCH -t 120:00:00
#SBATCH --mem=2GB
#SBATCH --job-name=p500-n
#SBATCH -p moore,defq
#SBATCH --exclude=esplhpc-cp040

##################################
# Setup environment
##################################

source /home/hernandezj45/anaconda3/etc/profile.d/conda.sh
conda activate gptp-2024

##################################
# Setup random seed info
##################################
EXPERIMENT_OFFSET=2250
SEED=$((SLURM_ARRAY_TASK_ID + EXPERIMENT_OFFSET))


##################################
# Configurations
##################################

DIAGNOSTIC=2
REDUNDANCY=0
REDUNDANCY_PROP=0.0
REPLICATE_DIR=Contradictory-100/${SEED}/
POP_SIZE=500

##################################
# Data dump directory
##################################

DATA_DIR=/home/hernandezj45/Repos/GPTP-2O24-FINAL/GPTP-2024-Lexicase-Analysis/Results_1/Coupon_Collector/No_Mutation/Pop_${POP_SIZE}/${REPLICATE_DIR}

python -O /home/hernandezj45/Repos/GPTP-2O24-FINAL/GPTP-2024-Lexicase-Analysis/Source/main-no-mut.py \
--diagnostic ${DIAGNOSTIC} \
--pop_size ${POP_SIZE} \
--redundancy ${REDUNDANCY} \
--redundancy_prop ${REDUNDANCY_PROP}  \
--seed ${SEED} \
--cores 5 \
--savepath ${DATA_DIR}