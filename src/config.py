from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationConfig:
    """Configuration for the grid-based SIR simulation."""

    grid_size: int = 180
    steps: int = 120
    initial_infected: int = 18
    infection_probability: float = 0.32
    recovery_days: int = 12
    seed: int = 42
    processes: int = 4

    def validate(self) -> None:
        if self.grid_size <= 2:
            raise ValueError("grid_size must be greater than 2")
        if self.steps < 1:
            raise ValueError("steps must be at least 1")
        if self.initial_infected < 1:
            raise ValueError("initial_infected must be at least 1")
        if self.initial_infected > self.grid_size * self.grid_size:
            raise ValueError("initial_infected cannot exceed the population size")
        if not 0 <= self.infection_probability <= 1:
            raise ValueError("infection_probability must be between 0 and 1")
        if self.recovery_days < 1:
            raise ValueError("recovery_days must be at least 1")
        if self.processes < 1:
            raise ValueError("processes must be at least 1")
