from __future__ import annotations

import argparse
import json

from .scenarios import SCENARIOS
from .simulation import Simulation


def main() -> None:
    parser = argparse.ArgumentParser(description="CrowdFlowSystem MVP 0")
    parser.add_argument("--scenario", choices=SCENARIOS, default="bottleneck")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--headless", action="store_true", help="Executa sem interface gráfica")
    parser.add_argument("--steps", type=int, default=600)
    args = parser.parse_args()

    if args.headless:
        simulation = Simulation(args.scenario, args.seed)
        for _ in range(args.steps):
            simulation.step()
        print(json.dumps(simulation.summary(), indent=2, ensure_ascii=False))
    else:
        from .gui import run_gui

        run_gui(args.scenario, args.seed)


if __name__ == "__main__":
    main()

