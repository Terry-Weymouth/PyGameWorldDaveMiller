import unittest

from parts.cells.CellCollection import CellCollection
from parts.BrainFactory import BrainFactory

from Thing import Thing
from World import World

from parts.Genome import Genome
from parts.Brain import Brain

from goals.GoalSouthEastCorner import GoalSouthEastCorner
from goals.GoalCenter import GoalCenter
from goals.GoalFourCorner import GoalFourCorner


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

    def test_direct_satisfy_center_goal(self):
        world = World(128, 100, False)
        start_pos = (64, 64)
        thing_center = Thing(start_pos, world)
        start_pos = (4, 4)
        thing_outside_center = Thing(start_pos, world)
        goal = GoalCenter(world)
        self.assertTrue(goal.satisfy_goal(thing_center))
        self.assertFalse(goal.satisfy_goal(thing_outside_center))

    def test_direct_satisfy_four_corner_goal(self):
        world = World(128, 100, False)
        size = world.size
        size_half = size / 2
        size_eight = size / 8
        size_minus_eight = size - size_eight
        thing_center = Thing((size_half, size_half), world)
        thing_ne = Thing((size_eight, size_eight), world)
        thing_se = Thing((size_eight, size_minus_eight), world)
        thing_nw = Thing((size_minus_eight, size_eight), world)
        thing_sw = Thing((size_minus_eight, size_minus_eight), world)
        thing_n = Thing((size_half, size_eight), world)
        thing_s = Thing((size_half, size_minus_eight), world)
        thing_e = Thing((size_eight, size_half), world)
        thing_w = Thing((size_minus_eight, size_half), world)
        goal = GoalFourCorner(world)
        self.assertTrue(goal.satisfy_goal(thing_ne))
        self.assertTrue(goal.satisfy_goal(thing_se))
        self.assertTrue(goal.satisfy_goal(thing_nw))
        self.assertTrue(goal.satisfy_goal(thing_sw))
        self.assertFalse(goal.satisfy_goal(thing_center))
        self.assertFalse(goal.satisfy_goal(thing_n))
        self.assertFalse(goal.satisfy_goal(thing_s))
        self.assertFalse(goal.satisfy_goal(thing_e))
        self.assertFalse(goal.satisfy_goal(thing_w))

    def test_brain_satisfy_goal(self):
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
