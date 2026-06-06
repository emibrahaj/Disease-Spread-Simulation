from __future__ import annotations

from typing import List, Tuple

import numpy as np

from .config import SimulationConfig
from .population import (
    HEALTHY,
    INFECTED,
    RECOVERED,
    count_states,
    create_initial_population,
    deterministic_chance,
    move_population,
)

NEIGHBOR_OFFSETS = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


def _has_infected_neighbor(state: np.ndarray, row: int, col: int) -> bool:
    max_row, max_col = state.shape
    for row_offset, col_offset in NEIGHBOR_OFFSETS:
        near_row = row + row_offset
        near_col = col + col_offset
        if 0 <= near_row < max_row and 0 <= near_col < max_col:
            if state[near_row, near_col] == INFECTED:
                return True
    return False


def step_sequential(
    state: np.ndarray,
    infection_age: np.ndarray,
    step: int,
    config: SimulationConfig,
    age_groups: np.ndarray | None = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Advance the model by one time step using a single CPU process."""
    next_state = state.copy()
    next_age = infection_age.copy()
    if age_groups is None:
        age_groups = np.ones_like(state, dtype=np.int8)
    infection_probability = config.infection_probability_for_step(step)

    rows, cols = state.shape
    for row in range(rows):
        for col in range(cols):
            if state[row, col] == HEALTHY:
                exposed = _has_infected_neighbor(state, row, col)
                chance = deterministic_chance(row, col, step, config.seed)
                susceptibility = config.susceptibility_for_age_group(int(age_groups[row, col]))
                adjusted_probability = min(1.0, infection_probability * susceptibility)
                if exposed and chance < adjusted_probability:
                    next_state[row, col] = INFECTED
                    next_age[row, col] = 0
            elif state[row, col] == INFECTED:
                next_age[row, col] += 1
                if next_age[row, col] >= config.recovery_days:
                    next_state[row, col] = RECOVERED

    return next_state, next_age


def run_sequential(config: SimulationConfig) -> Tuple[np.ndarray, List[dict[str, int]]]:
    """Run the complete disease simulation sequentially."""
    state, infection_age, age_groups = create_initial_population(config)
    history = [count_states(state)]

    for step in range(config.steps):
        state, infection_age, age_groups = move_population(state, infection_age, age_groups, step, config)
        state, infection_age = step_sequential(state, infection_age, step, config, age_groups)
        history.append(count_states(state))

    return state, history
