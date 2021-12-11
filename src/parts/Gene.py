from random import getrandbits
from settings import GeneCellType

class Gene:
    BYTE_STRING_LENGTH = 4

    def __init__(self, gene_bytes):
        self.gene_bytes = gene_bytes

    def get_gene_bytes(self):
        return self.gene_bytes

    def copy(self):
        return Gene(bytearray(self.get_gene_bytes()))

    def parse(self):
        source_type_index = self.gene_bytes[0] >> 7
        source_index = self.gene_bytes[0] & 127
        sink_type_index = self.gene_bytes[1] >> 7
        sink_index = self.gene_bytes[1] & 127
        source_type = GeneCellType.source_type_by_index(source_type_index)
        sink_type = GeneCellType.sink_type_by_index(sink_type_index)
        connection_strength = self.gene_bytes[2]*256 + self.gene_bytes[3]
        return [[source_type, source_index], [sink_type, sink_index], connection_strength]

    @staticmethod
    def make_random_gene_bytes():
        ret = bytearray(Gene.BYTE_STRING_LENGTH)
        for i in range(0,len(ret)):
            ret[i] = getrandbits(8)
        return ret
