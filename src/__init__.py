"""Disease spread simulation package."""

from .config import SimulationConfig
from .population import HEALTHY, INFECTED, RECOVERED, create_initial_population
from .parallel_simulation import run_parallel
from .sequential_simulation import run_sequential

__all__ = [
    "HEALTHY",
    "INFECTED",
    "RECOVERED",
    "SimulationConfig",
    "create_initial_population",
    "run_parallel",
    "run_sequential",
]
