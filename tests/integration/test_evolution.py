import unittest

from parts.cells.CellCollection import CellCollection
# from parts.BrainFactory import BrainFactory

from Thing import Thing
from World import World

# from parts.Genome import Genome
# from parts.Brain import Brain


class TestEvolution(unittest.TestCase):

    def test_conditions(self):
        world = World(1000)
        start_pos = (20, 20)
        thing = Thing(start_pos, world)
        potential_cells = CellCollection(thing)
        # minimal conditions for tests
        self.assertGreaterEqual(len(potential_cells.get_sensors()), 3)
        self.assertGreaterEqual(len(potential_cells.get_actuators()), 5)
        self.assertGreaterEqual(len(potential_cells.get_neurons()), 6)

    def test_satisfy_goal(self):
        pass
