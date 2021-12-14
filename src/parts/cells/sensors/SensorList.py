from parts.cells.sensors.LocationEastWest import LocationEastWest
from parts.cells.sensors.LocationNorthSouth import LocationNorthSouth
from parts.cells.sensors.Age import Age


class SensorList:

    def __init__(self, thing):
        self.sensors = [
            LocationEastWest(thing),
            LocationNorthSouth(thing),
            Age(thing)
        ]
