from __future__ import annotations

from typing import Tuple

import numpy as np

from .config import SimulationConfig

HEALTHY = 0
INFECTED = 1
RECOVERED = 2


def create_initial_population(config: SimulationConfig) -> Tuple[np.ndarray, np.ndarray]:
    """Create the starting state and infection-age grids."""
    config.validate()
    rng = np.random.default_rng(config.seed)
    state = np.full((config.grid_size, config.grid_size), HEALTHY, dtype=np.int8)
    infection_age = np.zeros_like(state, dtype=np.int16)

    population_size = config.grid_size * config.grid_size
    infected_cells = rng.choice(population_size, size=config.initial_infected, replace=False)
    rows, cols = np.unravel_index(infected_cells, state.shape)
    state[rows, cols] = INFECTED

    return state, infection_age


def count_states(state: np.ndarray) -> dict[str, int]:
    """Return healthy, infected, and recovered counts for one simulation step."""
    return {
        "healthy": int(np.count_nonzero(state == HEALTHY)),
        "infected": int(np.count_nonzero(state == INFECTED)),
        "recovered": int(np.count_nonzero(state == RECOVERED)),
    }


def deterministic_chance(row: int, col: int, step: int, seed: int) -> float:
    """Fast deterministic pseudo-random value in [0, 1) for a cell and step."""
    value = (
        (row + 1) * 73856093
        ^ (col + 1) * 19349663
        ^ (step + 1) * 83492791
        ^ (seed + 1) * 2654435761
    ) & 0xFFFFFFFF
    return value / 0x100000000
