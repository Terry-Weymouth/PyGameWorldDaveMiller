from settings import NUMBER_OF_NURONS
from parts.cells.LocationEastWest import LocationEastWest
from parts.cells.LocationNorthSouth import LocationNorthSouth
from parts.cells.MoveEastWest import MoveEastWest
from parts.cells.MoveNorthSouth import MoveNorthSouth
from parts.cells.Neuron import Neuron

SENSORS = [LocationEastWest(), LocationNorthSouth()]
ACTUATORS = [MoveEastWest(), MoveNorthSouth()]
NURONS = [Neuron() for i in range(NUMBER_OF_NURONS)]
