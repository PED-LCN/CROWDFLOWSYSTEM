from __future__ import annotations

from dataclasses import dataclass
import math

from .model import Agent


@dataclass(slots=True)
class Cell:
    density: float = 0.0
    velocity_x: float = 0.0
    velocity_y: float = 0.0
    samples: int = 0


class CrowdField:
    def __init__(self, width: float, height: float, columns: int = 40, rows: int = 24):
        self.width = width
        self.height = height
        self.columns = columns
        self.rows = rows
        self.cells = [[Cell() for _ in range(columns)] for _ in range(rows)]

    def update(self, agents: list[Agent]) -> None:
        self.cells = [[Cell() for _ in range(self.columns)] for _ in range(self.rows)]
        sigma = 1.15
        radius = 2

        for agent in agents:
            cx = min(self.columns - 1, max(0, int(agent.position.x / self.width * self.columns)))
            cy = min(self.rows - 1, max(0, int(agent.position.y / self.height * self.rows)))
            center = self.cells[cy][cx]
            center.velocity_x += agent.velocity.x
            center.velocity_y += agent.velocity.y
            center.samples += 1

            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    x, y = cx + dx, cy + dy
                    if 0 <= x < self.columns and 0 <= y < self.rows:
                        weight = math.exp(-(dx * dx + dy * dy) / (2 * sigma * sigma))
                        self.cells[y][x].density += weight

        for row in self.cells:
            for cell in row:
                if cell.samples:
                    cell.velocity_x /= cell.samples
                    cell.velocity_y /= cell.samples

    @property
    def peak_density(self) -> float:
        return max(cell.density for row in self.cells for cell in row)

    @property
    def occupied_cells(self) -> int:
        return sum(cell.density >= 0.25 for row in self.cells for cell in row)

