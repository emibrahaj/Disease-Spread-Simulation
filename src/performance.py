from __future__ import annotations

import csv
import time
from pathlib import Path
from typing import Callable

from .config import SimulationConfig
from .parallel_simulation import run_parallel
from .sequential_simulation import run_sequential


BenchmarkRow = dict[str, float | int | str]


def time_run(label: str, runner: Callable[[SimulationConfig], object], config: SimulationConfig) -> BenchmarkRow:
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


def compare_modes(config: SimulationConfig) -> list[BenchmarkRow]:
    """Run sequential and parallel versions and report timing plus speedup."""
    sequential_config = SimulationConfig(
        grid_size=config.grid_size,
        steps=config.steps,
        initial_infected=config.initial_infected,
        infection_probability=config.infection_probability,
        recovery_days=config.recovery_days,
        seed=config.seed,
        processes=1,
        intervention_step=config.intervention_step,
        intervention_infection_probability=config.intervention_infection_probability,
    )

    sequential = time_run("sequential", run_sequential, sequential_config)
    parallel = time_run("parallel", run_parallel, config)
    speedup = float(sequential["seconds"]) / max(float(parallel["seconds"]), 0.0001)
    parallel["speedup_vs_sequential"] = round(speedup, 3)
    sequential["speedup_vs_sequential"] = 1.0
    return [sequential, parallel]


def benchmark_process_counts(config: SimulationConfig, process_counts: list[int]) -> list[BenchmarkRow]:
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
            intervention_step=config.intervention_step,
            intervention_infection_probability=config.intervention_infection_probability,
        )
        rows.append(time_run("parallel", run_parallel, process_config))

    baseline_seconds = float(rows[0]["seconds"]) if rows else 0.0
    for row in rows:
        seconds = max(float(row["seconds"]), 0.0001)
        row["speedup_vs_1_process"] = round(baseline_seconds / seconds, 3)
    return rows


def write_csv(rows: list[BenchmarkRow], output_path: str | Path) -> None:
    """Save benchmark output for the report."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})

    with output.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def print_benchmark_table(rows: list[BenchmarkRow]) -> None:
    """Print benchmark rows in a simple readable table."""
    if not rows:
        print("No benchmark rows to show.")
        return

    fieldnames = sorted({key for row in rows for key in row})
    widths = {
        field: max(len(field), *(len(str(row.get(field, ""))) for row in rows))
        for field in fieldnames
    }
    header = "  ".join(field.ljust(widths[field]) for field in fieldnames)
    print(header)
    print("-" * len(header))
    for row in rows:
        print("  ".join(str(row.get(field, "")).ljust(widths[field]) for field in fieldnames))
