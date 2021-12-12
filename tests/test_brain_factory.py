import unittest
from parts.cells.brain_cell_arrays import SENSORS, ACTUATORS, NEURONS
from settings import GeneCellType
from parts.Gene import Gene
from parts.Genome import Genome
from parts.BrainFactory import BrainFactory


class BrianFactoryTest(unittest.TestCase):

    def test_brain_cell_type(self):
        for cell in SENSORS:
            self.assertEqual(GeneCellType.SENSOR, cell.type)
        for cell in ACTUATORS:
            self.assertEqual(GeneCellType.ACTUATOR, cell.type)
        for cell in NEURONS:
            self.assertEqual(GeneCellType.NEURON, cell.type)

    def test_brain_connection(self):
        factory = BrainFactory()

        settings = [[0, 0], [1, 1], 256*255 + 255]
        byte0 = settings[0][0] << 7 | settings[0][1]
        byte1 = settings[1][0] << 7 | settings[1][1]
        byte2 = settings[2] >> 8 & 255
        byte3 = settings[2] & 255
        gene = Gene(bytearray([byte0, byte1, byte2, byte3]))

        parse_array = gene.parse()
        self.assertEqual(GeneCellType.SENSOR, parse_array[0][0])
        self.assertEqual(GeneCellType.NEURON, parse_array[1][0])
        source_cell = factory.cell_from_parse_array(parse_array[0])
        sink_cell = factory.cell_from_parse_array(parse_array[1])
        self.assertEqual(GeneCellType.SENSOR, source_cell.type)
        self.assertEqual(SENSORS[0], source_cell)
        self.assertEqual(GeneCellType.NEURON, sink_cell.type)
        self.assertEqual(NEURONS[1], sink_cell)

        connection = factory.make_connection_from(gene)
        self.assertEqual(GeneCellType.SENSOR, connection.source.type)
        self.assertEqual(SENSORS[0], connection.source)
        self.assertEqual(GeneCellType.NEURON, connection.sink.type)
        self.assertEqual(NEURONS[1], connection.sink)
        self.assertGreaterEqual(4.0, connection.strength)
        self.assertLessEqual(3.999, connection.strength)

    def test_make_simple_connection_list(self):
        # fixed connection strengths for testing
        maximum_strength_raw = 256*255 + 255
        minimum_strength_raw = 0
        middle_strength_raw = 256*128

        # genes for testing
        # 1) sensor0 to nuron0
        settings = [[0, 0], [1, 0], maximum_strength_raw]
        byte0 = settings[0][0] << 7 | settings[0][1]
        byte1 = settings[1][0] << 7 | settings[1][1]
        byte2 = settings[2] >> 8 & 255
        byte3 = settings[2] & 255
        gene1 = Gene(bytearray([byte0, byte1, byte2, byte3]))
        # 2) nuron0 to actuator0
        settings = [[1, 0], [0, 0], minimum_strength_raw]
        byte0 = settings[0][0] << 7 | settings[0][1]
        byte1 = settings[1][0] << 7 | settings[1][1]
        byte2 = settings[2] >> 8 & 255
        byte3 = settings[2] & 255
        gene2 = Gene(bytearray([byte0, byte1, byte2, byte3]))
        # 3) sensor1 to actuator1
        settings = [[0, 1], [0, 1], middle_strength_raw]
        byte0 = settings[0][0] << 7 | settings[0][1]
        byte1 = settings[1][0] << 7 | settings[1][1]
        byte2 = settings[2] >> 8 & 255
        byte3 = settings[2] & 255
        gene3 = Gene(bytearray([byte0, byte1, byte2, byte3]))

        # replace random genes with fixed genes - for testing
        genome = Genome()
        genome.genes = [gene1, gene2, gene3]

        factory = BrainFactory()
        connections = factory.make_connections_from(genome)
        self.assertEqual(3, len(connections))
        connection1 = connections[0]
        self.assertEqual(SENSORS[0], connection1.source)
        self.assertEqual(NEURONS[0], connection1.sink)
        self.assertGreaterEqual(4.0, connection1.strength)
        self.assertLessEqual(3.999, connection1.strength)
        connection2 = connections[1]
        self.assertEqual(NEURONS[0], connection2.source)
        self.assertEqual(ACTUATORS[0], connection2.sink)
        self.assertEqual(-4.0, connection2.strength)
        connection3 = connections[2]
        self.assertEqual(SENSORS[1], connection3.source)
        self.assertEqual(ACTUATORS[1], connection3.sink)
        self.assertEqual(0.0, connection3.strength)

