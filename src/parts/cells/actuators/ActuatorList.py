from parts.cells.actuators.MoveEastWest import MoveEastWest
from parts.cells.actuators.MoveNorthSouth import MoveNorthSouth


class ActuatorList:

    def __init__(self, thing):
        self.actuators = [
            MoveEastWest(thing),
            MoveNorthSouth(thing)
        ]
