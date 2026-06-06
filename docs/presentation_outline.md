# Presentation Notes

## Slide 1: Title

Parallel Disease Spread Simulation

## Slide 2: What My Project Does

My project simulates a disease spreading through a population. The population is shown as a grid, and each cell is one person.

## Slide 3: States In The Simulation

Each person can be:

- healthy
- infected
- recovered

## Slide 4: Basic Rules

- Healthy people can become infected from nearby infected people.
- Infected people recover after some simulation steps.
- Recovered people stay recovered.
- The simulation repeats this for many steps.

## Slide 5: Why It Is Related To Parallel Programming

The grid has many cells, and each step repeats the same type of calculation for every cell. This makes it possible to divide the work between processes.

## Slide 6: Sequential Version

The sequential version updates the whole grid using one process. This is the simpler version and is used as the comparison point.

## Slide 7: Parallel Version

The parallel version splits the grid into row chunks. Each process updates one chunk, and then the main process combines the results.

## Slide 8: Files I Worked On

- `main.py`
- `src/sequential_simulation.py`
- `src/parallel_simulation.py`
- `src/performance.py`
- `src/visualization.py`
- `tests/test_simulation.py`

## Slide 9: Extra Feature

I added an intervention setting. After a selected step, the infection probability becomes lower. This can represent prevention measures like distancing or quarantine.

Example:

```bash
python main.py --mode parallel --intervention-step 30 --intervention-probability 0.12 --save-plots
```

## Slide 10: Results

In the process comparison experiment, using more processes reduced the running time:

- 1 process: about 3.16 seconds
- 2 processes: about 1.84 seconds
- 4 processes: about 1.09 seconds

The output also shows the speedup compared to 1 process.

## Slide 11: What I Learned

- How to split a grid into parts
- How to use multiprocessing in Python
- Why parallel code can have overhead
- Why bigger workloads show better parallel performance

## Slide 12: How I Run It

```bash
.venv\Scripts\python.exe main.py --mode parallel --save-plots
```

or on Windows:

```text
run_demo.bat
```

## Slide 13: Conclusion

This project shows a simple real-world style simulation and compares sequential execution with multiprocessing. It helped me understand that parallelism can improve performance, but only when the workload is large enough.
