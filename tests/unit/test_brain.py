import unittest
from parts.BrainFactory import BrainFactory
from parts.Genome import Genome
from parts.Brain import Brain
from parts.cells.CellCollection import CellCollection


class TestBrain(unittest.TestCase):

    def test_conditions(self):
        potential_cells = CellCollection()
        # minimal conditions for tests
        self.assertGreaterEqual(len(potential_cells.get_sensors()), 3)
        self.assertGreaterEqual(len(potential_cells.get_actuators()), 2)
        self.assertGreaterEqual(len(potential_cells.get_neurons()), 5)

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

    def test_big_brain_raw(self):
        factory = BrainFactory()
        potential_cells = CellCollection()

        # build and minimally test big_brain
        self.build_big_brain(factory, potential_cells)

    def test_brain_marking_code(self):
        factory = BrainFactory()
        potential_cells = CellCollection()
        brain = self.build_big_brain(factory, potential_cells)
        starting_list = brain.actuators
        newly_marked = []
        mark_next = []
        for cell in starting_list:
            if not cell.is_marked():
                cell.set_mark()
                newly_marked.append(cell)
                for connection in cell.connects_from:
                    mark_next.append(connection.source)
        brain.marked_cells += newly_marked
        self.assertEqual(2, len(newly_marked))
        self.assertEqual(2, len(brain.marked_cells))
        self.assertEqual(brain.marked_cells, newly_marked)
        self.assertIn(brain.actuators[0], newly_marked)
        self.assertTrue(brain.actuators[0].is_marked())
        self.assertIn(brain.actuators[1], newly_marked)
        self.assertTrue(brain.actuators[1].is_marked())
        self.assertIn(brain.neurons[0], mark_next)
        self.assertIn(brain.neurons[3], mark_next)
        self.assertIn(brain.neurons[4], mark_next)

        # repeat
        starting_list = mark_next
        newly_marked = []
        mark_next = []
        for cell in starting_list:
            if not cell.is_marked():
                cell.set_mark()
                newly_marked.append(cell)
                for connection in cell.connects_from:
                    mark_next.append(connection.source)
        brain.marked_cells += newly_marked
        self.assertEqual(3, len(newly_marked))
        self.assertEqual(5, len(brain.marked_cells))
        self.assertIn(brain.neurons[0], newly_marked)
        self.assertIn(brain.neurons[3], newly_marked)
        self.assertIn(brain.neurons[4], newly_marked)

    def test_brain_marking_useful_cells(self):
        factory = BrainFactory()
        potential_cells = CellCollection()
        brain = self.build_big_brain(factory, potential_cells)
        brain.mark_used_cells()
        self.assertIn(brain.actuators[0], brain.marked_cells)
        self.assertIn(brain.actuators[1], brain.marked_cells)
        self.assertIn(brain.neurons[0], brain.marked_cells)
        self.assertIn(brain.neurons[3], brain.marked_cells)
        self.assertIn(brain.neurons[4], brain.marked_cells)
        self.assertIn(brain.sensors[0], brain.marked_cells)
        self.assertIn(brain.sensors[1], brain.marked_cells)
        self.assertIn(brain.sensors[2], brain.marked_cells)
        self.assertFalse(brain.neurons[1].is_marked())
        self.assertFalse(brain.neurons[2].is_marked())

    def test_brain_remove_useless_cells_after_marking_code(self):
        factory = BrainFactory()
        potential_cells = CellCollection()
        brain = self.build_big_brain(factory, potential_cells)
        self.assertEqual(12, len(brain.connections))
        self.assertEqual(10, len(brain.all_cells))
        self.assertEqual(3, len(brain.sensors))
        self.assertEqual(2, len(brain.actuators))
        self.assertEqual(5, len(brain.neurons))

        brain.mark_used_cells()
        cells_to_remove = []
        for cell in brain.all_cells:
            if not cell.is_marked():
                cells_to_remove.append(cell)
        self.assertEqual(2, len(cells_to_remove))
        self.assertIn(brain.neurons[1], cells_to_remove)
        self.assertIn(brain.neurons[2], cells_to_remove)
        for cell in cells_to_remove:
            brain.all_cells.remove(cell)
            if cell in brain.sensors:
                brain.sensors.remove(cell)
            if cell in brain.neurons:
                brain.neurons.remove(cell)
            for connection in cell.connects_from:
                if connection in brain.connections:
                    brain.connections.remove(connection)
                if connection in connection.source.connects_to:
                    connection.source.connects_to.remove(connection)
            for connection in cell.connects_to:
                if connection in brain.connections:
                    brain.connections.remove(connection)
                if connection in connection.sink.connects_from:
                    connection.sink.connects_from.remove(connection)
        self.assertEqual(10, len(brain.connections))
        self.assertEqual(8, len(brain.all_cells))
        self.assertEqual(3, len(brain.sensors))
        self.assertEqual(2, len(brain.actuators))
        self.assertEqual(3, len(brain.neurons))

        self.assertEqual(1, len(brain.neurons[0].connects_from))
        self.assertEqual(1, len(brain.neurons[0].connects_to))
        self.assertEqual(brain.sensors[0], brain.neurons[0].connects_from[0].source)
        self.assertEqual(brain.actuators[0], brain.neurons[0].connects_to[0].sink)

        for cell in brain.all_cells:
            self.assertIn(cell, brain.sensors + brain.actuators + brain.neurons)
        for cell in brain.sensors + brain.actuators + brain.neurons:
            self.assertIn(cell, brain.all_cells)

    def test_big_brain_cleaned_by_parts(self):
        factory = BrainFactory()
        potential_cells = CellCollection()
        brain = self.build_big_brain(factory, potential_cells)
        brain.mark_used_cells()
        brain.remove_unmarked_cells()
        brain.reset_marks()
        self.assertEqual(10, len(brain.connections))
        self.assertEqual(8, len(brain.all_cells))
        self.assertEqual(3, len(brain.sensors))
        self.assertEqual(2, len(brain.actuators))
        self.assertEqual(3, len(brain.neurons))

        self.assertEqual(1, len(brain.neurons[0].connects_from))
        self.assertEqual(1, len(brain.neurons[0].connects_to))
        self.assertEqual(brain.sensors[0], brain.neurons[0].connects_from[0].source)
        self.assertEqual(brain.actuators[0], brain.neurons[0].connects_to[0].sink)

        for cell in brain.all_cells:
            self.assertIn(cell, brain.sensors + brain.actuators + brain.neurons)
        for cell in brain.sensors + brain.actuators + brain.neurons:
            self.assertIn(cell, brain.all_cells)

    def test_big_brain_optimized(self):
        factory = BrainFactory()
        potential_cells = CellCollection()
        brain = self.build_big_brain(factory, potential_cells)
        brain.clear_unused_cells()
        self.assertEqual(10, len(brain.connections))
        self.assertEqual(8, len(brain.all_cells))
        self.assertEqual(3, len(brain.sensors))
        self.assertEqual(2, len(brain.actuators))
        self.assertEqual(3, len(brain.neurons))

    def test_clearing_cells_does_not_remove_neuron_without_inputs(self):
        factory = BrainFactory()
        potential_cells = CellCollection()

        # genes for testing
        genes = [
            # nuron0 to actuator0
            factory.make_gene_from_settings_array([[1, 0], [0, 0], 0])]

        # make Genome with fixed genes - for testing
        genome = Genome(genes)

        brain = Brain(genome, potential_cells)
        neuron0 = brain.neurons[0]
        actuator0 = brain.actuators[0]

        self.assertEqual(1, len(brain.connections))
        connection0 = brain.connections[0]
        self.assertEqual(neuron0, connection0.source)
        self.assertEqual(actuator0, connection0.sink)
        brain.clear_unused_cells()

        self.assertEqual(1, len(brain.connections))
        self.assertEqual(connection0, brain.connections[0])

    def build_big_brain(self, factory, potential_cells):
        # build - genome for connections
        genes = [
            # Sensor0 -> Neuron0
            factory.make_gene_from_settings_array([[0, 0], [1, 0], 0]),
            # Neuron0 -> Neuron1
            factory.make_gene_from_settings_array([[1, 0], [1, 1], 0]),
            # Nuron0 -> Actuator0
            factory.make_gene_from_settings_array([[1, 0], [0, 0], 0]),
            # Nuron2 -> Neuron2
            factory.make_gene_from_settings_array([[1, 2], [1, 2], 0]),
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
        self.assertEqual(genome, brain.genome)
        self.assertEqual(10, len(brain.all_cells))
        self.assertEqual(3, len(brain.sensors))
        self.assertEqual(2, len(brain.actuators))
        self.assertEqual(5, len(brain.neurons))

        self.assertEqual(1, len(brain.sensors[0].connects_to))
        self.assertEqual(2, len(brain.sensors[1].connects_to))
        self.assertEqual(2, len(brain.sensors[2].connects_to))

        self.assertEqual(2, len(brain.neurons[0].connects_to))
        self.assertEqual(0, len(brain.neurons[1].connects_to))
        self.assertEqual(1, len(brain.neurons[2].connects_to))
        self.assertEqual(2, len(brain.neurons[3].connects_to))
        self.assertEqual(2, len(brain.neurons[4].connects_to))

        for cell in brain.all_cells:
            for connection in cell.connects_to:
                self.assertEqual(cell, connection.source)
            for connection in cell.connects_from:
                self.assertEqual(cell, connection.sink)

        return brain
