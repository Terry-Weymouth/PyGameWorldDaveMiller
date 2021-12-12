from settings import NUMBER_OF_NEURONS
# Sensors
from parts.cells.LocationEastWest import LocationEastWest
from parts.cells.LocationNorthSouth import LocationNorthSouth
# Actuators
from parts.cells.MoveEastWest import MoveEastWest
from parts.cells.MoveNorthSouth import MoveNorthSouth
# Neuron
from parts.cells.Neuron import Neuron

SENSORS = [LocationEastWest(), LocationNorthSouth()]
ACTUATORS = [MoveEastWest(), MoveNorthSouth()]
NEURONS = [Neuron() for i in range(NUMBER_OF_NEURONS)]
