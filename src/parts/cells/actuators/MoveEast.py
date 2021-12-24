from parts.cells.actuators.Actuator import Actuator
from util import add_points


class MoveEast(Actuator):

    def __init__(self, thing):
        super().__init__(thing)

    def add_action(self, accumulator):
        dx = self.clip_effective_value()
        dy = 0.0
        accumulator.delta_pos = add_points((dx, dy), accumulator.delta_pos)
        return accumulator
