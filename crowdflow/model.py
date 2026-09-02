from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(slots=True)
class Vec2:
    x: float
    y: float

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vec2":
        return Vec2(self.x * scalar, self.y * scalar)

    def length(self) -> float:
        return math.hypot(self.x, self.y)

    def normalized(self) -> "Vec2":
        length = self.length()
        return Vec2(0.0, 0.0) if length == 0 else Vec2(self.x / length, self.y / length)


@dataclass(slots=True)
class Agent:
    position: Vec2
    target: Vec2
    velocity: Vec2
    speed: float
    group: int = 0


@dataclass(frozen=True, slots=True)
class Wall:
    x1: float
    y1: float
    x2: float
    y2: float

    def contains(self, point: Vec2, padding: float = 0.0) -> bool:
        return (
            self.x1 - padding <= point.x <= self.x2 + padding
            and self.y1 - padding <= point.y <= self.y2 + padding
        )

