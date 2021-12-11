from random import getrandbits


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
        connection_strength = self.gene_bytes[2]*256 + self.gene_bytes[3]
        return (source_type_index, source_index), (sink_type_index, sink_index), connection_strength

    @staticmethod
    def make_random_gene_bytes():
        ret = bytearray(Gene.BYTE_STRING_LENGTH)
        for i in range(0,len(ret)):
            ret[i] = getrandbits(8)
        return ret
