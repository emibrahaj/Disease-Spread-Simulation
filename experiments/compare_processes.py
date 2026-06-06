import multiprocessing
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import SimulationConfig
from src.performance import benchmark_process_counts, print_benchmark_table, write_csv


if __name__ == "__main__":
    multiprocessing.freeze_support()
    config = SimulationConfig(grid_size=180, steps=80, initial_infected=20)
    rows = benchmark_process_counts(config, [1, 2, 4])
    write_csv(rows, "results/process_comparison.csv")
    print_benchmark_table(rows)
    print("Process comparison saved to results/process_comparison.csv")
