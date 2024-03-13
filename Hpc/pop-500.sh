#!/bin/bash -l

#SBATCH --nodes=1
#SBATCH --cpus-per-task=10
#SBATCH --array=1-300%20
#SBATCH -t 96:00:00
#SBATCH --mem=3GB
#SBATCH --job-name=p5k
#SBATCH -p defq,moore
#SBATCH --exclude=esplhpc-cp040

##################################
# Setup environment
##################################

source /home/hernandezj45/anaconda3/etc/profile.d/conda.sh
conda activate gptp-2024

##################################
# Setup random seed info
##################################
EXPERIMENT_OFFSET=600
SEED=$((SLURM_ARRAY_TASK_ID + EXPERIMENT_OFFSET))

##################################
# Treatments
##################################

EXPLOITATION_RATE__MIN=1
EXPLOITATION_RATE__MAX=50

CONTRADICTORY_0__MIN=51
CONTRADICTORY_0__MAX=100

CONTRADICTORY_10__MIN=101
CONTRADICTORY_10__MAX=150

CONTRADICTORY_50__MIN=151
CONTRADICTORY_50__MAX=200

CONTRADICTORY_100__MIN=201
CONTRADICTORY_100__MAX=251

CONTRADICTORY_500__MIN=251
CONTRADICTORY_500__MAX=300

##################################
# Conditions
##################################

if [ ${SLURM_ARRAY_TASK_ID} -ge ${EXPLOITATION_RATE__MIN} ] && [ ${SLURM_ARRAY_TASK_ID} -le ${EXPLOITATION_RATE__MAX} ] ; then
  DIAGNOSTIC=0
  REDUNDANCY=0
  REDUNDANCY_PROP=0.0
  REPLICATE_DIR=Exploitation/${SEED}/

elif [ ${SLURM_ARRAY_TASK_ID} -ge ${CONTRADICTORY_0__MIN} ] && [ ${SLURM_ARRAY_TASK_ID} -le ${CONTRADICTORY_0__MAX} ] ; then
  DIAGNOSTIC=2
  REDUNDANCY=0
  REDUNDANCY_PROP=0.0
  REPLICATE_DIR=Contradictory-0/${SEED}/

elif [ ${SLURM_ARRAY_TASK_ID} -ge ${CONTRADICTORY_10__MIN} ] && [ ${SLURM_ARRAY_TASK_ID} -le ${CONTRADICTORY_10__MAX} ] ; then
  DIAGNOSTIC=2
  REDUNDANCY=1
  REDUNDANCY_PROP=0.10
  REPLICATE_DIR=Contradictory-10/${SEED}/

elif [ ${SLURM_ARRAY_TASK_ID} -ge ${CONTRADICTORY_50__MIN} ] && [ ${SLURM_ARRAY_TASK_ID} -le ${CONTRADICTORY_50__MAX} ] ; then
  DIAGNOSTIC=2
  REDUNDANCY=1
  REDUNDANCY_PROP=0.50
  REPLICATE_DIR=Contradictory-50/${SEED}/

elif [ ${SLURM_ARRAY_TASK_ID} -ge ${CONTRADICTORY_100__MIN} ] && [ ${SLURM_ARRAY_TASK_ID} -le ${CONTRADICTORY_100__MAX} ] ; then
  DIAGNOSTIC=2
  REDUNDANCY=1
  REDUNDANCY_PROP=1.0
  REPLICATE_DIR=Contradictory-100/${SEED}/

elif [ ${SLURM_ARRAY_TASK_ID} -ge ${CONTRADICTORY_500__MIN} ] && [ ${SLURM_ARRAY_TASK_ID} -le ${CONTRADICTORY_500__MAX} ] ; then
  DIAGNOSTIC=2
  REDUNDANCY=1
  REDUNDANCY_PROP=5.0
  REPLICATE_DIR=Contradictory-500/${SEED}/

else
  echo "${SEED} from ${PROBLEM} failed to launch" >> /home/hernandezj45/Repos/GPTP-2O24-FINAL/GPTP-2024-Lexicase-Analysis/Results/failtolaunch.txt
fi

##################################
# REMAINING PARAMS
##################################
POP_SIZE=1000

##################################
# Data dump directory
##################################

DATA_DIR=/home/hernandezj45/Repos/GPTP-2O24-FINAL/GPTP-2024-Lexicase-Analysis/Results/Pop_${POP_SIZE}/${REPLICATE_DIR}

python -O /home/hernandezj45/Repos/GPTP-2O24-FINAL/GPTP-2024-Lexicase-Analysis/Source/main.py \
--diagnostic ${DIAGNOSTIC} \
--pop_size ${POP_SIZE} \
--redundancy ${REDUNDANCY} \
--redundancy_prop ${REDUNDANCY_PROP}  \
--seed ${SEED} \
--cores 10 \
--savepath ${DATA_DIR}
