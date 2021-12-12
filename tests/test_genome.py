import unittest
from settings import NUMBER_OF_GENES_IN_GENOME
from parts.Genome import Genome


class TestGenome(unittest.TestCase):

    def test_number_of_genes(self):
        genome = Genome()
        self.assertEqual(NUMBER_OF_GENES_IN_GENOME, len(genome.get_genes()))
