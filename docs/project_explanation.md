# Parallel Disease Spread Simulation

## Project Description

For this project I made a small disease spread simulation. The population is shown as a 2D grid, and each cell in the grid represents one person.

A person can be in one of these states:

- healthy
- infected
- recovered

The idea is similar to a basic SIR model. It is not meant to be a perfect medical model, but it is a good example for showing how a large amount of similar work can be split between processes.

## Why I Chose This Topic

I chose disease spread because it is easy to understand visually, but it also connects to real scientific computing. Simulations like this can be used to test how an infection might move through a population.

It also fits parallel programming because the grid has many cells, and every step needs many repeated calculations.

## Parallel Programming Part

I implemented two versions:

- `run_sequential`, which updates the full grid with one process
- `run_parallel`, which divides the grid into row chunks and uses more than one process

In the parallel version, each process updates only its own group of rows. After that, the main process puts the updated rows back together.

The program uses the same starting seed for both versions, so the sequential and parallel results can be compared fairly.

## Simulation Rules

For every simulation step:

1. A healthy person checks the eight nearby cells.
2. If one of the neighbors is infected, the healthy person may become infected.
3. An infected person keeps an infection age counter.
4. After enough steps, the infected person becomes recovered.
5. Recovered people do not become infected again.

I also added an intervention option. This means that after a chosen step, the infection probability can be reduced. For example, this can represent masks, distancing, or quarantine rules.

## Main Files

- `main.py`: runs the program from the terminal
- `src/config.py`: stores the simulation settings
- `src/population.py`: creates the starting grid and counts people
- `src/sequential_simulation.py`: sequential implementation
- `src/parallel_simulation.py`: parallel multiprocessing implementation
- `src/performance.py`: measures execution time
- `src/visualization.py`: creates charts
- `experiments/`: scripts for testing different runs
- `tests/`: tests for checking that the program works

## How To Run It

Install requirements:

```bash
pip install -r requirements.txt
```

Run the parallel simulation:

```bash
python main.py --mode parallel --save-plots
```

The settings can also be changed from the terminal. For example:

```bash
python main.py --mode parallel --grid-size 250 --steps 150 --initial-infected 25 --save-plots
```

Changing the seed gives a different outbreak pattern:

```bash
python main.py --mode parallel --seed 7 --save-plots
```

Some important parameters are:

- `--grid-size`: how large the population grid is
- `--steps`: how many simulation steps are run
- `--initial-infected`: how many people start infected
- `--infection-probability`: how easily the disease spreads
- `--recovery-days`: how long infection lasts
- `--seed`: controls the repeatable random behavior
- `--processes`: number of worker processes
- `--intervention-step`: when prevention starts
- `--intervention-probability`: lower infection chance after prevention starts

Compare sequential and parallel performance:

```bash
python main.py --mode compare --grid-size 180 --steps 100 --processes 4
```

Run the tests:

```bash
pytest
```

## What I Implemented

- A grid-based disease spread model
- Healthy, infected, and recovered states
- Sequential simulation
- Parallel simulation with `multiprocessing`
- Timing comparison between versions
- Optional intervention step that lowers infection probability
- Charts for the results
- Tests to check that the parallel and sequential versions match

## Performance Notes

The parallel version is useful when the grid is bigger. With very small grids, the program can be slower because starting processes and passing data also takes time.

This was one of the main things I noticed while working on the project: parallel programming is not just about using more processes. The problem must be large enough for the extra work to be worth it.

In one of my process-count tests, the results were approximately:

- 1 process: 3.16 seconds
- 2 processes: 1.84 seconds
- 4 processes: 1.09 seconds

This shows that the parallel version became faster when more processes were used for a larger grid.
