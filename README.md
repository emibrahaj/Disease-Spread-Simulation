# Disease Spread Simulation

This is my parallel programming project. The idea is to simulate a simple disease outbreak in a city. I used a grid, where each square represents one person.

Each person can be:

- healthy
- infected
- recovered

I made two versions of the simulation: one sequential version and one parallel version using Python multiprocessing. The main point of the project is to compare how the program runs when the work is done by one process versus multiple processes.

## How The Simulation Works

The city is stored as a 2D grid. During each step, every person checks the people around them. If a healthy person has an infected neighbor, there is a chance they also become infected. After being infected for a certain number of steps, the person becomes recovered.

The parallel version splits the grid into row sections. Each process works on one section, then the results are joined together for the next step.

## Files

```text
.
|-- main.py
|-- run_demo.bat
|-- src/
|   |-- config.py
|   |-- population.py
|   |-- sequential_simulation.py
|   |-- parallel_simulation.py
|   |-- performance.py
|   `-- visualization.py
|-- experiments/
|   |-- run_sequential.py
|   |-- run_parallel.py
|   `-- compare_processes.py
|-- tests/
|   `-- test_simulation.py
|-- docs/
|   |-- project_explanation.md
|   |-- presentation_outline.md
|   `-- progress_checkin.md
`-- results/
```

## Install

```bash
pip install -r requirements.txt
```

If using the included virtual environment:

```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run The Project

Run the parallel version and save charts:

```bash
python main.py --mode parallel --save-plots
```

Run the sequential version:

```bash
python main.py --mode sequential --save-plots
```

Compare sequential and parallel time:

```bash
python main.py --mode compare --grid-size 180 --steps 100 --processes 4
```

Compare different process counts:

```bash
python experiments/compare_processes.py
```

On Windows, the easiest way is also to double-click:

```text
run_demo.bat
```

## Run Tests

```bash
pytest
```

or:

```bash
.venv\Scripts\python.exe -m pytest -q
```

## Output

The charts and timing files are saved in the `results` folder.

The benchmark commands print a small table in the terminal and also save CSV files, for example:

- `results/timing_results.csv`
- `results/process_comparison.csv`

For submission, the most important files are:

- source code in `main.py`, `src/`, and `experiments/`
- explanation in `docs/project_explanation.md`
- presentation notes in `docs/presentation_outline.md`
- generated results in `results/`
