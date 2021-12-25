from parts.cells.actuators.Actuator import Actuator
from util import add_points


class MoveNorth(Actuator):

    def __init__(self, thing):
        super().__init__(thing)

    def add_action(self, accumulator):
        dx = 0.0
        dy = -self.clip_effective_value()
        accumulator.delta_pos = add_points((dx, dy), accumulator.delta_pos)
        return accumulator


