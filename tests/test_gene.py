import unittest
from parts.Gene import Gene
from settings import GeneCellType
from parts.BrainFactory import BrainFactory


class TestGene(unittest.TestCase):

    def test_base_byte_length(self):  # note, these test only work for length of 4
        self.assertEqual(4, Gene.BYTE_STRING_LENGTH)

    def test_new_fixed(self):
        gene_bytes = bytearray(b'\x01\x02\x03\x04\x05\x06\x07\x08')
        gene = Gene(gene_bytes)
        self.assertEqual(gene_bytes, gene.get_gene_bytes())

    def test_new_random(self):
        gene_bytes = Gene.make_random_gene_bytes()
        gene = Gene(gene_bytes)
        self.assertEqual(gene_bytes, gene.get_gene_bytes())

    def test_copy(self):
        gene_bytes = bytearray(b'\x01\x02\x03\x04\x05\x06\x07\x08')
        gene = Gene(gene_bytes)
        gene_copy = gene.copy()
        self.assertEqual(gene.get_gene_bytes(), gene_copy.get_gene_bytes())
        gene_copy.get_gene_bytes()[0] = 255
        self.assertNotEqual(gene.get_gene_bytes(), gene_copy.get_gene_bytes())

    def test_parse(self):
        settings = [[0, 127], [1, 15], 256*255 + 15]
        factory = BrainFactory()
        gene = factory.make_gene_from_settings_array(settings)
        settings[0][0] = GeneCellType.source_type_by_index(settings[0][0])
        settings[1][0] = GeneCellType.source_type_by_index(settings[1][0])
        parse_list = gene.parse()
        self.assertEqual(settings, parse_list)
