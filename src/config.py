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
    intervention_step: int | None = None
    intervention_infection_probability: float | None = None
    vaccination_rate: float = 0.0
    movement_probability: float = 0.0
    use_age_groups: bool = False
    child_fraction: float = 0.25
    senior_fraction: float = 0.15
    child_susceptibility: float = 1.15
    adult_susceptibility: float = 1.0
    senior_susceptibility: float = 1.35

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
        if self.intervention_step is not None and self.intervention_step < 0:
            raise ValueError("intervention_step cannot be negative")
        if self.intervention_infection_probability is not None:
            if not 0 <= self.intervention_infection_probability <= 1:
                raise ValueError("intervention_infection_probability must be between 0 and 1")
        if not 0 <= self.vaccination_rate <= 1:
            raise ValueError("vaccination_rate must be between 0 and 1")
        if not 0 <= self.movement_probability <= 1:
            raise ValueError("movement_probability must be between 0 and 1")
        if not 0 <= self.child_fraction <= 1:
            raise ValueError("child_fraction must be between 0 and 1")
        if not 0 <= self.senior_fraction <= 1:
            raise ValueError("senior_fraction must be between 0 and 1")
        if self.child_fraction + self.senior_fraction > 1:
            raise ValueError("child_fraction plus senior_fraction cannot exceed 1")
        if self.child_susceptibility < 0:
            raise ValueError("child_susceptibility cannot be negative")
        if self.adult_susceptibility < 0:
            raise ValueError("adult_susceptibility cannot be negative")
        if self.senior_susceptibility < 0:
            raise ValueError("senior_susceptibility cannot be negative")

    def infection_probability_for_step(self, step: int) -> float:
        """Return normal or intervention infection probability for the current step."""
        if (
            self.intervention_step is not None
            and self.intervention_infection_probability is not None
            and step >= self.intervention_step
        ):
            return self.intervention_infection_probability
        return self.infection_probability

    def susceptibility_for_age_group(self, age_group: int) -> float:
        """Return infection multiplier for child, adult, or senior groups."""
        if not self.use_age_groups:
            return 1.0
        if age_group == 0:
            return self.child_susceptibility
        if age_group == 2:
            return self.senior_susceptibility
        return self.adult_susceptibility
