import unittest

from crowdflow.field import CrowdField
from crowdflow.scenarios import SCENARIOS, build_scenario
from crowdflow.simulation import Simulation


class MVP0Tests(unittest.TestCase):
    def test_all_scenarios_are_reproducible(self):
        for name in SCENARIOS:
            first = build_scenario(name, seed=13)
            second = build_scenario(name, seed=13)
            self.assertEqual(first.agents[0].position, second.agents[0].position)
            self.assertEqual(len(first.agents), len(second.agents))

    def test_field_detects_occupancy(self):
        scenario = build_scenario("corridor", seed=1)
        field = CrowdField(scenario.width, scenario.height)
        field.update(scenario.agents)
        self.assertGreater(field.peak_density, 0)
        self.assertGreater(field.occupied_cells, 0)

    def test_simulation_advances_and_stays_in_bounds(self):
        simulation = Simulation("bottleneck", seed=5)
        for _ in range(50):
            simulation.step()
        self.assertGreater(simulation.time, 0)
        for agent in simulation.scenario.agents:
            self.assertGreaterEqual(agent.position.x, 0)
            self.assertLessEqual(agent.position.x, simulation.scenario.width)
            self.assertGreaterEqual(agent.position.y, 0)
            self.assertLessEqual(agent.position.y, simulation.scenario.height)


if __name__ == "__main__":
    unittest.main()
