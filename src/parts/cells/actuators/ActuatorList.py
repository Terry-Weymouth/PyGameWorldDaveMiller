from parts.cells.actuators.MoveEast import MoveEast
from parts.cells.actuators.MoveWest import MoveWest
from parts.cells.actuators.MoveNorth import MoveNorth
from parts.cells.actuators.MoveSouth import MoveSouth


class ActuatorList:

    def __init__(self, thing):
        self.actuators = [
            MoveEast(thing),
            MoveWest(thing),
            MoveNorth(thing),
            MoveSouth(thing)
        ]
