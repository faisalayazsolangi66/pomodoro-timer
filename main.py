#!/usr/bin/env python3
"""A command-line Pomodoro focus timer with work/break cycles."""
import argparse
import sys
import time
from datetime import datetime


def parse_duration(value):
    """Accept seconds, or '25m' / '90s' style values; returns seconds."""
    value = value.strip().lower()
    try:
        if value.endswith("m"):
            return int(float(value[:-1]) * 60)
        if value.endswith("s"):
            return int(float(value[:-1]))
        return int(float(value))
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"invalid duration: {value!r} (use seconds, e.g. 1500, or 25m)")


def countdown(seconds, label, quiet=False):
    end = time.time() + seconds
    while True:
        remaining = int(end - time.time())
        if remaining < 0:
            break
        mins, secs = divmod(remaining, 60)
        if not quiet:
            print(f"\r{label}: {mins:02d}:{secs:02d} remaining",
                  end="", flush=True)
        time.sleep(1)
    if not quiet:
        print()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {label} finished!")


def main():
    parser = argparse.ArgumentParser(
        description="Pomodoro focus timer with work/break cycles.")
    parser.add_argument("--work", type=parse_duration, default=25 * 60,
                        help="Work session length, seconds or e.g. 25m (default: 25m)")
    parser.add_argument("--break", dest="break_len", type=parse_duration,
                        default=5 * 60,
                        help="Short break length (default: 5m)")
    parser.add_argument("--long-break", type=parse_duration, default=15 * 60,
                        help="Long break length (default: 15m)")
    parser.add_argument("--cycles", type=int, default=4,
                        help="Work sessions before a long break (default: 4)")
    parser.add_argument("--rounds", type=int, default=1,
                        help="How many full sets of cycles to run (default: 1)")
    parser.add_argument("--no-break", action="store_true",
                        help="Run one work session only, no breaks")
    parser.add_argument("--quiet", action="store_true",
                        help="Only print when a session finishes")
    args = parser.parse_args()

    if args.work <= 0 or args.break_len <= 0 or args.cycles < 1 or args.rounds < 1:
        parser.error("work/break must be positive and cycles/rounds >= 1")

    total_work = 0
    try:
        for round_no in range(1, args.rounds + 1):
            for cycle in range(1, args.cycles + 1):
                label = f"Work {cycle}/{args.cycles} (round {round_no})"
                print(f"Starting {label} — {args.work // 60}m {args.work % 60}s")
                countdown(args.work, label, args.quiet)
                total_work += args.work
                if args.no_break:
                    break
                if cycle == args.cycles:
                    print(f"Long break — {args.long_break // 60}m")
                    countdown(args.long_break, "Long break", args.quiet)
                else:
                    print(f"Short break — {args.break_len // 60}m")
                    countdown(args.break_len, "Short break", args.quiet)
            if args.no_break:
                break
    except KeyboardInterrupt:
        print("\nTimer stopped.")
        sys.exit(130)
    print(f"\nDone! Total focus time: {total_work // 60}m {total_work % 60}s")


if __name__ == "__main__":
    main()
