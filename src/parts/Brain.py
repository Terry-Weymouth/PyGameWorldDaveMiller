from parts.BrainFactory import BrainFactory
from settings import GeneCellType

factory = BrainFactory()


class Brain:

    def __init__(self, genome, cells_for_brain):
        self.candidates = cells_for_brain
        self.genome = genome
        self.all_cells = []
        self.sensors = []
        self.actuators = []
        self.neurons = []
        self.connections = factory.make_connections_from(genome, self.candidates)
        for connection in self.connections:
            source = connection.source
            sink = connection.sink
            self.add_cell(source)
            self.add_cell(sink)
            source.add_connects_to(connection)
            sink.add_connects_from(connection)

    def add_cell(self, cell):
        cell_type = cell.type
        if cell not in self.all_cells:
            self.all_cells.append(cell)
        if cell_type is GeneCellType.SENSOR:
            if cell not in self.sensors:
                self.sensors.append(cell)
        if cell_type is GeneCellType.ACTUATOR:
            if cell not in self.actuators:
                self.actuators.append(cell)
        if cell_type is GeneCellType.NEURON:
            if cell not in self.neurons:
                self.neurons.append(cell)
