from __future__ import annotations

import csv
import time
from pathlib import Path
from typing import Callable

from .config import SimulationConfig
from .parallel_simulation import run_parallel
from .sequential_simulation import run_sequential


def time_run(label: str, runner: Callable[[SimulationConfig], object], config: SimulationConfig) -> dict[str, float | int | str]:
    """Measure one simulation run."""
    started = time.perf_counter()
    runner(config)
    elapsed = time.perf_counter() - started
    return {
        "mode": label,
        "grid_size": config.grid_size,
        "steps": config.steps,
        "processes": config.processes,
        "seconds": round(elapsed, 4),
    }


def compare_modes(config: SimulationConfig) -> list[dict[str, float | int | str]]:
    """Run sequential and parallel versions and report timing plus speedup."""
    sequential_config = SimulationConfig(
        grid_size=config.grid_size,
        steps=config.steps,
        initial_infected=config.initial_infected,
        infection_probability=config.infection_probability,
        recovery_days=config.recovery_days,
        seed=config.seed,
        processes=1,
    )

    sequential = time_run("sequential", run_sequential, sequential_config)
    parallel = time_run("parallel", run_parallel, config)
    speedup = float(sequential["seconds"]) / max(float(parallel["seconds"]), 0.0001)
    parallel["speedup_vs_sequential"] = round(speedup, 3)
    sequential["speedup_vs_sequential"] = 1.0
    return [sequential, parallel]


def benchmark_process_counts(config: SimulationConfig, process_counts: list[int]) -> list[dict[str, float | int | str]]:
    """Measure the parallel implementation with different process counts."""
    rows = []
    for process_count in process_counts:
        process_config = SimulationConfig(
            grid_size=config.grid_size,
            steps=config.steps,
            initial_infected=config.initial_infected,
            infection_probability=config.infection_probability,
            recovery_days=config.recovery_days,
            seed=config.seed,
            processes=process_count,
        )
        rows.append(time_run("parallel", run_parallel, process_config))
    return rows


def write_csv(rows: list[dict[str, float | int | str]], output_path: str | Path) -> None:
    """Save benchmark output for the report."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})

    with output.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
