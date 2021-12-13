from settings import NUMBER_OF_NEURONS
# Sensors
from parts.cells.LocationEastWest import LocationEastWest
from parts.cells.LocationNorthSouth import LocationNorthSouth
from parts.cells.Age import Age
# Actuators
from parts.cells.MoveEastWest import MoveEastWest
from parts.cells.MoveNorthSouth import MoveNorthSouth
# Neuron
from parts.cells.Neuron import Neuron


class CellCollection:

    def __init__(self):
        self.sensors = [LocationEastWest(), LocationNorthSouth(), Age()]
        self.actuators = [MoveEastWest(), MoveNorthSouth()]
        self.neurons = []
        while len(self.neurons) < NUMBER_OF_NEURONS:
            self.neurons.append(Neuron())

    def get_sensors(self):
        return self.sensors

    def get_actuators(self):
        return self.actuators

    def get_neurons(self):
        return self.neurons

