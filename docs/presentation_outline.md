# Presentation Outline

## Slide 1: Title

Parallel Disease Spread Simulation

## Slide 2: Project Goal

The goal is to simulate how a disease spreads through a population and compare a sequential implementation with a parallel multiprocessing implementation.

## Slide 3: Real-World Context

Disease spread simulations are used in scientific computing and epidemiology to understand outbreak behavior, infection peaks, and recovery patterns.

## Slide 4: Model

The city is represented as a 2D grid. Each cell is one person:

- Healthy
- Infected
- Recovered

## Slide 5: Simulation Rules

- Healthy people can become infected if they have an infected neighbor.
- Infected people recover after a fixed number of simulation days.
- Recovered people stay recovered.
- Each step updates the whole population.

## Slide 6: Parallel Programming Approach

The parallel version splits the grid into row chunks. Each process updates one chunk at the same time. After all processes finish, the main process combines the chunks into the next grid.

## Slide 7: Why Parallelism Helps

Each cell update mostly depends on the previous grid state, so many cells can be processed independently. Larger grids create more work, which makes parallel processing more useful.

## Slide 8: Files Implemented

- `main.py`: command-line runner
- `src/sequential_simulation.py`: sequential version
- `src/parallel_simulation.py`: multiprocessing version
- `src/performance.py`: timing tests
- `src/visualization.py`: charts
- `tests/test_simulation.py`: correctness tests

## Slide 9: Results

The process comparison experiment showed that using more processes reduced runtime on the test machine:

- 1 process: about 3.0 seconds
- 2 processes: about 1.7 seconds
- 4 processes: about 1.1 seconds

## Slide 10: What I Learned

- Parallel programs need correct work splitting.
- Process creation and communication add overhead.
- Small simulations may not benefit much from parallelism.
- Larger workloads show clearer speedup.

## Slide 11: How To Run

```bash
.venv\Scripts\python.exe main.py --mode parallel --save-plots
```

or double-click:

```text
run_demo.bat
```

## Slide 12: Conclusion

The project demonstrates a real scientific computing problem and shows how multiprocessing can improve performance when the workload is large enough.
