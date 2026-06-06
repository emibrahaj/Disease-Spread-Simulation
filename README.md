# Disease Spread Simulation

A parallel programming project that simulates disease spread in a city using a grid-based SIR model. Each person is represented by one cell and can be healthy, infected, or recovered.

The project includes both sequential and multiprocessing versions so their results and execution times can be compared.

## Why This Is Parallel Programming

At each simulation step, the grid is split into row chunks. Multiple worker processes update different parts of the population at the same time, then the main process combines the chunks into the next grid state.

This is applied scientific computing: disease models like this are useful for understanding outbreaks and testing how fast infections spread under different parameters.

## Project Structure

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

If you use the included virtual environment:

```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run

Run the parallel simulation and save charts:

```bash
python main.py --mode parallel --save-plots
```

Run the sequential simulation:

```bash
python main.py --mode sequential --save-plots
```

Compare sequential and parallel performance:

```bash
python main.py --mode compare --grid-size 180 --steps 100 --processes 4
```

Run a process-count experiment:

```bash
python experiments/compare_processes.py
```

On Windows, you can also double-click:

```text
run_demo.bat
```

## Test

```bash
pytest
```

or:

```bash
.venv\Scripts\python.exe -m pytest -q
```

## Example Parameters

```bash
python main.py --mode parallel --grid-size 250 --steps 150 --initial-infected 25 --infection-probability 0.28 --recovery-days 14 --processes 4 --save-plots
```

## Output

Generated charts and benchmark CSV files are saved in `results/`.

Useful files for submission:

- Source code: `main.py`, `src/`, `experiments/`, `tests/`
- Printed explanation: `docs/project_explanation.md`
- Presentation outline: `docs/presentation_outline.md`
- Lab progress notes: `docs/progress_checkin.md`
- Results: `results/timing_results.csv` and generated chart images
