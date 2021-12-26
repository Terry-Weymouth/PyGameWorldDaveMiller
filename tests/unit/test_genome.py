import unittest
from settings import NUMBER_OF_GENES_IN_GENOME
from parts.Genome import Genome


class TestGenome(unittest.TestCase):

    def test_number_of_genes(self):
        genome = Genome()
        self.assertEqual(NUMBER_OF_GENES_IN_GENOME, len(genome.get_genes()))

    def test_mutate_genome(self):
        genome = Genome()
        new_genome = genome.create_mutant_genome_single_bit()

        self.assertNotEqual(genome, new_genome)
        self.assertEqual(len(genome.get_genes()), len(new_genome.get_genes()))

        dif_count = 0
        for i in range(len(genome.get_genes())):
            bytes1 = genome.get_genes()[i].get_gene_bytes()
            bytes2 = new_genome.get_genes()[i].get_gene_bytes()
            if bytes1 != bytes2:
                dif_count += 1

        self.assertEqual(1, dif_count)