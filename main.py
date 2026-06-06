from __future__ import annotations

import argparse
import multiprocessing
from pathlib import Path

from src.config import SimulationConfig
from src.parallel_simulation import run_parallel
from src.performance import compare_modes, write_csv
from src.sequential_simulation import run_sequential
from src.visualization import plot_grid, plot_history


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Parallel disease spread simulation")
    parser.add_argument("--mode", choices=["sequential", "parallel", "compare"], default="parallel")
    parser.add_argument("--grid-size", type=int, default=180)
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--initial-infected", type=int, default=18)
    parser.add_argument("--infection-probability", type=float, default=0.32)
    parser.add_argument("--recovery-days", type=int, default=12)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--processes", type=int, default=max(1, multiprocessing.cpu_count() // 2))
    parser.add_argument("--save-plots", action="store_true")
    return parser


def make_config(args: argparse.Namespace) -> SimulationConfig:
    return SimulationConfig(
        grid_size=args.grid_size,
        steps=args.steps,
        initial_infected=args.initial_infected,
        infection_probability=args.infection_probability,
        recovery_days=args.recovery_days,
        seed=args.seed,
        processes=args.processes,
    )


def print_history_summary(history: list[dict[str, int]]) -> None:
    peak_step, peak = max(enumerate(history), key=lambda item: item[1]["infected"])
    final = history[-1]
    print(f"Peak infected: {peak['infected']} people at step {peak_step}")
    print(
        "Final counts: "
        f"healthy={final['healthy']}, infected={final['infected']}, recovered={final['recovered']}"
    )


def main() -> None:
    args = build_parser().parse_args()
    config = make_config(args)
    config.validate()

    if args.mode == "compare":
        rows = compare_modes(config)
        write_csv(rows, "results/timing_results.csv")
        for row in rows:
            print(row)
        print("Timing results saved to results/timing_results.csv")
        return

    runner = run_parallel if args.mode == "parallel" else run_sequential
    final_state, history = runner(config)
    print(f"Mode: {args.mode}")
    print(f"Grid: {config.grid_size}x{config.grid_size}, steps: {config.steps}")
    print(f"CPU cores available: {multiprocessing.cpu_count()}, processes used: {config.processes}")
    print_history_summary(history)

    if args.save_plots:
        output_dir = Path("results/screenshots/charts")
        plot_history(history, output_dir / f"{args.mode}_history.png")
        plot_grid(final_state, output_dir / f"{args.mode}_final_grid.png")
        print(f"Plots saved in {output_dir}")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
