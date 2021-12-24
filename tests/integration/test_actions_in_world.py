import unittest
from parts.cells.actuators.ActionAccumulator import ActionAccumulator
from parts.cells.actuators.Actuator import Actuator
from parts.cells.actuators.MoveEast import MoveEast
from parts.cells.actuators.MoveWest import MoveWest
from parts.cells.actuators.MoveNorth import MoveNorth
from parts.cells.actuators.MoveSouth import MoveSouth

from Thing import Thing
from World import World
from parts.Brain import Brain
from util import add_points
from settings import GeneCellType

class DummyBrain(Brain):

    def __init__(self):
        self.all_cells = []
        self.sensors = []
        self.actuators = []
        self.neurons = []


class TestAcionsInTheWorld(unittest.TestCase):

    def test_move_unimplemented(self):
        world = World(1000)
        start_pos = (20, 20)
        thing = Thing(start_pos, world)
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
        brain = DummyBrain()

        for cell in actuator_list:
            self.assertEqual(GeneCellType.ACTUATOR, cell.type)
            brain.add_cell(cell)
        self.assertEqual(4, len(brain.all_cells))
        self.assertEqual(4, len(brain.actuators))
        for cell in brain.actuators:
            self.assertIn(cell, actuator_list)
        for cell in actuator_list:
            self.assertIn(cell, brain.actuators)

        values = [1.0, 1.0, 1.0, 1.0]
        results = [(1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0)]
        new_pos = add_points((0.0, 0.0), start_pos)
        self.assertEqual((20, 20), new_pos)
        for i in range(len(values)):
            actuator_list[i].value = values[i]
            accumulator = ActionAccumulator()
            sum = (0.0, 0.0)
            for j in range(i+1):
                sum = add_points(sum, results[j])
                accumulator = actuator_list[j].add_action(accumulator)
            self.assertEqual(sum, accumulator.delta_pos)
            new_pos = add_points(start_pos, accumulator.delta_pos)
            self.assertEqual(add_points(sum, start_pos), new_pos)

        self.assertIsNotNone(world.thing_at(start_pos))
        self.assertEqual(thing, world.thing_at(start_pos))
        sx = int(start_pos[0])
        sy = int(start_pos[1])
        nx = int(new_pos[0])
        ny = int(new_pos[1])
        thing.pos = (nx, ny)
        self.assertEqual(start_pos, thing.pos)

    def test_move_brain_no_net(self):

        world = World(1000)
        start_pos = (20, 20)
        thing = Thing(start_pos, world)
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
        brain = DummyBrain()

        for cell in actuator_list:
            self.assertEqual(GeneCellType.ACTUATOR, cell.type)
            brain.add_cell(cell)
        self.assertEqual(4, len(brain.all_cells))
        self.assertEqual(4, len(brain.actuators))
        for cell in brain.actuators:
            self.assertIn(cell, actuator_list)
        for cell in actuator_list:
            self.assertIn(cell, brain.actuators)

#        values = [1.0, 1.0, 1.0, 1.0]
#
#        world.grid[sx][sy] = None
#        world.grid[nx][ny] = thing
#        self.assertIsNotNone(world.thing_at((nx, ny)))
#        self.assertEqual(thing, world.thing_at((nx, ny)))
#        self.assertEqual(thing.pos, world.thing_at(thing.pos).pos)
