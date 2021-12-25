import unittest

from parts.cells.CellCollection import CellCollection
from parts.BrainFactory import BrainFactory

from Thing import Thing
from World import World

from parts.Genome import Genome
from parts.Brain import Brain

from goals.GoalSouthEastCorner import GoalSouthEastCorner


class TestGoal(unittest.TestCase):

    def test_conditions(self):
        world = World(1000, 100, False)
        start_pos = (20, 20)
        thing = Thing(start_pos, world)
        potential_cells = CellCollection(thing)
        # minimal conditions for tests
        self.assertGreaterEqual(len(potential_cells.get_sensors()), 3)
        self.assertGreaterEqual(len(potential_cells.get_actuators()), 5)
        self.assertGreaterEqual(len(potential_cells.get_neurons()), 6)

    def test_satisfy_goal(self):
        world = World(128, 100, False)
        factory = BrainFactory()
        for thing in world.things:
            potential_cells = CellCollection(thing)
            thing.brain = self.get_south_east_brain(factory,potential_cells)
            thing.brain.clear_unused_cells()
            for con in thing.brain.connections:
                con.strength = 4.0

        goal = GoalSouthEastCorner(world)

        start_count = 0
        for thing in world.things:
            if goal.satisfy_goal(thing):
                start_count += 1

        self.assertLess(start_count, 50)

        for _ in range(300):
            world.one_step_all()

        self.assertGreater(goal.get_count(), start_count + 30)

    @staticmethod
    def get_south_east_brain(factory, potential_cells):
        # build - genome for connections
        genes = [
            # Nuron0 -> Actuator0
            factory.make_gene_from_settings_array([[1, 0], [0, 0], 0]),
            # Nuron1 -> Actuator3
            factory.make_gene_from_settings_array([[1, 1], [0, 3], 0])
        ]

        # make Genome with fixed genes - for testing
        genome = Genome(genes)
        brain = Brain(genome, potential_cells)
        return brain
