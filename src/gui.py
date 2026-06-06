from __future__ import annotations

import multiprocessing
import threading
import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import ListedColormap
from matplotlib.figure import Figure

from .config import SimulationConfig
from .parallel_simulation import run_parallel
from .population import HEALTHY, INFECTED, RECOVERED, VACCINATED
from .sequential_simulation import run_sequential


class SimulationApp(ttk.Frame):
    """Tkinter dashboard for running the simulation without terminal flags."""

    def __init__(self, master: tk.Tk) -> None:
        self.colors = {
            "background": "#f4f7fb",
            "panel": "#ffffff",
            "text": "#1f2937",
            "muted": "#64748b",
            "border": "#d8e0ea",
            "accent": "#2563eb",
            "healthy": "#2f80ed",
            "infected": "#eb5757",
            "recovered": "#27ae60",
            "vaccinated": "#8e44ad",
        }
        self._configure_style(master)

        super().__init__(master, padding=18, style="App.TFrame")
        self.master = master
        self.grid(sticky="nsew")
        self.master.title("Disease Spread Simulation")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)

        self.mode = tk.StringVar(value="parallel")
        self.grid_size = tk.IntVar(value=80)
        self.steps = tk.IntVar(value=60)
        self.initial_infected = tk.IntVar(value=8)
        self.infection_probability = tk.DoubleVar(value=0.32)
        self.recovery_days = tk.IntVar(value=12)
        self.processes = tk.IntVar(value=max(1, multiprocessing.cpu_count() // 2))
        self.vaccination_rate = tk.DoubleVar(value=0.0)
        self.movement_probability = tk.DoubleVar(value=0.0)
        self.use_age_groups = tk.BooleanVar(value=False)
        self.status = tk.StringVar(value="Ready")
        self.summary_vars = {
            "healthy": tk.StringVar(value="-"),
            "infected": tk.StringVar(value="-"),
            "recovered": tk.StringVar(value="-"),
            "vaccinated": tk.StringVar(value="-"),
            "peak": tk.StringVar(value="-"),
        }

        self._build_header()
        self._build_controls()
        self._build_summary()
        self._build_chart()

    def _configure_style(self, master: tk.Tk) -> None:
        master.configure(bg=self.colors["background"])
        style = ttk.Style(master)
        style.theme_use("clam")
        style.configure("App.TFrame", background=self.colors["background"])
        style.configure("Panel.TFrame", background=self.colors["panel"], relief="flat")
        style.configure("TLabel", background=self.colors["panel"], foreground=self.colors["text"])
        style.configure("Muted.TLabel", background=self.colors["panel"], foreground=self.colors["muted"])
        style.configure(
            "Title.TLabel",
            background=self.colors["background"],
            foreground=self.colors["text"],
            font=("Segoe UI", 18, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=self.colors["background"],
            foreground=self.colors["muted"],
            font=("Segoe UI", 10),
        )
        style.configure("Section.TLabelframe", background=self.colors["panel"], bordercolor=self.colors["border"])
        style.configure(
            "Section.TLabelframe.Label",
            background=self.colors["panel"],
            foreground=self.colors["text"],
            font=("Segoe UI", 10, "bold"),
        )
        style.configure("TEntry", fieldbackground="#ffffff", bordercolor=self.colors["border"])
        style.configure("TCombobox", fieldbackground="#ffffff", bordercolor=self.colors["border"])
        style.configure(
            "Accent.TButton",
            background=self.colors["accent"],
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=(10, 8),
        )
        style.map("Accent.TButton", background=[("active", "#1d4ed8"), ("disabled", "#93a4bd")])

    def _build_header(self) -> None:
        header = ttk.Frame(self, style="App.TFrame")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 14))
        header.columnconfigure(0, weight=1)

        ttk.Label(header, text="Disease Spread Simulation", style="Title.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            header,
            text="Try vaccination, movement, age groups, and multiprocessing from one window.",
            style="Subtitle.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))

    def _build_controls(self) -> None:
        options = ttk.Frame(self, padding=14, style="Panel.TFrame")
        options.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=(0, 16))
        options.columnconfigure(0, weight=1)
        options.rowconfigure(4, weight=1)

        model_section = ttk.LabelFrame(options, text="Model", padding=10, style="Section.TLabelframe")
        model_section.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        model_section.columnconfigure(1, weight=1)

        ttk.Label(model_section, text="Mode").grid(row=0, column=0, sticky="w", pady=4)
        mode_box = ttk.Combobox(
            model_section,
            textvariable=self.mode,
            values=("parallel", "sequential"),
            state="readonly",
            width=18,
        )
        mode_box.grid(row=0, column=1, sticky="ew", pady=4)

        model_fields = [
            ("Grid size", self.grid_size),
            ("Steps", self.steps),
            ("Initial infected", self.initial_infected),
            ("Infection probability", self.infection_probability),
            ("Recovery days", self.recovery_days),
            ("Processes", self.processes),
        ]

        for index, (label, variable) in enumerate(model_fields, start=1):
            self._add_input(model_section, index, label, variable)

        features = ttk.LabelFrame(options, text="Features", padding=10, style="Section.TLabelframe")
        features.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        features.columnconfigure(1, weight=1)
        self._add_input(features, 0, "Vaccination rate", self.vaccination_rate)
        self._add_input(features, 1, "Movement probability", self.movement_probability)
        ttk.Checkbutton(features, text="Use age groups", variable=self.use_age_groups).grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(8, 2)
        )

        presets = ttk.LabelFrame(options, text="Presets", padding=10, style="Section.TLabelframe")
        presets.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        presets.columnconfigure((0, 1), weight=1)
        ttk.Button(presets, text="Baseline", command=self.apply_baseline).grid(
            row=0, column=0, sticky="ew", padx=(0, 4)
        )
        ttk.Button(presets, text="Prevention", command=self.apply_prevention).grid(
            row=0, column=1, sticky="ew", padx=(4, 0)
        )

        self.run_button = ttk.Button(
            options,
            text="Run simulation",
            command=self.run_simulation,
            style="Accent.TButton",
        )
        self.run_button.grid(row=3, column=0, sticky="ew", pady=(2, 8))

        ttk.Label(options, textvariable=self.status, wraplength=250, style="Muted.TLabel").grid(
            row=4, column=0, sticky="new"
        )

    def _add_input(
        self, parent: ttk.Frame, row: int, label: str, variable: tk.IntVar | tk.DoubleVar
    ) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(parent, textvariable=variable, width=18).grid(row=row, column=1, sticky="ew", pady=4)

    def _build_summary(self) -> None:
        summary = ttk.Frame(self, style="App.TFrame")
        summary.grid(row=1, column=1, sticky="ew", pady=(0, 12))
        summary.rowconfigure(0, minsize=72)
        for col in range(5):
            summary.columnconfigure(col, weight=1)

        cards = [
            ("Healthy", "healthy", self.colors["healthy"]),
            ("Infected", "infected", self.colors["infected"]),
            ("Recovered", "recovered", self.colors["recovered"]),
            ("Vaccinated", "vaccinated", self.colors["vaccinated"]),
            ("Peak", "peak", "#111827"),
        ]
        for col, (label, key, color) in enumerate(cards):
            card = tk.Frame(
                summary,
                bg=self.colors["panel"],
                height=72,
                highlightbackground=self.colors["border"],
                highlightthickness=1,
            )
            card.grid(row=0, column=col, sticky="nsew", padx=(0 if col == 0 else 6, 0))
            card.pack_propagate(False)
            tk.Label(card, text=label, bg=self.colors["panel"], fg=self.colors["muted"], font=("Segoe UI", 9)).pack(
                anchor="w", padx=10, pady=(8, 0)
            )
            tk.Label(
                card,
                textvariable=self.summary_vars[key],
                bg=self.colors["panel"],
                fg=color,
                font=("Segoe UI", 15, "bold"),
            ).pack(anchor="w", padx=10, pady=(0, 8))

    def _build_chart(self) -> None:
        chart_area = ttk.Frame(self, padding=12, style="Panel.TFrame")
        chart_area.grid(row=2, column=1, sticky="nsew")
        chart_area.columnconfigure(0, weight=1)
        chart_area.rowconfigure(0, weight=1)

        self.figure = Figure(figsize=(8, 5), dpi=100, facecolor=self.colors["panel"])
        grid = self.figure.add_gridspec(1, 2, width_ratios=[3, 2])
        self.history_axis = self.figure.add_subplot(grid[0, 0])
        self.grid_axis = self.figure.add_subplot(grid[0, 1])
        self._draw_empty_chart()
        self.canvas = FigureCanvasTkAgg(self.figure, master=chart_area)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def _draw_empty_chart(self) -> None:
        self.history_axis.set_title("Disease Spread Over Time")
        self.history_axis.set_xlabel("Step")
        self.history_axis.set_ylabel("People")
        self.history_axis.grid(True, color="#e5eaf1", linewidth=0.8)
        self.grid_axis.set_title("Final Grid")
        self.grid_axis.set_xticks([])
        self.grid_axis.set_yticks([])
        self.figure.tight_layout()

    def apply_baseline(self) -> None:
        self.vaccination_rate.set(0.0)
        self.movement_probability.set(0.0)
        self.use_age_groups.set(False)
        self.status.set("Baseline preset selected.")

    def apply_prevention(self) -> None:
        self.vaccination_rate.set(0.25)
        self.movement_probability.set(0.04)
        self.use_age_groups.set(True)
        self.status.set("Prevention preset selected.")

    def run_simulation(self) -> None:
        self.run_button.config(state="disabled")
        self.status.set("Running...")
        thread = threading.Thread(target=self._run_worker, daemon=True)
        thread.start()

    def _run_worker(self) -> None:
        try:
            config = SimulationConfig(
                grid_size=self.grid_size.get(),
                steps=self.steps.get(),
                initial_infected=self.initial_infected.get(),
                infection_probability=self.infection_probability.get(),
                recovery_days=self.recovery_days.get(),
                processes=self.processes.get(),
                vaccination_rate=self.vaccination_rate.get(),
                movement_probability=self.movement_probability.get(),
                use_age_groups=self.use_age_groups.get(),
            )
            config.validate()
            runner = run_parallel if self.mode.get() == "parallel" else run_sequential
            final_state, history = runner(config)
        except Exception as exc:  # pragma: no cover - GUI error path
            self.master.after(0, self._show_error, str(exc))
            return

        self.master.after(0, self._show_results, final_state, history)

    def _show_error(self, message: str) -> None:
        self.status.set(f"Error: {message}")
        self.run_button.config(state="normal")

    def _show_results(self, final_state, history: list[dict[str, int]]) -> None:
        steps = range(len(history))
        self.history_axis.clear()
        self.grid_axis.clear()
        self.history_axis.plot(
            steps, [item["healthy"] for item in history], label="Healthy", color=self.colors["healthy"], linewidth=2
        )
        self.history_axis.plot(
            steps, [item["infected"] for item in history], label="Infected", color=self.colors["infected"], linewidth=2
        )
        self.history_axis.plot(
            steps, [item["recovered"] for item in history], label="Recovered", color=self.colors["recovered"], linewidth=2
        )
        vaccinated = [item.get("vaccinated", 0) for item in history]
        if any(vaccinated):
            self.history_axis.plot(
                steps, vaccinated, label="Vaccinated", color=self.colors["vaccinated"], linewidth=2
            )
        self.history_axis.set_title("Disease Spread Over Time")
        self.history_axis.set_xlabel("Step")
        self.history_axis.set_ylabel("People")
        self.history_axis.grid(True, color="#e5eaf1", linewidth=0.8)
        self.history_axis.legend()

        cmap = ListedColormap(
            [
                self.colors["healthy"],
                self.colors["infected"],
                self.colors["recovered"],
                self.colors["vaccinated"],
            ]
        )
        self.grid_axis.imshow(final_state, cmap=cmap, vmin=HEALTHY, vmax=VACCINATED)
        self.grid_axis.set_title("Final Grid")
        self.grid_axis.set_xticks([])
        self.grid_axis.set_yticks([])
        self.figure.tight_layout()
        self.canvas.draw()

        peak_step, peak = max(enumerate(history), key=lambda item: item[1]["infected"])
        final = history[-1]
        self.summary_vars["healthy"].set(str(final["healthy"]))
        self.summary_vars["infected"].set(str(final["infected"]))
        self.summary_vars["recovered"].set(str(final["recovered"]))
        self.summary_vars["vaccinated"].set(str(final.get("vaccinated", 0)))
        self.summary_vars["peak"].set(f"{peak['infected']} at {peak_step}")
        self.status.set(
            f"Peak infected: {peak['infected']} at step {peak_step}. "
            f"Final infected: {final['infected']}."
        )
        self.run_button.config(state="normal")


def launch_gui() -> None:
    root = tk.Tk()
    root.geometry("1160x680")
    root.minsize(980, 600)
    SimulationApp(root)
    root.mainloop()
