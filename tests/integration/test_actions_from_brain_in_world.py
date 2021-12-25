import unittest

from parts.cells.CellCollection import CellCollection
from parts.BrainFactory import BrainFactory

from Thing import Thing
from World import World

from parts.Genome import Genome
from parts.Brain import Brain


class TestActionsFromBrainInWorld(unittest.TestCase):

    def test_conditions(self):
        world = World(1000)
        start_pos = (20, 20)
        thing = Thing(start_pos, world)
        potential_cells = CellCollection(thing)
        # minimal conditions for tests
        self.assertGreaterEqual(len(potential_cells.get_sensors()), 0)
        self.assertGreaterEqual(len(potential_cells.get_actuators()), 4)
        self.assertGreaterEqual(len(potential_cells.get_neurons()), 2)

    def test_brain_move_south_east(self):

        world = World(1000)
        start_pos = (20, 20)
        thing = Thing(start_pos, world)

        factory = BrainFactory()
        potential_cells = CellCollection(thing)

        east = potential_cells.actuators[0]
        south = potential_cells.actuators[3]

        brain = self.get_south_east_brain(factory, potential_cells)
        brain.clear_unused_cells()
        self.assertEqual(4, len(brain.all_cells))
        self.assertEqual(0, len(brain.sensors))
        self.assertEqual(2, len(brain.neurons))
        self.assertEqual(2, len(brain.actuators))
        self.assertEqual(east, brain.actuators[0])
        self.assertEqual(south, brain.actuators[1])
        self.assertEqual(east,brain.connections[0].sink)
        self.assertEqual(south,brain.connections[1].sink)
        thing.brain = brain
        self.assertEqual(start_pos, thing.pos)
        world.things = []
        world.add_thing_to_world(thing)
        self.assertEqual(1, len(world.things))
        self.assertEqual(thing, world.things[0])
        self.assertIsNotNone(world.thing_at(start_pos))
        self.assertEqual(thing, world.thing_at(start_pos))

        for con in brain.connections:
            con.strength = 4.0
        for act in brain.actuators:
            act.value = 0.0
        for n in brain.neurons:
            n.value = 1.0

        world.one_step_all()
        self.assertGreater(brain.actuators[0].value, 0.5)
        self.assertGreater(brain.actuators[1].value, 0.5)
        self.assertIsNone(world.thing_at(start_pos))
        self.assertEqual((21, 19), thing.pos)
        self.assertEqual(thing, world.thing_at(thing.pos))

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
