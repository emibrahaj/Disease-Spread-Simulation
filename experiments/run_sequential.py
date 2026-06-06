import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import SimulationConfig
from src.sequential_simulation import run_sequential
from src.visualization import plot_history


if __name__ == "__main__":
    config = SimulationConfig(grid_size=160, steps=100, initial_infected=12)
    _, history = run_sequential(config)
    plot_history(history, "results/screenshots/charts/sequential_experiment.png")
    print("Sequential experiment finished.")
