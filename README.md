# pomodoro-timer

A command-line Pomodoro focus timer with work/break cycles.

Runs work sessions followed by short breaks, with a long break after
a set number of cycles. Durations accept seconds or `25m` / `90s`
style values. Press Ctrl+C to stop early.

## Requirements

- Python 3
- No third-party packages

## How to run

```bash
python3 main.py [--work 25m] [--break 5m] [--long-break 15m] [--cycles 4] [--rounds 1] [--no-break]
```

## Example

```bash
python3 main.py --work 2s --break 1s --cycles 2 --no-break
```

Sample output:

```
Starting Work 1/2 (round 1) — 0m 2s
Work 1/2 (round 1) finished!

Done! Total focus time: 0m 2s
```

## License

MIT — see `LICENSE`.
