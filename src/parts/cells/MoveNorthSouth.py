from parts.cells.BrainCell import BrainCell
from settings import GeneCellType


class MoveNorthSouth(BrainCell):

    def __init__(self):
        super().__init__()
        self.type = GeneCellType.ACTUATOR