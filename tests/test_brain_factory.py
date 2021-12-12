import unittest
from settings import GeneCellType
from parts.Genome import Genome
from parts.BrainFactory import BrainFactory


class BrianFactoryTest(unittest.TestCase):

    def test_brain_cell_type(self):
        factory = BrainFactory()
        for cell in factory.get_library().get_sensors():
            self.assertEqual(GeneCellType.SENSOR, cell.type)
        for cell in factory.get_library().get_actuators():
            self.assertEqual(GeneCellType.ACTUATOR, cell.type)
        for cell in factory.get_library().get_neurons():
            self.assertEqual(GeneCellType.NEURON, cell.type)

    def test_brain_connection(self):
        factory = BrainFactory()
        library = factory.get_library()

        gene = factory.make_gene_from_settings_array([[0, 0], [1, 1], 256*255 + 255])

        parse_array = gene.parse()
        self.assertEqual(GeneCellType.SENSOR, parse_array[0][0])
        self.assertEqual(GeneCellType.NEURON, parse_array[1][0])
        source_cell = factory.cell_from_parse_array(parse_array[0])
        sink_cell = factory.cell_from_parse_array(parse_array[1])
        self.assertEqual(GeneCellType.SENSOR, source_cell.type)
        self.assertEqual(type(library.get_sensors()[0]), type(source_cell))
        self.assertEqual(GeneCellType.NEURON, sink_cell.type)
        self.assertEqual(type(library.get_neurons()[1]), type(sink_cell))

        connection = factory.make_connection_from(gene)
        self.assertEqual(GeneCellType.SENSOR, connection.source.type)
        self.assertEqual(type(library.get_sensors()[0]), type(connection.source))
        self.assertEqual(GeneCellType.NEURON, connection.sink.type)
        self.assertEqual(type(library.get_neurons()[1]), type(connection.sink))
        self.assertGreaterEqual(4.0, connection.strength)
        self.assertLessEqual(3.999, connection.strength)

    def test_make_simple_connection_list(self):
        # fixed connection strengths for testing
        maximum_strength_raw = 256*255 + 255
        minimum_strength_raw = 0
        middle_strength_raw = 256*128

        factory = BrainFactory()
        # genes for testing
        # 1) sensor0 to nuron0
        gene1 = factory.make_gene_from_settings_array(
            [[0, 0], [1, 0], maximum_strength_raw])
        # 2) nuron0 to actuator0
        gene2 = factory.make_gene_from_settings_array(
            [[1, 0], [0, 0], minimum_strength_raw])
        # 3) sensor1 to actuator1
        gene3 = factory.make_gene_from_settings_array(
            [[0, 1], [0, 1], middle_strength_raw])

        # replace random genes with fixed genes - for testing
        genome = Genome()
        genome.genes = [gene1, gene2, gene3]

        library = factory.get_library()
        connections = factory.make_connections_from(genome)
        self.assertEqual(3, len(connections))
        connection1 = connections[0]
        self.assertEqual(library.get_sensors()[0], connection1.source)
        self.assertEqual(library.get_neurons()[0], connection1.sink)
        self.assertGreaterEqual(4.0, connection1.strength)
        self.assertLessEqual(3.999, connection1.strength)
        connection2 = connections[1]
        self.assertEqual(library.get_neurons()[0], connection2.source)
        self.assertEqual(library.get_actuators()[0], connection2.sink)
        self.assertEqual(-4.0, connection2.strength)
        connection3 = connections[2]
        self.assertEqual(library.get_sensors()[1], connection3.source)
        self.assertEqual(library.get_actuators()[1], connection3.sink)
        self.assertEqual(0.0, connection3.strength)
