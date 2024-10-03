"""Schedule Athan calls."""

import argparse
import sched
import subprocess
import time

# from datetime import datetime, timedelta
from athantime import Athan


def call_athan(scheduler, next_salah, args):
    """Execute athan player.

    Args:
        scheduler (scheduler): sched obj
        next_salah (str): salah name e.g. fajr, dhuhr, asr, maghrib, isha
        args (Namespace): argparse args
    """
    # print("Simulate calling Athan")
    shell_script_path = "/home/pi/sounds/many.sh"
    if next_salah == "fajr":
        shell_script_path = "/home/pi/sounds/fajr.sh"

    try:
        result = subprocess.run(
            shell_script_path,
            capture_output=True,  # Capture stdout and stderr
            text=True,  # Decode output as text
            check=True,  # Raise an exception if the script fails
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")
        print(e.stdout)  # Print stdout if available
        print(e.stderr)  # Print stderr if available
    else:
        print("Script executed successfully.")
        print(result.stdout)  # Print stdout if successful

    sched_athan(scheduler, args)


def sched_athan(sch, args):
    """Recursive function to schedule next athan.

    Args:
        sch (scheduler): sched obj
        args (Namespace): argparse args
    """
    # create Athan object based on user params
    prayer = Athan(
        elev=args.elev,
        lat=args.lat,
        lon=args.lon,
        asr_method=args.asr,
        fajr_angle=args.fajr_angle,
        isha_angle=args.isha_angle,
    )

    # calculate athan times
    m_times = prayer.calc_times()

    # figure out next salah time
    athan_time, next_salah = prayer.get_next_salah(m_times)
    # athan_time = datetime.now() + timedelta(minutes=1)  # testing
    print(f"Next Athan ({next_salah}) will be called @ {athan_time}")

    # Schedule run at desired time
    sch.enterabs(
        time.mktime(athan_time.timetuple()), 1, call_athan, argument=(sch, next_salah, args)
    )  # type: ignore

    # Run the scheduler
    sch.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Schedule Athan Times.")
    parser.add_argument("-e", "--elev", type=float, default=100, help="Elevation in meters")
    parser.add_argument("-l", "--lat", type=float, default=30, help="Latitude in degrees")
    parser.add_argument("-L", "--lon", type=float, default=-120, help="Longitude in degrees")
    parser.add_argument("-a", "--asr", type=int, default=1, help="Asr (1: Jumhoor, 2: Hanafi)")
    parser.add_argument("-f", "--fajr_angle", type=float, default=15, help="Fajr angle in degrees")
    parser.add_argument("-i", "--isha_angle", type=float, default=15, help="Isha angle in degrees")

    args = parser.parse_args()

    # create sched object
    s = sched.scheduler(time.time, time.sleep)

    # schedule athan
    sched_athan(s, args)
