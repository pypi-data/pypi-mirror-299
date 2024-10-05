# PYTHON_ARGCOMPLETE_OK
import argparse
import time
import os
import subprocess
import datetime


def parse_args():
    parser = argparse.ArgumentParser(description="Log watcher")
    parser.add_argument(
        "--t-kill",
        type=int,
        help="Number of seconds to wait for logfile output before killing the job",
        default=3600,
    )
    parser.add_argument(
        "--t-warn",
        type=int,
        help="Number of seconds to wait for logfile output before printing warning",
        default=300,
    )
    parser.add_argument(
        "--t-check",
        type=int,
        help="Number of seconds to wait between checking the logfile",
        default=60,
    )
    parser.add_argument(
        "--initial-wait",
        type=int,
        help="Number of seconds to wait before checking the logfile for the first time",
        default=600,
    )
    parser.add_argument("--scancel-bin", type=str, help="Path to scancel binary", default="scancel")
    parser.add_argument("logfile", type=str, help="Path to log file")
    args = parser.parse_args()
    return args


def kill_job(scancel_bin):
    slurm_id = os.environ.get("SLURM_JOB_ID")
    print(f"slurm-watchdog: Killing job {slurm_id} due to inactivity.", flush=True)
    subprocess.run([scancel_bin, slurm_id])


def log_watchdog(msg, also_to_stdout=False):
    with open("watchdog.log", "a") as f:
        # format current time as ISO string and prepend to message
        msg = f"{datetime.datetime.now().isoformat()}: {msg}"
        f.write(msg + "\n")
    if also_to_stdout:
        print(msg, flush=True)


def main():
    args = parse_args()
    time.sleep(args.initial_wait)
    if not os.path.isfile(args.logfile):
        log_watchdog(f"Log file {args.logfile} not found. Aborting job.")
        kill_job(args.scancel_bin)
    last_modified = os.path.getmtime(args.logfile)
    while True:
        time.sleep(args.t_check)
        mtime = os.path.getmtime(args.logfile)
        if mtime > last_modified:
            last_modified = os.path.getmtime(args.logfile)
        else:
            t_since_last_modified = time.time() - last_modified
            if t_since_last_modified > args.t_kill:
                log_watchdog(
                    f"ERROR: No output in last {t_since_last_modified:.0f} seconds to {args.logfile}. Klling job.",
                    also_to_stdout=True,
                )
                kill_job(args.scancel_bin)
                break
            if t_since_last_modified > args.t_warn:
                log_watchdog(f"WARNING: No output in last {t_since_last_modified:.0f} seconds to {args.logfile}.")


if __name__ == "__main__":
    main()
