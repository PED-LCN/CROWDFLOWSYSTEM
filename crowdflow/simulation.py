from __future__ import annotations

import math

from .field import CrowdField
from .model import Agent, Vec2
from .scenarios import Scenario, build_scenario


class Simulation:
    def __init__(self, scenario_name: str = "bottleneck", seed: int = 7):
        self.scenario_name = scenario_name
        self.seed = seed
        self.time = 0.0
        self.scenario: Scenario = build_scenario(scenario_name, seed)
        self.field = CrowdField(self.scenario.width, self.scenario.height)
        self.field.update(self.scenario.agents)

    def reset(self, scenario_name: str | None = None, seed: int | None = None) -> None:
        self.__init__(scenario_name or self.scenario_name, self.seed if seed is None else seed)

    def step(self, dt: float = 0.05) -> None:
        agents = self.scenario.agents
        proposed: list[tuple[Agent, Vec2, Vec2]] = []

        for agent in agents:
            desired = (agent.target - agent.position).normalized()
            separation = Vec2(0.0, 0.0)
            for other in agents:
                if other is agent:
                    continue
                delta = agent.position - other.position
                distance = delta.length()
                if 0 < distance < 0.55:
                    separation = separation + delta.normalized() * ((0.55 - distance) / 0.55)

            direction = (desired + separation * 0.8).normalized()
            velocity = direction * agent.speed
            candidate = agent.position + velocity * dt

            if any(wall.contains(candidate, padding=0.12) for wall in self.scenario.walls):
                alternatives = [
                    Vec2(agent.position.x, agent.position.y + math.copysign(agent.speed * dt, 6.0 - agent.position.y)),
                    Vec2(agent.position.x, agent.position.y - math.copysign(agent.speed * dt, 6.0 - agent.position.y)),
                ]
                valid = next((p for p in alternatives if not any(w.contains(p, 0.12) for w in self.scenario.walls)), agent.position)
                velocity = Vec2((valid.x - agent.position.x) / dt, (valid.y - agent.position.y) / dt)
                candidate = valid

            candidate.x = min(self.scenario.width, max(0.0, candidate.x))
            candidate.y = min(self.scenario.height, max(0.0, candidate.y))
            proposed.append((agent, candidate, velocity))

        for agent, position, velocity in proposed:
            agent.position = position
            agent.velocity = velocity

        self.time += dt
        self.field.update(agents)

    def summary(self) -> dict[str, float | int | str]:
        return {
            "scenario": self.scenario_name,
            "seed": self.seed,
            "time_seconds": round(self.time, 3),
            "agents": len(self.scenario.agents),
            "peak_density": round(self.field.peak_density, 3),
            "occupied_cells": self.field.occupied_cells,
        }

