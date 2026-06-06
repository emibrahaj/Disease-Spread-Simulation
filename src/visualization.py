from __future__ import annotations

from pathlib import Path
from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

from .population import HEALTHY, INFECTED, RECOVERED, VACCINATED


def plot_history(
    history: Sequence[dict[str, int]],
    output_path: str | Path | None = None,
    title: str = "Disease Spread Over Time",
    intervention_step: int | None = None,
) -> None:
    """Plot healthy, infected, and recovered counts over time."""
    steps = range(len(history))
    healthy = [item["healthy"] for item in history]
    infected = [item["infected"] for item in history]
    recovered = [item["recovered"] for item in history]
    vaccinated = [item.get("vaccinated", 0) for item in history]

    plt.figure(figsize=(9, 5))
    plt.plot(steps, healthy, label="Healthy", color="#2f80ed")
    plt.plot(steps, infected, label="Infected", color="#eb5757")
    plt.plot(steps, recovered, label="Recovered", color="#27ae60")
    if any(vaccinated):
        plt.plot(steps, vaccinated, label="Vaccinated", color="#8e44ad")
    plt.xlabel("Simulation step")
    plt.ylabel("People")
    if intervention_step is not None:
        plt.axvline(
            intervention_step,
            color="#333333",
            linestyle="--",
            linewidth=1.2,
            label="Intervention starts",
        )

    plt.title(title)
    plt.legend()
    plt.tight_layout()

    if output_path:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output, dpi=140)
        plt.close()
    else:
        plt.show()


def plot_grid(state: np.ndarray, output_path: str | Path | None = None) -> None:
    """Show the final city grid."""
    cmap = ListedColormap(["#2f80ed", "#eb5757", "#27ae60", "#8e44ad"])
    labels = {
        HEALTHY: "Healthy",
        INFECTED: "Infected",
        RECOVERED: "Recovered",
        VACCINATED: "Vaccinated",
    }

    plt.figure(figsize=(6, 6))
    plt.imshow(state, cmap=cmap, vmin=HEALTHY, vmax=VACCINATED)
    colorbar = plt.colorbar(ticks=list(labels.keys()), fraction=0.046, pad=0.04)
    colorbar.ax.set_yticklabels([labels[key] for key in labels])
    plt.title("Final Population State")
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()

    if output_path:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output, dpi=140)
        plt.close()
    else:
        plt.show()
