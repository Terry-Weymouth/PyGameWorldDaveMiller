from parts.cells.brain_cell_arrays import SENSORS, ACTUATORS, NEURONS
from settings import GeneCellType
from parts.Connection import Connection
from copy import deepcopy


class BrainFactory:

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
    def cell_from_parse_array(cell_parse):
        cell_type = cell_parse[0]
        raw_index = cell_parse[1]
        cell_array = []
        if cell_type is GeneCellType.SENSOR:
            cell_array = SENSORS
        elif cell_type is GeneCellType.ACTUATOR:
            cell_array = ACTUATORS
        elif cell_type is GeneCellType.NEURON:
            cell_array = NEURONS
        index = raw_index % len(cell_array)
        return deepcopy(cell_array[index])

    @staticmethod
    def map_raw_strength(raw_strength):
        # 256 ** 2 /8 = 8192
        return float(raw_strength)/8192 - 4.0
