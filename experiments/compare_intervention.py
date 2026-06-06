import multiprocessing
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import SimulationConfig
from src.parallel_simulation import run_parallel
from src.visualization import plot_history


def peak_infected(history: list[dict[str, int]]) -> int:
    return max(step["infected"] for step in history)


if __name__ == "__main__":
    multiprocessing.freeze_support()

    normal_config = SimulationConfig(grid_size=160, steps=100, initial_infected=12, processes=4)
    intervention_config = SimulationConfig(
        grid_size=160,
        steps=100,
        initial_infected=12,
        processes=4,
        intervention_step=30,
        intervention_infection_probability=0.12,
    )

    _, normal_history = run_parallel(normal_config)
    _, intervention_history = run_parallel(intervention_config)

    plot_history(
        normal_history,
        "results/screenshots/charts/no_intervention_history.png",
        title="Disease Spread Without Intervention",
    )
    plot_history(
        intervention_history,
        "results/screenshots/charts/intervention_history.png",
        title="Disease Spread With Intervention",
        intervention_step=intervention_config.intervention_step,
    )

    print(f"Peak infected without intervention: {peak_infected(normal_history)}")
    print(f"Peak infected with intervention: {peak_infected(intervention_history)}")
    print("Charts saved in results/screenshots/charts")
