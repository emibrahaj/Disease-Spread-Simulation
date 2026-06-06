# Lab Progress Check-In

## Topic

Parallel disease spread simulation using Python multiprocessing.

## What Is Working

- The population is represented as a 2D grid.
- Each person can be healthy, infected, or recovered.
- The sequential simulation runs correctly.
- The parallel simulation runs with multiple processes.
- The parallel and sequential versions produce the same result for the same seed.
- Charts and timing CSV files can be generated.
- Automated tests pass.

## What I Can Show In Lab

Run:

```bash
.venv\Scripts\python.exe main.py --mode parallel --save-plots
```

Then show the generated chart images in:

```text
results\screenshots\charts
```

Run:

```bash
.venv\Scripts\python.exe experiments\compare_processes.py
```

Then explain how runtime changes when using 1, 2, and 4 processes.

## What Still Can Be Improved

- Add more experiments with different infection probabilities.
- Add a final PowerPoint using the outline in `docs/presentation_outline.md`.
- Add screenshots of final charts to the printed report.
