from __future__ import annotations

from typing import Tuple

import numpy as np

from .config import SimulationConfig

HEALTHY = 0
INFECTED = 1
RECOVERED = 2
VACCINATED = 3

CHILD = 0
ADULT = 1
SENIOR = 2


def create_initial_population(
    config: SimulationConfig,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Create the starting state, infection-age, and age-group grids."""
    config.validate()
    rng = np.random.default_rng(config.seed)
    state = np.full((config.grid_size, config.grid_size), HEALTHY, dtype=np.int8)
    infection_age = np.zeros_like(state, dtype=np.int16)
    age_groups = np.full_like(state, ADULT, dtype=np.int8)

    population_size = config.grid_size * config.grid_size
    infected_cells = rng.choice(population_size, size=config.initial_infected, replace=False)
    rows, cols = np.unravel_index(infected_cells, state.shape)
    state[rows, cols] = INFECTED

    if config.use_age_groups:
        random_values = rng.random(population_size)
        flat_age_groups = age_groups.ravel()
        child_limit = config.child_fraction
        senior_limit = 1 - config.senior_fraction
        flat_age_groups[random_values < child_limit] = CHILD
        flat_age_groups[random_values >= senior_limit] = SENIOR

    if config.vaccination_rate > 0:
        healthy_cells = np.flatnonzero(state.ravel() == HEALTHY)
        vaccinated_count = int(round(healthy_cells.size * config.vaccination_rate))
        if vaccinated_count > 0:
            vaccinated_cells = rng.choice(healthy_cells, size=vaccinated_count, replace=False)
            state.ravel()[vaccinated_cells] = VACCINATED

    return state, infection_age, age_groups


def count_states(state: np.ndarray) -> dict[str, int]:
    """Return healthy, infected, and recovered counts for one simulation step."""
    return {
        "healthy": int(np.count_nonzero(state == HEALTHY)),
        "infected": int(np.count_nonzero(state == INFECTED)),
        "recovered": int(np.count_nonzero(state == RECOVERED)),
        "vaccinated": int(np.count_nonzero(state == VACCINATED)),
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


def move_population(
    state: np.ndarray,
    infection_age: np.ndarray,
    age_groups: np.ndarray,
    step: int,
    config: SimulationConfig,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Move people by deterministic neighboring swaps before an infection step."""
    if config.movement_probability <= 0:
        return state, infection_age, age_groups

    next_state = state.copy()
    next_age = infection_age.copy()
    next_age_groups = age_groups.copy()
    rows, cols = state.shape

    for row in range(rows):
        for col in range(cols):
            chance = deterministic_chance(row, col, step, config.seed + 97)
            if chance >= config.movement_probability:
                continue

            direction = int(deterministic_chance(row, col, step, config.seed + 193) * 4)
            near_row = row
            near_col = col
            if direction == 0:
                near_row -= 1
            elif direction == 1:
                near_row += 1
            elif direction == 2:
                near_col -= 1
            else:
                near_col += 1

            if 0 <= near_row < rows and 0 <= near_col < cols:
                next_state[row, col], next_state[near_row, near_col] = (
                    next_state[near_row, near_col],
                    next_state[row, col],
                )
                next_age[row, col], next_age[near_row, near_col] = (
                    next_age[near_row, near_col],
                    next_age[row, col],
                )
                next_age_groups[row, col], next_age_groups[near_row, near_col] = (
                    next_age_groups[near_row, near_col],
                    next_age_groups[row, col],
                )

    return next_state, next_age, next_age_groups
