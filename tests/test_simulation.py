import numpy as np
import pytest

from src.config import SimulationConfig
from src.parallel_simulation import run_parallel, step_parallel
from src.performance import benchmark_process_counts
from src.population import (
    HEALTHY,
    INFECTED,
    VACCINATED,
    count_states,
    create_initial_population,
    move_population,
)
from src.sequential_simulation import run_sequential, step_sequential


def test_initial_population_has_expected_counts():
    config = SimulationConfig(grid_size=20, initial_infected=5)
    state, infection_age, age_groups = create_initial_population(config)

    counts = count_states(state)

    assert counts["infected"] == 5
    assert counts["healthy"] == 395
    assert counts["recovered"] == 0
    assert counts["vaccinated"] == 0
    assert np.all(infection_age == 0)
    assert age_groups.shape == state.shape


def test_infection_spreads_to_neighbor_when_probability_is_one():
    config = SimulationConfig(
        grid_size=3,
        steps=1,
        initial_infected=1,
        infection_probability=1.0,
        recovery_days=5,
    )
    state = np.full((3, 3), HEALTHY, dtype=np.int8)
    state[1, 1] = INFECTED
    infection_age = np.zeros_like(state, dtype=np.int16)

    next_state, _ = step_sequential(state, infection_age, 0, config)

    assert np.count_nonzero(next_state == INFECTED) == 9


def test_parallel_step_matches_sequential_step():
    config = SimulationConfig(grid_size=15, initial_infected=6, steps=1, processes=2)
    state, infection_age, age_groups = create_initial_population(config)

    sequential_state, sequential_age = step_sequential(state, infection_age, 0, config, age_groups)
    parallel_state, parallel_age = step_parallel(state, infection_age, 0, config, age_groups=age_groups)

    np.testing.assert_array_equal(parallel_state, sequential_state)
    np.testing.assert_array_equal(parallel_age, sequential_age)


def test_parallel_run_matches_sequential_run():
    config = SimulationConfig(grid_size=20, steps=8, initial_infected=5, processes=2)

    sequential_state, sequential_history = run_sequential(config)
    parallel_state, parallel_history = run_parallel(config)

    np.testing.assert_array_equal(parallel_state, sequential_state)
    assert parallel_history == sequential_history


def test_invalid_config_rejected():
    with pytest.raises(ValueError):
        SimulationConfig(grid_size=1).validate()


def test_intervention_changes_infection_probability_after_step():
    config = SimulationConfig(
        infection_probability=0.8,
        intervention_step=5,
        intervention_infection_probability=0.2,
    )

    assert config.infection_probability_for_step(4) == 0.8
    assert config.infection_probability_for_step(5) == 0.2
    assert config.infection_probability_for_step(8) == 0.2


def test_intervention_reduces_spread():
    normal_config = SimulationConfig(grid_size=20, steps=10, initial_infected=5, processes=2)
    intervention_config = SimulationConfig(
        grid_size=20,
        steps=10,
        initial_infected=5,
        processes=2,
        intervention_step=2,
        intervention_infection_probability=0.0,
    )

    _, normal_history = run_parallel(normal_config)
    _, intervention_history = run_parallel(intervention_config)

    assert intervention_history[-1]["infected"] <= normal_history[-1]["infected"]


def test_vaccination_adds_immune_population():
    config = SimulationConfig(grid_size=10, initial_infected=5, vaccination_rate=0.5)

    state, _, _ = create_initial_population(config)
    counts = count_states(state)

    assert counts["infected"] == 5
    assert counts["vaccinated"] == 48
    assert counts["healthy"] == 47


def test_vaccinated_people_do_not_become_infected():
    config = SimulationConfig(grid_size=3, infection_probability=1.0)
    state = np.full((3, 3), HEALTHY, dtype=np.int8)
    state[1, 1] = INFECTED
    state[0, 0] = VACCINATED
    infection_age = np.zeros_like(state, dtype=np.int16)

    next_state, _ = step_sequential(state, infection_age, 0, config)

    assert next_state[0, 0] == VACCINATED


def test_age_groups_change_infection_probability():
    config = SimulationConfig(
        grid_size=3,
        infection_probability=0.5,
        use_age_groups=True,
        child_susceptibility=0.0,
    )
    state = np.full((3, 3), HEALTHY, dtype=np.int8)
    state[1, 1] = INFECTED
    infection_age = np.zeros_like(state, dtype=np.int16)
    age_groups = np.zeros_like(state, dtype=np.int8)

    next_state, _ = step_sequential(state, infection_age, 0, config, age_groups)

    assert np.count_nonzero(next_state == INFECTED) == 1


def test_movement_keeps_state_counts_same():
    config = SimulationConfig(grid_size=8, initial_infected=4, movement_probability=1.0)
    state, infection_age, age_groups = create_initial_population(config)

    moved_state, _, _ = move_population(state, infection_age, age_groups, 0, config)

    assert count_states(moved_state) == count_states(state)


def test_process_benchmark_includes_speedup():
    config = SimulationConfig(grid_size=8, steps=2, initial_infected=2)

    rows = benchmark_process_counts(config, [1])

    assert rows[0]["processes"] == 1
    assert rows[0]["speedup_vs_1_process"] == 1.0
