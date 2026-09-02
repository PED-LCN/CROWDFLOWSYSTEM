from __future__ import annotations

from dataclasses import dataclass
import random

from .model import Agent, Vec2, Wall


@dataclass(slots=True)
class Scenario:
    name: str
    title: str
    width: float
    height: float
    agents: list[Agent]
    walls: list[Wall]


def _agent(rng: random.Random, x: float, y: float, tx: float, ty: float, group: int = 0) -> Agent:
    return Agent(
        position=Vec2(x, y),
        target=Vec2(tx, ty),
        velocity=Vec2(0.0, 0.0),
        speed=rng.uniform(1.0, 1.45),
        group=group,
    )


def build_scenario(name: str, seed: int = 7) -> Scenario:
    rng = random.Random(seed)
    width, height = 20.0, 12.0
    agents: list[Agent] = []
    walls: list[Wall] = []

    if name == "corridor":
        for _ in range(55):
            agents.append(_agent(rng, rng.uniform(1, 9), rng.uniform(2.0, 10.0), 19.0, rng.uniform(3, 9)))
        title = "Fluxo normal em corredor"
    elif name == "bottleneck":
        walls = [Wall(9.7, 0.0, 10.3, 4.7), Wall(9.7, 7.3, 10.3, 12.0)]
        for _ in range(90):
            agents.append(_agent(rng, rng.uniform(1, 8.7), rng.uniform(0.8, 11.2), 19.0, 6.0))
        title = "Gargalo com passagem estreita"
    elif name == "counterflow":
        for _ in range(45):
            agents.append(_agent(rng, rng.uniform(1, 8), rng.uniform(1, 11), 19.0, rng.uniform(2, 10), 0))
        for _ in range(45):
            agents.append(_agent(rng, rng.uniform(12, 19), rng.uniform(1, 11), 1.0, rng.uniform(2, 10), 1))
        title = "Fluxos em sentidos opostos"
    else:
        raise ValueError(f"Cenário desconhecido: {name}")

    return Scenario(name, title, width, height, agents, walls)


SCENARIOS = ("corridor", "bottleneck", "counterflow")

