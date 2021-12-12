from parts.Gene import Gene
from settings import GeneCellType
from parts.Connection import Connection
from parts.cells.CellCollection import CellCollection


class BrainFactory:

    def __init__(self):
        self.library = CellCollection()

    def get_library(self):
        return self.library

    def make_connection_from(self, gene):
        parse_array = gene.parse()
        source_cell = self.cell_from_parse_array(parse_array[0])
        sink_cell = self.cell_from_parse_array(parse_array[1])
        strength = self.map_raw_strength(parse_array[2])
        return Connection(source_cell, sink_cell, strength)

    def make_connections_from(self, genome):
        connections = []
        for gene in genome.get_genes():
            connections.append(self.make_connection_from(gene))
        return connections

    @staticmethod
    def make_gene_from_settings_array(settings):
        # for example: settings = [[0, 127], [1, 15], 256*255 + 15]
        # source - type 0/1 for SENSOR/NEURON, and raw_index
        # sink - type 0/1 for ACTUATOR/NEURON, and raw_index
        # raw_connection_strength
        # see GeneCellType in settings, parts.Gene, and BrainFactory.cell_from_parse_array
        byte0 = settings[0][0] << 7 | settings[0][1]
        byte1 = settings[1][0] << 7 | settings[1][1]
        byte2 = settings[2] >> 8 & 255
        byte3 = settings[2] & 255
        gene_bytes = bytearray([byte0, byte1, byte2, byte3])
        gene = Gene(gene_bytes)
        return gene

    def cell_from_parse_array(self, cell_parse):
        cell_type = cell_parse[0]
        raw_index = cell_parse[1]
        cell_array = []
        if cell_type is GeneCellType.SENSOR:
            cell_array = self.library.get_sensors()
        elif cell_type is GeneCellType.ACTUATOR:
            cell_array = self.library.get_actuators()
        elif cell_type is GeneCellType.NEURON:
            cell_array = self.library.get_neurons()
        index = raw_index % len(cell_array)
        return cell_array[index]

    @staticmethod
    def map_raw_strength(raw_strength):
        # 256 ** 2 /8 = 8192
        return float(raw_strength)/8192 - 4.0
