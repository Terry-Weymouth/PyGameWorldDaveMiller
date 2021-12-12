from parts.BrainFactory import BrainFactory

factory = BrainFactory()


class Brain:

    def __init__(self, genom):
        self.genom = genom
        self.all_cells = []
        self.sensors = []
        self.actuators = []
        self.neurons = []
        self.connections = factory.make_connections_from(genom)
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
