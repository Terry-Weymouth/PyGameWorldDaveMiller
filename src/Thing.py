from math import sin, pi
from util import add_points
from parts.Brain import Brain
from parts.cells.actuators.ActionAccumulator import ActionAccumulator


class Thing:

    def __init__(self, start_pos, world):
        self.world = world
        self.pos = start_pos
        self.next_pos = self.pos
        self.move_direction = (0, 0)
        self.age = 0
        self.brain = None

    def set_brain(self, genome, initial_cells):
        self.brain = Brain(genome, initial_cells)

    def get_normalized_age(self):
        return float(self.age)/float(self.world.max_number_of_steps)

    def set_sensors(self):
        for sensor in self.brain.sensors:
            sensor.set_sense_value()

    def setup_next_step_from_actions(self):
        actions = ActionAccumulator()
        for cell in self.brain.actuators:
            actions = cell.add_action(actions)
        self.next_pos = self.round_up_motion_steps(add_points(self.pos, actions.delta_pos))

    @staticmethod
    def round_up_motion_steps(pos):
        (x, y) = pos
        return int(x + 0.5), int(y + 0.5)

    def move_to_next_world_position(self):
        (x, y) = self.next_pos
        # in case it can't move
        self.next_pos = self.pos
        # multiple Things may be trying to move into the free cell
        # so, check is another Thing has already made the move
        if self.world.is_free_grid_cell(x, y):
            self.move_direction = (x - self.pos[0], y - self.pos[1])
            self.pos = (x, y)
            # reset next_pos
            self.next_pos = self.pos
            return True
        return False

    def get_oscillator_value(self):
        return sin((self.age * pi) / 100.0)

