from parts.cells.BrainCell import BrainCell
from settings import GeneCellType


class Actuator(BrainCell):

    def __init__(self, thing):
        super().__init__()
        self.type = GeneCellType.ACTUATOR
        self.thing = thing
