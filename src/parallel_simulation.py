from __future__ import annotations

from multiprocessing import Pool, cpu_count
from multiprocessing.pool import Pool as PoolType
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
)
from .sequential_simulation import NEIGHBOR_OFFSETS


def _has_infected_neighbor_in_slice(state_slice: np.ndarray, local_row: int, col: int) -> bool:
    max_row, max_col = state_slice.shape
    for row_offset, col_offset in NEIGHBOR_OFFSETS:
        near_row = local_row + row_offset
        near_col = col + col_offset
        if 0 <= near_row < max_row and 0 <= near_col < max_col:
            if state_slice[near_row, near_col] == INFECTED:
                return True
    return False


def _process_rows(
    args: tuple[np.ndarray, np.ndarray, int, int, int, int, SimulationConfig]
) -> tuple[int, np.ndarray, np.ndarray]:
    state_slice, age_slice, slice_start, start_row, end_row, step, config = args
    row_count = end_row - start_row
    target_start = start_row - slice_start
    target_end = target_start + row_count
    next_rows = state_slice[target_start:target_end].copy()
    next_age_rows = age_slice[target_start:target_end].copy()
    infection_probability = config.infection_probability_for_step(step)

    for local_row in range(row_count):
        row = start_row + local_row
        source_row = target_start + local_row
        for col in range(state_slice.shape[1]):
            if state_slice[source_row, col] == HEALTHY:
                exposed = _has_infected_neighbor_in_slice(state_slice, source_row, col)
                chance = deterministic_chance(row, col, step, config.seed)
                if exposed and chance < infection_probability:
                    next_rows[local_row, col] = INFECTED
                    next_age_rows[local_row, col] = 0
            elif state_slice[source_row, col] == INFECTED:
                next_age_rows[local_row, col] += 1
                if next_age_rows[local_row, col] >= config.recovery_days:
                    next_rows[local_row, col] = RECOVERED

    return start_row, next_rows, next_age_rows


def _row_chunks(row_count: int, processes: int) -> list[tuple[int, int]]:
    chunk_count = min(processes, row_count)
    base_size, remainder = divmod(row_count, chunk_count)
    chunks = []
    start = 0
    for index in range(chunk_count):
        size = base_size + (1 if index < remainder else 0)
        end = start + size
        chunks.append((start, end))
        start = end
    return chunks


def step_parallel(
    state: np.ndarray,
    infection_age: np.ndarray,
    step: int,
    config: SimulationConfig,
    pool: PoolType | None = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Advance the model by one step, splitting grid rows across processes."""
    process_count = min(config.processes, cpu_count(), state.shape[0])
    tasks = []
    for start_row, end_row in _row_chunks(state.shape[0], process_count):
        slice_start = max(0, start_row - 1)
        slice_end = min(state.shape[0], end_row + 1)
        tasks.append(
            (
                state[slice_start:slice_end],
                infection_age[slice_start:slice_end],
                slice_start,
                start_row,
                end_row,
                step,
                config,
            )
        )

    if process_count == 1:
        results = [_process_rows(task) for task in tasks]
    elif pool is not None:
        results = pool.map(_process_rows, tasks)
    else:
        with Pool(processes=process_count) as pool:
            results = pool.map(_process_rows, tasks)

    next_state = state.copy()
    next_age = infection_age.copy()
    for start_row, rows, ages in results:
        end_row = start_row + rows.shape[0]
        next_state[start_row:end_row] = rows
        next_age[start_row:end_row] = ages

    return next_state, next_age


def run_parallel(config: SimulationConfig) -> Tuple[np.ndarray, List[dict[str, int]]]:
    """Run the complete disease simulation using multiprocessing."""
    state, infection_age = create_initial_population(config)
    history = [count_states(state)]
    process_count = min(config.processes, cpu_count(), state.shape[0])

    if process_count == 1:
        for step in range(config.steps):
            state, infection_age = step_parallel(state, infection_age, step, config)
            history.append(count_states(state))
    else:
        with Pool(processes=process_count) as pool:
            for step in range(config.steps):
                state, infection_age = step_parallel(state, infection_age, step, config, pool)
                history.append(count_states(state))

    return state, history
