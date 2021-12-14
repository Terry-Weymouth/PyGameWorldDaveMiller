from parts.cells.BrainCell import BrainCell
from settings import GeneCellType


class Sensor(BrainCell):

    def __init__(self, thing):
        super().__init__()
        self.type = GeneCellType.SENSOR
        self.thing = thing

    def set_sense_value(self):
        self.value = 0.0
