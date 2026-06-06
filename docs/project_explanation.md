# Parallel Disease Spread Simulation

## Project Idea

This project simulates how an infectious disease spreads through a city represented as a 2D grid. Each cell is one person and can be in one of three states:

- Healthy
- Infected
- Recovered

The simulation is a practical example of scientific computing. Similar models are used in epidemiology to study how infections move through a population and how quickly outbreaks grow or disappear.

## Parallel Programming Connection

The project contains two implementations:

- `run_sequential`: updates the whole grid using one process.
- `run_parallel`: splits the grid into row chunks and processes those chunks using Python multiprocessing.

Each worker process calculates the next state for its assigned rows. The main process then combines all updated chunks into the next full grid. This is a good fit for parallelism because most cell updates are independent once the current grid state is known.

## Model Rules

At every step:

1. A healthy person checks the eight neighboring cells around them.
2. If at least one neighbor is infected, the healthy person can become infected.
3. An infected person keeps an infection age counter.
4. When the infection age reaches the configured recovery time, the person becomes recovered.
5. Recovered people stay recovered.

The simulation uses a deterministic seeded chance function. This means the sequential and parallel versions can be compared fairly because they produce the same result for the same configuration.

## Files

- `main.py`: command-line entry point.
- `src/config.py`: simulation settings.
- `src/population.py`: grid creation and state counting.
- `src/sequential_simulation.py`: one-process implementation.
- `src/parallel_simulation.py`: multiprocessing implementation.
- `src/performance.py`: timing and benchmark helpers.
- `src/visualization.py`: charts for the simulation result.
- `experiments/`: small scripts for running experiments.
- `tests/`: correctness tests.
- `results/`: generated timing data and charts.

## How To Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the parallel simulation:

```bash
python main.py --mode parallel --save-plots
```

Compare sequential and parallel timing:

```bash
python main.py --mode compare --grid-size 180 --steps 100 --processes 4
```

Run tests:

```bash
pytest
```

## What Was Implemented

- A grid-based SIR disease model.
- Sequential simulation.
- Parallel simulation using `multiprocessing.Pool`.
- Deterministic infection decisions for fair comparison.
- Benchmarking of sequential vs parallel execution.
- Process-count comparison experiment.
- Result visualization with Matplotlib.
- Automated tests checking correctness.

## Notes About Performance

Parallelism helps most when the grid is large enough. For very small grids, multiprocessing overhead can be larger than the useful work. This is an important real-world parallel programming lesson: parallel programs are not automatically faster, because creating processes and transferring data also has a cost.
