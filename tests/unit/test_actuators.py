# see Readme.md; Dave Miller's actions, specifically see: executeActions.cpp, sensors-actions.h
#   https://github.com/davidrmiller/biosim4/blob/main/src/executeActions.cpp
#   https://github.com/davidrmiller/biosim4/blob/main/src/sensors-actions.himport

import unittest
from parts.cells.actuators.ActionAccumulator import ActionAccumulator
from parts.cells.actuators.Actuator import Actuator
from parts.cells.actuators.MoveEast import MoveEast
from parts.cells.actuators.MoveWest import MoveWest
from parts.cells.actuators.MoveNorth import MoveNorth
from parts.cells.actuators.MoveSouth import MoveSouth

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

    def test_value_cliping(self):
        actuator = Actuator(DummyThing(0.0, DummyWorld(1000)))
        actuator.value = -1.0
        self.assertEqual(0.0, actuator.clip_effective_value())
        actuator.value = -0.5
        self.assertEqual(0.0, actuator.clip_effective_value())
        actuator.value = 0.5
        self.assertEqual(0.5, actuator.clip_effective_value())
        actuator.value = 1.0
        self.assertEqual(1.0, actuator.clip_effective_value())
        actuator.value = 1.5
        self.assertEqual(1.0, actuator.clip_effective_value())

    def test_move_east(self):
        world = DummyWorld(1000)
        start_pos = (20, 20)
        thing = DummyThing((20, 20), world)
        self.assertEqual(start_pos, thing.pos)
        world.add_thing_to_world(thing)
        self.assertIsNotNone(world.thing_at(start_pos))
        self.assertEqual(thing, world.thing_at(start_pos))
        actuator = MoveEast(thing)
        actuator.value = 1.0
        accumulator = ActionAccumulator()
        results = actuator.add_action(accumulator)
        self.assertEqual(1.0, results.delta_pos[0])
        self.assertEqual(0.0, results.delta_pos[1])

        actuator.value = -1.0
        accumulator = ActionAccumulator()
        results = actuator.add_action(accumulator)
        self.assertEqual(0.0, results.delta_pos[0])
        self.assertEqual(0.0, results.delta_pos[1])

    def test_move_west(self):
        world = DummyWorld(1000)
        start_pos = (20, 20)
        thing = DummyThing((20, 20), world)
        self.assertEqual(start_pos, thing.pos)
        world.add_thing_to_world(thing)
        self.assertIsNotNone(world.thing_at(start_pos))
        self.assertEqual(thing, world.thing_at(start_pos))
        actuator = MoveWest(thing)
        actuator.value = 1.0
        accumulator = ActionAccumulator()
        results = actuator.add_action(accumulator)
        self.assertEqual(-1.0, results.delta_pos[0])
        self.assertEqual(0.0, results.delta_pos[1])

        actuator.value = -1.0
        accumulator = ActionAccumulator()
        results = actuator.add_action(accumulator)
        self.assertEqual(0.0, results.delta_pos[0])
        self.assertEqual(0.0, results.delta_pos[1])

    def test_move_north(self):
        world = DummyWorld(1000)
        start_pos = (20, 20)
        thing = DummyThing((20, 20), world)
        self.assertEqual(start_pos, thing.pos)
        world.add_thing_to_world(thing)
        self.assertIsNotNone(world.thing_at(start_pos))
        self.assertEqual(thing, world.thing_at(start_pos))
        actuator = MoveNorth(thing)

        actuator.value = -1.0
        accumulator = ActionAccumulator()
        results = actuator.add_action(accumulator)
        self.assertEqual(0.0, results.delta_pos[0])
        self.assertEqual(0.0, results.delta_pos[1])

        actuator.value = 1.0
        accumulator = ActionAccumulator()
        results = actuator.add_action(accumulator)
        self.assertEqual(0.0, results.delta_pos[0])
        self.assertEqual(1.0, results.delta_pos[1])

    def test_move_south(self):
        world = DummyWorld(1000)
        start_pos = (20, 20)
        thing = DummyThing((20, 20), world)
        self.assertEqual(start_pos, thing.pos)
        world.add_thing_to_world(thing)
        self.assertIsNotNone(world.thing_at(start_pos))
        self.assertEqual(thing, world.thing_at(start_pos))
        actuator = MoveSouth(thing)
        actuator.value = -1.0
        accumulator = ActionAccumulator()
        results = actuator.add_action(accumulator)
        self.assertEqual(0.0, results.delta_pos[0])
        self.assertEqual(0.0, results.delta_pos[1])

        actuator.value = 1.0
        accumulator = ActionAccumulator()
        results = actuator.add_action(accumulator)
        self.assertEqual(0.0, results.delta_pos[0])
        self.assertEqual(-1.0, results.delta_pos[1])

    def test_move_north_south_east_west(self):
        world = DummyWorld(1000)
        start_pos = (20, 20)
        thing = DummyThing((20, 20), world)
        self.assertEqual(start_pos, thing.pos)
        world.add_thing_to_world(thing)
        self.assertIsNotNone(world.thing_at(start_pos))
        self.assertEqual(thing, world.thing_at(start_pos))
        actuator_list = [
            MoveEast(thing),
            MoveWest(thing),
            MoveNorth(thing),
            MoveSouth(thing)
            ]
        values = [1.0, 0.5, 1.0, 0.5]
        results = [(1.0, 0.0), (0.5, 0.0), (0.5, 1.0), (0.5, 0.5)]
        accumulator = ActionAccumulator()
        for i in range(len(values)):
            actuator_list[i].value = values[i]
            accumulator = actuator_list[i].add_action(accumulator)
            self.assertEqual(results[i], accumulator.delta_pos, "at i = " + str(i))

# untested
#    MOVE_X,                   // W +- X component of movement
#    MOVE_Y,                   // W +- Y component of movement
#    MOVE_FORWARD,             // W continue last direction
#    MOVE_RL,                  // W +- component of movement
#    MOVE_LEFT,                // W
#    MOVE_RIGHT,               // W
#    MOVE_REVERSE,             // W
#    MOVE_RANDOM,              // W
#    SET_OSCILLATOR_PERIOD,    // I
#    SET_LONGPROBE_DIST,       // I
#    SET_RESPONSIVENESS,       // I
#    EMIT_SIGNAL0,             // W
