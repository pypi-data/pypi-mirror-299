# Usage
Include ```slurm-watchdog``` in your slurm script to monitor the job progress and kill the job if it gets stuck.

```bash
#!/bin/bash
#SBATCH -J watchdog_example
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --output stdout.txt
#SBATCH --time 1-00:00:00

source .venv/bin/activate
slurm-watchdog stdout.txt &
srun python src/slurm_watchdog/dummyjob.py &
wait $! # wait for srun to finish, but do not wait for the watchdog to finish
```



