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

    def test_parse(self):
        settings = [[0, 127], [1, 15], 256*255 + 15]
        factory = BrainFactory()
        gene = factory.make_gene_from_settings_array(settings)
        settings[0][0] = GeneCellType.source_type_by_index(settings[0][0])
        settings[1][0] = GeneCellType.source_type_by_index(settings[1][0])
        parse_list = gene.parse()
        self.assertEqual(settings, parse_list)

    def test_gene_mutate_code(self):
        gene_bytes = bytearray(b'\x01\x02\x03\x04')
        byte_index = 2
        bit_index = 4
        new_gene_bytes = bytearray(len(gene_bytes))
        for i in range(len(new_gene_bytes)):
            byte = gene_bytes[i]
            if i == byte_index:
                byte ^= 1 << bit_index
            new_gene_bytes[i] = byte

        self.assertEqual(gene_bytes[0],new_gene_bytes[0])
        self.assertEqual(gene_bytes[1],new_gene_bytes[1])
        self.assertEqual(gene_bytes[2] + 16,new_gene_bytes[2])
        self.assertEqual(gene_bytes[3],new_gene_bytes[3])

    def test_gene_mutate(self):
        gene_bytes = bytearray(b'\x01\x02\x03\x04')
        gene = Gene(gene_bytes)
        new_gene = gene.create_mutant_gene_single_bit()

        self.assertNotEqual(gene, new_gene)
        self.assertNotEqual(gene.get_gene_bytes(), new_gene.get_gene_bytes())

        dif_count = 0
        dif_index = -1
        for i in range(len(gene_bytes)):
            if not (gene.get_gene_bytes()[i] == new_gene.get_gene_bytes()[i]):
                dif_count += 1
                dif_index = i
        self.assertEqual(1, dif_count)
        self.assertGreater(dif_index, -1)

        byte1 = gene.get_gene_bytes()[dif_index]
        byte2 = new_gene.get_gene_bytes()[dif_index]

        self.assertNotEqual(byte1, byte2)

        dif_count = 0
        for i in range(8):
            bit1 = byte1 & 1
            bit2 = byte2 & 1
            if not (bit1 == bit2):
                dif_count += 1
            byte1 = byte1 >> 1
            byte2 = byte2 >> 1

        self.assertEqual(1, dif_count)
