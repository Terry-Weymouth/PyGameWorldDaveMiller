import unittest
import math
from parts.cells.CellCollection import CellCollection
from parts.BrainFactory import BrainFactory
from parts.Genome import Genome
from parts.Brain import Brain


class TestNetworkCompute(unittest.TestCase):

    def test_conditions(self):
        potential_cells = CellCollection()
        # minimal conditions for tests
        self.assertGreaterEqual(len(potential_cells.get_sensors()), 3)
        self.assertGreaterEqual(len(potential_cells.get_actuators()), 2)
        self.assertGreaterEqual(len(potential_cells.get_neurons()), 5)

    def test_propagate_code(self):
        factory = BrainFactory()
        potential_cells = CellCollection()

        brain = self.build_new_big_brain(factory, potential_cells)
        brain.clear_unused_cells()

        # for test add weights to all connections
        for connection in brain.connections:
            connection.strength = 4.0

        # Update the network values to determine next actions...
        # 0) clear all sums_of_input
        for cell in brain.all_cells:
            cell.sum_of_inputs = 0.0
        # 1) each each sensor gets its value from the World/Thing
        for sensor in brain.sensors:
            sensor.value = 0.5
        # 2) for each sensor and neuron add its value * connection to sums of connected_to cells
        for cell in brain.sensors + brain.neurons:
            for connection in cell.connects_to:
                connection.sink.sum_of_inputs += connection.strength * cell.value
        self.assertEqual(2.0, brain.neurons[0].sum_of_inputs)
        self.assertEqual(0.0, brain.neurons[1].sum_of_inputs)
        self.assertEqual(4.0, brain.neurons[2].sum_of_inputs)
        self.assertEqual(4.0, brain.neurons[3].sum_of_inputs)
        self.assertEqual(0.0, brain.actuators[0].sum_of_inputs)
        self.assertEqual(0.0, brain.actuators[1].sum_of_inputs)

        # 3) for each neuron and actuator:
        #     if is has connected_from uppdate value from sum_of_inputs
        #     else value = 1.0 (a neuron that supplies a bias via connection weight
        for cell in brain.neurons + brain.actuators:
            if cell.connects_from:
                cell.value = math.tanh(cell.sum_of_inputs)
            else:
                cell.value = 1.0

        self.assertAlmostEqual(0.96, brain.neurons[0].value, 1)
        self.assertAlmostEqual(1.00, brain.neurons[1].value, 1)
        self.assertAlmostEqual(0.99, brain.neurons[2].value, 1)
        self.assertAlmostEqual(0.99, brain.neurons[3].value, 1)

    def test_propagate_method(self):
        factory = BrainFactory()
        potential_cells = CellCollection()

        brain = self.build_new_big_brain(factory, potential_cells)
        brain.clear_unused_cells()

        # for test add weights to all connections
        for connection in brain.connections:
            connection.strength = 4.0

        # simulate sensor input
        for sensor in brain.sensors:
            sensor.value = 0.5

        brain.propagate()
        self.assertEqual(2.0, brain.neurons[0].sum_of_inputs)
        self.assertEqual(0.0, brain.neurons[1].sum_of_inputs)
        self.assertEqual(4.0, brain.neurons[2].sum_of_inputs)
        self.assertEqual(4.0, brain.neurons[3].sum_of_inputs)
        self.assertEqual(0.0, brain.actuators[0].sum_of_inputs)
        self.assertEqual(0.0, brain.actuators[1].sum_of_inputs)
        self.assertAlmostEqual(0.96, brain.neurons[0].value, 1)
        self.assertAlmostEqual(1.00, brain.neurons[1].value, 1)
        self.assertAlmostEqual(0.99, brain.neurons[2].value, 1)
        self.assertAlmostEqual(0.99, brain.neurons[3].value, 1)
        self.assertAlmostEqual(0.0, brain.actuators[0].value, 1)
        self.assertAlmostEqual(0.0, brain.actuators[1].value, 1)

        brain.propagate()
        self.assertEqual(2.0, brain.neurons[0].sum_of_inputs)
        self.assertEqual(0.0, brain.neurons[1].sum_of_inputs)
        self.assertAlmostEqual(7.99, brain.neurons[2].sum_of_inputs, 1)
        self.assertAlmostEqual(7.99, brain.neurons[3].sum_of_inputs, 1)
        self.assertAlmostEqual(7.85, brain.actuators[0].sum_of_inputs, 1)
        self.assertAlmostEqual(7.99, brain.actuators[1].sum_of_inputs, 1)
        self.assertAlmostEqual(0.96, brain.neurons[0].value, 1)
        self.assertAlmostEqual(1.00, brain.neurons[1].value, 1)
        self.assertAlmostEqual(0.99, brain.neurons[2].value, 1)
        self.assertAlmostEqual(0.99, brain.neurons[3].value, 1)
        self.assertAlmostEqual(0.99, brain.actuators[0].value, 1)
        self.assertAlmostEqual(0.99, brain.actuators[1].value, 1)

    @staticmethod
    def build_new_big_brain(factory, potential_cells):
        # build - genome for connections
        genes = [
            # Sensor0 -> Neuron0
            factory.make_gene_from_settings_array([[0, 0], [1, 0], 0]),
            # Neuron0 -> Neuron1
            factory.make_gene_from_settings_array([[1, 0], [1, 1], 0]),
            # Nuron0 -> Actuator0
            factory.make_gene_from_settings_array([[1, 0], [0, 0], 0]),
            # Nuron2 -> Actuator0
            factory.make_gene_from_settings_array([[1, 2], [0, 0], 0]),
            # Sensor1 -> Neuron3
            factory.make_gene_from_settings_array([[0, 1], [1, 3], 0]),
            # Sensor1 -> Neuron4
            factory.make_gene_from_settings_array([[0, 1], [1, 4], 0]),
            # Nuron3 -> Actuator1
            factory.make_gene_from_settings_array([[1, 3], [0, 1], 0]),
            # Nuron4 -> Actuator1
            factory.make_gene_from_settings_array([[1, 4], [0, 1], 0]),
            # Sensor2 -> Neuron3
            factory.make_gene_from_settings_array([[0, 2], [1, 3], 0]),
            # Sensor2 -> Neuron4
            factory.make_gene_from_settings_array([[0, 2], [1, 4], 0]),
            # Nuron3 -> Neuron4
            factory.make_gene_from_settings_array([[1, 3], [1, 4], 0]),
            # Nuron4 -> Neuron3
            factory.make_gene_from_settings_array([[1, 4], [1, 3], 0])
        ]

        # make Genome with fixed genes - for testing
        genome = Genome(genes)
        brain = Brain(genome, potential_cells)
        return brain
