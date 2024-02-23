#!/bin/bash -l

#SBATCH --nodes=1
#SBATCH --cpus-per-task=20
#SBATCH --array=1-250%20
#SBATCH -t 10:00:00
#SBATCH --mem=1GB
#SBATCH --job-name=con-500
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
PRELIM_OFFSET=10000
EXPERIMENT_OFFSET=2500
SEED=$((SLURM_ARRAY_TASK_ID + EXPERIMENT_OFFSET + PRELIM_OFFSET))

##################################
# Treatments
##################################

POP__SIZE__5000__MIN=1
POP__SIZE__5000__MAX=50

POP__SIZE__1000__MIN=51
POP__SIZE__1000__MAX=100

POP__SIZE__500__MIN=101
POP__SIZE__500__MAX=150

POP__SIZE__100__MIN=151
POP__SIZE__100__MAX=200

POP__SIZE__50__MIN=201
POP__SIZE__50__MAX=250

##################################
# Conditions
##################################

if [ ${SLURM_ARRAY_TASK_ID} -ge ${POP__SIZE__5000__MIN} ] && [ ${SLURM_ARRAY_TASK_ID} -le ${POP__SIZE__5000__MAX} ] ; then
  POP_SIZE=5000
  GENERATIONS=5000

elif [ ${SLURM_ARRAY_TASK_ID} -ge ${POP__SIZE__1000__MIN} ] && [ ${SLURM_ARRAY_TASK_ID} -le ${POP__SIZE__1000__MAX} ] ; then
  POP_SIZE=1000
  GENERATIONS=25000

elif [ ${SLURM_ARRAY_TASK_ID} -ge ${POP__SIZE__500__MIN} ] && [ ${SLURM_ARRAY_TASK_ID} -le ${POP__SIZE__500__MAX} ] ; then
  POP_SIZE=500
  GENERATIONS=50000

elif [ ${SLURM_ARRAY_TASK_ID} -ge ${POP__SIZE__100__MIN} ] && [ ${SLURM_ARRAY_TASK_ID} -le ${POP__SIZE__100__MAX} ] ; then
  POP_SIZE=100
  GENERATIONS=250000

elif [ ${SLURM_ARRAY_TASK_ID} -ge ${POP__SIZE__50__MIN} ] && [ ${SLURM_ARRAY_TASK_ID} -le ${POP__SIZE__50__MAX} ] ; then
  POP_SIZE=50
  GENERATIONS=500000

else
  echo "${SEED} from ${PROBLEM} failed to launch" >> /mnt/ls15/scratch/users/herna383/ps-coh-failtolaunch.txt
fi

##################################
# Data dump directory
##################################

DATA_DIR=/home/hernandezj45/Repos/GPTP-2024-Lexicase-Analysis/Results/Specialist_Maintenance/500/${POP_SIZE}-${SEED}/
mkdir -p ${DATA_DIR}

##################################
# REMAINING PARAMS
##################################
DIAGNOSTIC=2
REDUNDANCY=1
REDUNDANCY_PROP=5.0

python /home/hernandezj45/Repos/GPTP-2024-Lexicase-Analysis/Source/main.py \
--diagnostic ${DIAGNOSTIC} \
--generations ${GENERATIONS} \
--pop_size ${POP_SIZE} \
--redundancy ${REDUNDANCY} \
--redundancy_prop ${REDUNDANCY_PROP}  \
--seed ${SEED} \
--savepath ${DATA_DIR} \
--cores 20