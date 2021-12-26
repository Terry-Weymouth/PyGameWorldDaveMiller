import unittest
from random import randint

from parts.cells.CellCollection import CellCollection
from parts.BrainFactory import BrainFactory
from goals.GoalSouthEastCorner import GoalSouthEastCorner

from Thing import Thing
from World import World
from parts.Genome import Genome
from parts.Brain import Brain


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

    def test_satisfy_goal_fixed_genome(self):
        world = World(128, 100, False)
        factory = BrainFactory()
        for thing in world.things:
            potential_cells = CellCollection(thing)
            thing.brain = self.get_south_east_brain(factory, potential_cells)
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

    def test_new_brain_pool(self):
        world = World(128, 100, False)
        factory = BrainFactory()
        for thing in world.things:
            potential_cells = CellCollection(thing)
            thing.brain = self.get_south_east_brain(factory, potential_cells)
            thing.brain.clear_unused_cells()
            for con in thing.brain.connections:
                con.strength = 4.0

        goal = GoalSouthEastCorner(world)

        for _ in range(300):
            world.one_step_all()

        result_count = goal.get_count()

        genomes = []
        for thing in world.things:
            if goal.satisfy_goal(thing):
                genomes.append(thing.brain.genome)

        self.assertEqual(result_count, len(genomes))

    def test_new_generation(self):
        generation_size = 100
        world = World(128, generation_size, False)
        for thing in world.things:
            potential_cells = CellCollection(thing)
            thing.brain = Brain(Genome(), potential_cells)  # random bits
            thing.brain.clear_unused_cells()

        goal = GoalSouthEastCorner(world)

        for _ in range(300):
            world.one_step_all()

        genome_list = []
        for thing in world.things:
            if goal.satisfy_goal(thing):
                genome_list.append(thing.brain.genome)

        self.assertGreater(len(genome_list), 0)

        previous_count = len(genome_list)

        world = World(128, generation_size, False)

        for thing in world.things:
            potential_cells = CellCollection(thing)
            genome = self.select_random_from_list(genome_list)
            thing.brain = Brain(genome, potential_cells)
            thing.brain.clear_unused_cells()
            for cell in thing.brain.all_cells:
                cell.value = 0.0

        for _ in range(300):
            world.one_step_all()

        genome_list = []
        for thing in world.things:
            if goal.satisfy_goal(thing):
                genome_list.append(thing.brain.genome)

        self.assertGreater(len(genome_list), previous_count)

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

    @staticmethod
    def select_random_from_list(genome_list):
        random_index = randint(0, len(genome_list) - 1)
        return genome_list[random_index]
