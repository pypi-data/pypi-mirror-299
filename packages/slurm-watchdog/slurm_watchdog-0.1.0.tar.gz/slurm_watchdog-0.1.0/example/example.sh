#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --output stdout.txt

source .venv/bin/activate
slurm-watchdog --initial-wait 5 --t-check 5 --t-warn 5 --t-kill 10 stdout.txt &
srun python ../src/slurm_watchdog/dummyjob.py &
wait $! # wait for srun to finish, but do not wait for the watchdog to finish