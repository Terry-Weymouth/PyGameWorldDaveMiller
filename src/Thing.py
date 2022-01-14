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
        self.neighborhood_cache = None
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
            self.cache_local_neighorhood()
            return True
        return False

    def get_oscillator_value(self):
        return sin((self.age * pi) / 100.0)

    def cache_local_neighorhood(self):
        # 'northward' (from top-center) clockwise
        local = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        # that is   N      NE      E       SE        S         SW       W        NW
        current_direction_index = -1
        for i in range(8):
            if local[i] == self.move_direction:
                current_direction_index = i
        if current_direction_index < 0:
            # the current direction is (0 0), no movement - default to north for now
            current_direction_index = 0
        self.value_for_test = current_direction_index
        new_local = local[current_direction_index:] + local[:current_direction_index]
        cache = []
        for offset in new_local:
            (x, y) = add_points(self.pos, offset)
            cache.append(not self.world.is_free_grid_cell(x, y))
        self.neighborhood_cache = cache
        # in terms of forward, left, backword, right... from forward clockwise
        # for cache index  0   1   2   3   4   5   6   7
        # that is          F   FR  R   BR  B   BL  L   FL

    def forward_neighbor_count(self):  # 0 - 3
        # cache indexs = [7, 0, 1] - that is Fl, F, and FR
        count = 0
        for index in [7, 0, 6]:
            if self.neighborhood_cache:
                count += 1
        return count

    def left_right_neighbor_count(self):  # 0 - 6
        # cache indexs = [1, 2, 3, 5, 6, 7] - that is FR, R, BR, BL, L, FL
        count = 0
        for index in [1, 2, 3, 5, 6, 7]:
            if self.neighborhood_cache:
                count += 1
        return count

    def neighbor_count(self):  # 0 - 8
        # all directions
        count = 0
        for index in range(8):
            if self.neighborhood_cache:
                count += 1
        return count
