from settings import NUMBER_OF_NEURONS
from parts.cells.Neuron import Neuron
from parts.cells.sensors.SensorList import SensorList
from parts.cells.actuators.ActuatorList import ActuatorList


class CellCollection:

    def __init__(self, thing):
        self.sensors = SensorList(thing).sensors
        self.actuators = ActuatorList(thing).actuators
        self.neurons = []
        while len(self.neurons) < NUMBER_OF_NEURONS:
            self.neurons.append(Neuron())

    def get_sensors(self):
        return self.sensors

    def get_actuators(self):
        return self.actuators

    def get_neurons(self):
        return self.neurons
