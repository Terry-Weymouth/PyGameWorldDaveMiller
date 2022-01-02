import unittest
from random import randint
from settings import NUMBER_OF_GENES_IN_GENOME
from Thing import Thing
from World import World
from parts.Genome import Genome
from parts.Gene import Gene
from parts.cells.CellCollection import CellCollection


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

    def test_genome_color(self):
        genome = Genome()
        candidates = CellCollection(Thing((0,0), World(1000)))
        color1 = genome.get_color(candidates)

        new_genome = self.create_mutant_genome_single_bit(genome, 3, 0, 0)
        color2 = new_genome.get_color(candidates)
        self.assertEqual(color1[1], color2[1])
        self.assertEqual(color1[2], color2[2])
        dif = color1[0] - color2[0]
        if color2[0] > color1[0]:
            dif = color2[0] - color1[0]
        self.assertLess(dif, 3)

        new_genome = self.create_mutant_genome_single_bit(genome, 3, 1, 0)
        color2 = new_genome.get_color(candidates)
        self.assertEqual(color1[0], color2[0])
        self.assertEqual(color1[2], color2[2])
        dif = color1[1] - color2[1]
        if color2[1] > color1[1]:
            dif = color2[1] - color1[1]
        self.assertLess(dif, 3)

    # copied from Genome - hummm: greater control, I guess; bad idea - code divergence - lazy
    def create_mutant_genome_single_bit(self, genome, gene_index, byte_index, bit_index):
        genes = genome.get_genes()
        new_genes = []
        for i in range(len(genes)):
            new_gene = Gene(genes[i].gene_bytes)
            if i == gene_index:
                new_gene = self.create_mutant_gene_single_bit(genes[i], byte_index, bit_index)
            new_genes.append(new_gene)
        return Genome(new_genes, mutant=True)

    # copied from Gene - hummm: greater control, I guess; bad idea - code divergence - lazy
    @staticmethod
    def create_mutant_gene_single_bit(gene, byte_index, bit_index):
        new_gene_bytes = bytearray(len(gene.gene_bytes))
        for i in range(len(new_gene_bytes)):
            byte = gene.gene_bytes[i]
            if i == byte_index:
                byte ^= 1 << bit_index
            new_gene_bytes[i] = byte
        return Gene(new_gene_bytes)
