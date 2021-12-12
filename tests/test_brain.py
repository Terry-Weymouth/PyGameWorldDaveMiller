import unittest
from parts.BrainFactory import BrainFactory
from parts.Genome import Genome
from parts.Brain import Brain
from parts.cells.CellCollection import CellCollection


class TestBrain(unittest.TestCase):

    def test_conditions(self):
        potential_cells = CellCollection()
        # minimal conditions for tests
        self.assertGreaterEqual(len(potential_cells.get_sensors()), 2)
        self.assertGreaterEqual(len(potential_cells.get_actuators()), 2)
        self.assertGreaterEqual(len(potential_cells.get_neurons()), 3)

    def test_brain_connections(self):
        factory = BrainFactory()
        potential_cells = CellCollection()
        # genes for testing
        genes = [
            # 1) sensor0 to nuron0
            factory.make_gene_from_settings_array([[0, 0], [1, 0], 0]),
            # 2) nuron0 to actuator0
            factory.make_gene_from_settings_array([[1, 0], [0, 0], 0]),
            # 3) sensor1 to actuator1
            factory.make_gene_from_settings_array([[0, 1], [0, 1], 0])]

        # make Genome with fixed genes - for testing
        genome = Genome(genes)
        self.assertEqual(genes, genome.get_genes())

        connections = factory.make_connections_from(genome, potential_cells)
        self.assertEqual(3, len(connections))
        connection1 = connections[0]
        self.assertEqual(potential_cells.get_sensors()[0], connection1.source)
        self.assertEqual(potential_cells.get_neurons()[0], connection1.sink)
        self.assertEqual(-4.0, connection1.strength)
        connection2 = connections[1]
        self.assertEqual(potential_cells.get_neurons()[0], connection2.source)
        self.assertEqual(potential_cells.get_actuators()[0], connection2.sink)
        self.assertEqual(-4.0, connection2.strength)
        connection3 = connections[2]
        self.assertEqual(potential_cells.get_sensors()[1], connection3.source)
        self.assertEqual(potential_cells.get_actuators()[1], connection3.sink)
        self.assertEqual(-4.0, connection3.strength)

    def test_make_simple_connections(self):
        factory = BrainFactory()
        potential_cells = CellCollection()

        # genes for testing
        genes = [
            # 1) sensor0 to nuron0
            factory.make_gene_from_settings_array([[0, 0], [1, 0], 0]),
            # 2) nuron0 to actuator0
            factory.make_gene_from_settings_array([[1, 0], [0, 0], 0]),
            # 3) sensor1 to actuator1
            factory.make_gene_from_settings_array([[0, 1], [0, 1], 0])]

        # make Genome with fixed genes - for testing
        genome = Genome(genes)

        brain = Brain(genome, potential_cells)
        self.assertEqual(genome, brain.genome)
        self.assertEqual(5, len(brain.all_cells))
        self.assertEqual(2, len(brain.sensors))
        self.assertEqual(2, len(brain.actuators))
        self.assertEqual(1, len(brain.neurons))

        for cell in brain.sensors:
            self.assertIn(cell, potential_cells.get_sensors())
        for cell in brain.actuators:
            self.assertIn(cell, potential_cells.get_actuators())
        for cell in brain.neurons:
            self.assertIn(cell, potential_cells.get_neurons())

        connections = brain.connections
        self.assertEqual(3, len(connections))
        connection1 = connections[0]
        self.assertEqual(potential_cells.get_sensors()[0], connection1.source)
        self.assertEqual(potential_cells.get_neurons()[0], connection1.sink)
        self.assertEqual(-4.0, connection1.strength)
        connection2 = connections[1]
        self.assertEqual(potential_cells.get_neurons()[0], connection2.source)
        self.assertEqual(potential_cells.get_actuators()[0], connection2.sink)
        self.assertEqual(-4.0, connection2.strength)
        connection3 = connections[2]
        self.assertEqual(potential_cells.get_sensors()[1], connection3.source)
        self.assertEqual(potential_cells.get_actuators()[1], connection3.sink)
        self.assertEqual(-4.0, connection3.strength)

        for cell in brain.all_cells:
            for connection in cell.connects_to:
                self.assertEqual(cell, connection.source)
            for connection in cell.connects_from:
                self.assertEqual(cell, connection.sink)

        sensor0 = potential_cells.get_sensors()[0]
        neuron0 = potential_cells.get_neurons()[0]
        actuator0 = potential_cells.get_actuators()[0]

        self.assertEqual(sensor0, brain.sensors[0])
        self.assertEqual(neuron0, brain.neurons[0])
        self.assertEqual(actuator0, brain.actuators[0])

        self.assertEqual(0, len(sensor0.connects_from))
        self.assertEqual(1, len(sensor0.connects_to))
        self.assertEqual(sensor0, sensor0.connects_to[0].source)
        self.assertEqual(neuron0, sensor0.connects_to[0].sink)

        self.assertEqual(1, len(neuron0.connects_from))
        self.assertEqual(1, len(neuron0.connects_to))
        self.assertEqual(sensor0, neuron0.connects_from[0].source)
        self.assertEqual(neuron0, neuron0.connects_from[0].sink)
        self.assertEqual(neuron0, neuron0.connects_to[0].source)
        self.assertEqual(actuator0, neuron0.connects_to[0].sink)

        self.assertEqual(1, len(actuator0.connects_from))
        self.assertEqual(0, len(actuator0.connects_to))
        self.assertEqual(neuron0, actuator0.connects_from[0].source)
        self.assertEqual(actuator0, actuator0.connects_from[0].sink)

        self.assertEqual(sensor0.connects_to[0], neuron0.connects_from[0])
        self.assertEqual(neuron0.connects_to[0], actuator0.connects_from[0])

        sensor1 = potential_cells.get_sensors()[1]
        actuator1 = potential_cells.get_actuators()[1]

        self.assertEqual(sensor1, brain.sensors[1])
        self.assertEqual(actuator1, brain.actuators[1])

        self.assertEqual(0, len(sensor1.connects_from))
        self.assertEqual(1, len(sensor1.connects_to))
        self.assertEqual(sensor1, sensor1.connects_to[0].source)
        self.assertEqual(actuator1, sensor1.connects_to[0].sink)

        self.assertEqual(1, len(actuator1.connects_from))
        self.assertEqual(0, len(actuator1.connects_to))
        self.assertEqual(sensor1, actuator1.connects_from[0].source)
        self.assertEqual(actuator1, actuator1.connects_from[0].sink)

        self.assertEqual(sensor1.connects_to[0], actuator1.connects_from[0])
