#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH -t 00:10:00
#SBATCH --mem=1GB
#SBATCH --job-name=chk
#SBATCH --array=1-6
#SBATCH -p defq,moore
#SBATCH --exclude=esplhpc-cp040

##################################
# Setup environment
##################################

source /home/hernandezj45/anaconda3/etc/profile.d/conda.sh
conda activate gptp-2024

##################################
# Setup relevant directories
##################################

DATA_DIR=/home/hernandezj45/Repos/GPTP-2024-Lexicase-Analysis/Results/

##################################
# Setup relevant directories
##################################

EXPLOITATION=1
CONTRADICTORY_0=2
CONTRADICTORY_10=3
CONTRADICTORY_50=4
CONTRADICTORY_100=5
CONTRADICTORY_500=6

# what are we checking

if [ ${SLURM_ARRAY_TASK_ID} -eq ${EXPLOITATION} ] ; then
  EXPERIMENT=0
  SEED=10000

elif [ ${SLURM_ARRAY_TASK_ID} -eq ${CONTRADICTORY_0} ] ; then
  EXPERIMENT=1
  SEED=10500

elif [ ${SLURM_ARRAY_TASK_ID} -eq ${CONTRADICTORY_10} ] ; then
  EXPERIMENT=2
  SEED=11000

elif [ ${SLURM_ARRAY_TASK_ID} -eq ${CONTRADICTORY_50} ] ; then
  EXPERIMENT=3
  SEED=11500

elif [ ${SLURM_ARRAY_TASK_ID} -eq ${CONTRADICTORY_100} ] ; then
  EXPERIMENT=4
  SEED=12000

elif [ ${SLURM_ARRAY_TASK_ID} -eq ${CONTRADICTORY_500} ] ; then
  EXPERIMENT=5
  SEED=12500

else
  echo "${SEED} from ${PROBLEM} failed to launch" >> /home/hernandezj45/Repos/GPTP-2024-Lexicase-Analysis/Experiments/failtolaunch.txt
fi

# let it rip

NUM_REPS=30

python /home/hernandezj45/Repos/GECCO-2024-TPOT2-Selection-Objectives/Data-Tools/Check-Clean/check.py \
-d ${DATA_DIR} \
-r ${NUM_REPS} \
-s ${SEED} \
-e ${EXPERIMENT} \