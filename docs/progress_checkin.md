# Lab Progress Check-In

## Topic

My topic is a disease spread simulation using parallel programming in Python.

## What I Have Done So Far

- I created a 2D grid for the population.
- Each cell can be healthy, infected, or recovered.
- I made a sequential version of the simulation.
- I made a parallel version using multiprocessing.
- I added charts so the result can be seen more clearly.
- I added timing tests to compare one process with multiple processes.
- I added an intervention option that lowers infection probability after a chosen step.
- I added tests to check that the parallel version gives the same result as the sequential version.

## What I Can Show

I can run the simulation with:

```bash
.venv\Scripts\python.exe main.py --mode parallel --save-plots
```

Then I can show the generated charts from:

```text
results\screenshots\charts
```

I can also run:

```bash
.venv\Scripts\python.exe experiments\compare_processes.py
```

This shows how the running time changes with 1, 2, and 4 processes.

I can also show an intervention run:

```bash
.venv\Scripts\python.exe main.py --mode parallel --intervention-step 30 --intervention-probability 0.12 --save-plots
```

The current result from my computer was about:

- 1 process: 3.16 seconds
- 2 processes: 1.84 seconds
- 4 processes: 1.09 seconds

## What Is Still Left

- Make final screenshots for the presentation
- Choose the best results to show
- Prepare the final printed README or PowerPoint
- Maybe add one more experiment with a different infection probability
