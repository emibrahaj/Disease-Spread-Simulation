import multiprocessing
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import SimulationConfig
from src.parallel_simulation import run_parallel
from src.visualization import plot_history


if __name__ == "__main__":
    multiprocessing.freeze_support()
    config = SimulationConfig(grid_size=160, steps=100, initial_infected=12, processes=4)
    _, history = run_parallel(config)
    plot_history(history, "results/screenshots/charts/parallel_experiment.png")
    print("Parallel experiment finished.")
