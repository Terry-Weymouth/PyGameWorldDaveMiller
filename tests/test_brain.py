import unittest
from parts.BrainFactory import BrainFactory
from parts.Genome import Genome
from parts.Brain import Brain


class TestBrain(unittest.TestCase):

    def test_conditions(self):
        # minimal conditions for tests
        self.assertGreaterEqual(len(SENSORS),2)
        self.assertGreaterEqual(len(ACTUATORS),2)
        self.assertGreaterEqual(len(NEURONS),3)

    def test_make_initial_connections(self):
        factory = BrainFactory()
        # genes for testing
        genes = [
            # 1) sensor0 to nuron0
            factory.make_gene_from_settings_array([[0, 0], [1, 0], 0]),
            # 2) nuron0 to actuator0
            factory.make_gene_from_settings_array([[1, 0], [0, 0], 0]),
            # 3) sensor1 to actuator1
            factory.make_gene_from_settings_array([[0, 1], [0, 1], 0])]

        # make Genome with fixed genes - for testing
        genome = Genome(genes)

        brain = Brain(genome)
        self.assertEqual(5, len(brain.all_cells))
