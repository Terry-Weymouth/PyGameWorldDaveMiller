from random import randint
from util import add_points
from parts.cells.actuators.ActionAccumulator import ActionAccumulator


class Thing:

    def __init__(self, start_pos, world):
        self.world = world
        self.pos = start_pos
        self.next_pos = self.pos
        self.age = 0

    def get_normalized_age(self):
        return float(self.age)/float(self.world.max_number_of_steps)

    def desired_move(self):
        # sense environment
        # cycle brain
        # read out actions
        # effect world - random motion only for now
        dx = randint(0, 3) - 1
        dy = randint(0, 3) - 1
        return add_points(self.pos, (dx, dy))

    def set_next_world_position(self):
        check_pos = self.desired_move()
        (x, y) = check_pos
        if self.world.is_in_bounds(x, y) and self.world.is_free_grid_cell(x, y):
            self.next_pos = check_pos

#    def set_next_cycle_values(self):
#        accumulator = ActionAccumulator()

    def move_to_next_world_position(self):
        (x, y) = self.next_pos
        # in case it can't move
        self.next_pos = self.pos
        # multiple Things may be trying to move into the free cell
        # so, check is another Thing has already made the move
        if self.world.is_free_grid_cell(x, y):
            self.pos = (x, y)
            # reset next_pos
            self.next_pos = self.pos
            return True
        return False
