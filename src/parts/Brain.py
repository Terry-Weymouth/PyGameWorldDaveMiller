import math
from parts.BrainFactory import BrainFactory
from settings import GeneCellType

factory = BrainFactory()


class Brain:

    def __init__(self, genome, cells_for_self):
        self.candidates = cells_for_self
        self.genome = genome
        self.all_cells = []
        self.sensors = []
        self.actuators = []
        self.neurons = []
        self.marked_cells = []
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

    def mark_used_cells(self):
        self.marked_cells = []
        self.mark_all_from_connects_from(self.actuators)

    def mark_all_from_connects_from(self, starting_list):
        # starting from starting - mark unmarked on these
        # then recurse with connects_to of newly marked
        if not starting_list:
            return
        newly_marked = []
        mark_next = []
        for cell in starting_list:
            if not cell.is_marked():
                cell.set_mark()
                newly_marked.append(cell)
                for connection in cell.connects_from:
                    mark_next.append(connection.source)
        self.marked_cells += newly_marked
        self.mark_all_from_connects_from(mark_next)

    def remove_unmarked_cells(self):
        cells_to_remove = []
        for cell in self.all_cells:
            if not cell.is_marked():
                cells_to_remove.append(cell)
        for cell in cells_to_remove:
            self.all_cells.remove(cell)
            if cell in self.sensors:
                self.sensors.remove(cell)
            if cell in self.neurons:
                self.neurons.remove(cell)
            for connection in cell.connects_from:
                if connection in self.connections:
                    self.connections.remove(connection)
                if connection in connection.source.connects_to:
                    connection.source.connects_to.remove(connection)
            for connection in cell.connects_to:
                if connection in self.connections:
                    self.connections.remove(connection)
                if connection in connection.sink.connects_from:
                    connection.sink.connects_from.remove(connection)

    def clear_unused_cells(self):
        self.mark_used_cells()
        self.remove_unmarked_cells()
        self.reset_marks()

    def reset_marks(self):
        self.marked_cells = []
        for cell in self.all_cells:
            cell.reset_mark()

    def propagate(self):
        for cell in self.all_cells:
            cell.sum_of_inputs = 0.0
        for cell in self.sensors + self.neurons:
            for connection in cell.connects_to:
                connection.sink.sum_of_inputs += connection.strength * cell.value
        for cell in self.neurons + self.actuators:
            if cell.connects_from:
                cell.value = math.tanh(cell.sum_of_inputs)
            else:
                cell.value = 1.0

