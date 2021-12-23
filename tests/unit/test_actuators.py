# see Readme.md; Dave Miller's actions, specifically see: executeActions.cpp, sensors-actions.h
#   https://github.com/davidrmiller/biosim4/blob/main/src/executeActions.cpp
#   https://github.com/davidrmiller/biosim4/blob/main/src/sensors-actions.himport

import unittest
from parts.cells.actuators.MoveEastWest import MoveEastWest
# from parts.cells.actuators.MoveNorthSouth import MoveNorthSouth

from Thing import Thing
from World import World


class DummyWorld(World):

    def __init__(self, size):
        super().__init__(size)
        self.max_number_of_steps = size
        self.width = size
        self.height = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.dummy_random_value = 0.0

    def get_random_value_for_sensor(self):
        return self.dummy_random_value


class DummyThing(Thing):

    def __init__(self, start_pos, world):
        super().__init__(start_pos, world)

    def update(self):
        # suppress action that depends on World
        pass


class TestActuators(unittest.TestCase):

    def test_move_east_west(self):
        world = DummyWorld(1000)
        start_pos = (20, 20)
        thing = DummyThing((20, 20), world)
        self.assertEqual(start_pos, thing.pos)
        world.add_thing_to_world(thing)
        self.assertIsNotNone(world.thing_at(start_pos))
        self.assertEqual(thing, world.thing_at(start_pos))


    def test_move_north_south(self):
        pass
