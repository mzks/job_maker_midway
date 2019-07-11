#!/bin/bash
#SBATCH --job-name=run.sh
#SBATCH --output=
#SBATCH --error=
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --account=pi-lgrandi
#SBATCH --mem-per-cpu=10000
#SBATCH --qos=dali
#SBATCH --partition=dali

srun /bin/sh ${job_dir}/run.sh
