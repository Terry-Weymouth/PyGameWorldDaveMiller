from random import randint
from parts.cells.actuators.Actuator import Actuator
from util import add_points


class MoveRandom(Actuator):

    def __init__(self, thing):
        super().__init__(thing)

    def add_action(self, accumulator):
        weight = self.clip_effective_value()
        dx = (randint(0, 2) - 1) * weight
        dy = (randint(0, 2) - 1) * weight
        accumulator.delta_pos = add_points((dx, dy), accumulator.delta_pos)
        return accumulator
