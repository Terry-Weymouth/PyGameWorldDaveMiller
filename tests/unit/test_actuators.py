# see Readme.md; Dave Miller's actions, specifically see: executeActions.cpp, sensors-actions.h
#   https://github.com/davidrmiller/biosim4/blob/main/src/executeActions.cpp
#   https://github.com/davidrmiller/biosim4/blob/main/src/sensors-actions.himport

import unittest
from parts.cells.actuators.MoveEastWest import MoveEastWest
# from parts.cells.actuators.MoveNorthSouth import MoveNorthSouth

from Thing import Thing


class DummyWorld:

    def __init__(self, height, width):
        self.max_number_of_steps = 1000
        self.width = height
        self.height = width
        self.grid = [[None for _ in range(height)] for _ in range(width)]
        self.dummy_random_value = 0.0

    def add_thing_to_world(self, thing):
        (x, y) = thing.pos
        self.grid[x][y] = thing

    def thing_at(self, pos):
        (x, y) = pos
        return self.grid[x][y]

    def get_random_value_for_sensor(self):
        return self.dummy_random_value

    def is_free_grid_cell(self, x, y):
        return self.grid[x][y] is None


class DummyThing(Thing):

    def __init__(self, start_pos, world):
        super().__init__(start_pos, world)

    def update(self):
        # suppress action that depends on World
        pass


class TestActuators(unittest.TestCase):

    def test_move_east_west(self):
        world = DummyWorld(1000, 1000)
        start_pos = (20, 20)
        thing = DummyThing((20, 20), world)
        self.assertEqual(start_pos, thing.pos)
        world.add_thing_to_world(thing)
        self.assertIsNotNone(world.thing_at(start_pos))
        self.assertEqual(thing, world.thing_at(start_pos))
        

    def test_move_north_south(self):
        pass
