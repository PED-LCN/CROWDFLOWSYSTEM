from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .scenarios import SCENARIOS
from .simulation import Simulation


class CrowdFlowApp:
    WIDTH = 1000
    HEIGHT = 600

    def __init__(self, root: tk.Tk, scenario: str = "bottleneck", seed: int = 7):
        self.root = root
        self.root.title("CrowdFlowSystem — MVP 0")
        self.simulation = Simulation(scenario, seed)
        self.paused = False

        controls = ttk.Frame(root, padding=8)
        controls.pack(fill="x")
        ttk.Label(controls, text="Cenário:").pack(side="left")
        self.scenario_var = tk.StringVar(value=scenario)
        ttk.Combobox(controls, textvariable=self.scenario_var, values=SCENARIOS, state="readonly", width=14).pack(side="left", padx=5)
        ttk.Label(controls, text="Semente:").pack(side="left", padx=(10, 0))
        self.seed_var = tk.StringVar(value=str(seed))
        ttk.Entry(controls, textvariable=self.seed_var, width=7).pack(side="left", padx=5)
        self.pause_button = ttk.Button(controls, text="Pausar", command=self.toggle_pause)
        self.pause_button.pack(side="left", padx=5)
        ttk.Button(controls, text="Reiniciar", command=self.reset).pack(side="left")
        self.show_agents = tk.BooleanVar(value=True)
        self.show_vectors = tk.BooleanVar(value=True)
        ttk.Checkbutton(controls, text="Agentes", variable=self.show_agents).pack(side="left", padx=(15, 0))
        ttk.Checkbutton(controls, text="Vetores", variable=self.show_vectors).pack(side="left")
        self.status = ttk.Label(controls, text="")
        self.status.pack(side="right")

        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT, background="#08131f", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.tick()

    def reset(self) -> None:
        try:
            seed = int(self.seed_var.get())
        except ValueError:
            seed = 7
            self.seed_var.set("7")
        self.simulation.reset(self.scenario_var.get(), seed)

    def toggle_pause(self) -> None:
        self.paused = not self.paused
        self.pause_button.configure(text="Continuar" if self.paused else "Pausar")

    @staticmethod
    def density_color(value: float, maximum: float) -> str:
        ratio = min(1.0, value / max(1.0, maximum))
        red = int(30 + 225 * ratio)
        green = int(75 + 70 * (1.0 - ratio))
        blue = int(185 * (1.0 - ratio))
        return f"#{red:02x}{green:02x}{blue:02x}"

    def draw(self) -> None:
        self.canvas.delete("all")
        sim = self.simulation
        field = sim.field
        cw, ch = self.WIDTH / field.columns, self.HEIGHT / field.rows
        peak = field.peak_density

        for row_index, row in enumerate(field.cells):
            for column_index, cell in enumerate(row):
                x1, y1 = column_index * cw, row_index * ch
                self.canvas.create_rectangle(x1, y1, x1 + cw + 1, y1 + ch + 1, fill=self.density_color(cell.density, peak), outline="")
                if self.show_vectors.get() and cell.samples and (abs(cell.velocity_x) + abs(cell.velocity_y)) > 0.1:
                    mx, my = x1 + cw / 2, y1 + ch / 2
                    self.canvas.create_line(mx, my, mx + cell.velocity_x * 7, my + cell.velocity_y * 7, fill="#f5f7fa", arrow="last", width=1)

        sx, sy = self.WIDTH / sim.scenario.width, self.HEIGHT / sim.scenario.height
        for wall in sim.scenario.walls:
            self.canvas.create_rectangle(wall.x1 * sx, wall.y1 * sy, wall.x2 * sx, wall.y2 * sy, fill="#111827", outline="#f8fafc", width=2)

        if self.show_agents.get():
            for agent in sim.scenario.agents:
                x, y = agent.position.x * sx, agent.position.y * sy
                color = "#f8fafc" if agent.group == 0 else "#fbbf24"
                self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color, outline="")

        self.status.configure(text=f"t={sim.time:5.1f}s  agentes={len(sim.scenario.agents)}  pico={peak:.2f}")

    def tick(self) -> None:
        if not self.paused:
            self.simulation.step()
        self.draw()
        self.root.after(50, self.tick)


def run_gui(scenario: str = "bottleneck", seed: int = 7) -> None:
    root = tk.Tk()
    CrowdFlowApp(root, scenario, seed)
    root.mainloop()

