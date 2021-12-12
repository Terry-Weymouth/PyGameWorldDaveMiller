from parts.cells.brain_cell_arrays import SENSORS, ACTUATORS, NEURONS
from parts.BrainFactory import BrainFactory

factory = BrainFactory()


class Brain:

    def __init__(self, genom):
        self.genom = genom
        self.sensors = SENSORS
        self.actuators = ACTUATORS
        self.neurons = NEURONS
        self.connections = factory.make_connections_from(genom)
