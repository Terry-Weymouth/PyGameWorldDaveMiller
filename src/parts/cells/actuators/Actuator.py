from parts.cells.BrainCell import BrainCell
from settings import GeneCellType


class Actuator(BrainCell):

    def __init__(self, thing):
        super().__init__()
        self.type = GeneCellType.ACTUATOR
        self.thing = thing

    def add_action(self, accumulator=None):
        s = "No action annotation " + str(self.__class__)
        print(s)
        raise NotImplementedError(s)

    def clip_effective_value(self):
        return min(1.0, max(0.0, float(self.value)))

