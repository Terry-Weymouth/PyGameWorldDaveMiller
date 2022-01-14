from parts.cells.sensors.Age import Age
from parts.cells.sensors.LocationEastWest import LocationEastWest
from parts.cells.sensors.LocationNorthSouth import LocationNorthSouth
from parts.cells.sensors.LastMoveDirectionX import LastMoveDirectionX
from parts.cells.sensors.LastMoveDirectionY import LastMoveDirectionY
from parts.cells.sensors.NearestBoundary import NearestBoundary
from parts.cells.sensors.NearestBoundaryEastWest import NearestBoundaryEastWest
from parts.cells.sensors.NearestBoundaryNorthSouth import NearestBoundaryNorthSouth
from parts.cells.sensors.PopulationDensityNeighborhood import PopulationDensityNeighborhood
from parts.cells.sensors.PopulationDensityFoward import PopulationDensityFoward
from parts.cells.sensors.PopulationDensityLeftRight import PopulationDensityLeftRight
from parts.cells.sensors.Oscillator import Oscillator
from parts.cells.sensors.Random import Random


class SensorList:

    def __init__(self, thing):
        self.sensors = [
            LocationEastWest(thing),
            LocationNorthSouth(thing),
            Age(thing),
            LastMoveDirectionX(thing),
            LastMoveDirectionY(thing),
            NearestBoundary(thing),
            NearestBoundaryEastWest(thing),
            NearestBoundaryNorthSouth(thing),
            PopulationDensityNeighborhood(thing),
            PopulationDensityFoward(thing),
            PopulationDensityLeftRight(thing),
            Oscillator(thing),
            Random(thing)
        ]
