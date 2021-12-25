import unittest
from parts.cells.actuators.ActionAccumulator import ActionAccumulator
from parts.cells.actuators.MoveEast import MoveEast
from parts.cells.actuators.MoveWest import MoveWest
from parts.cells.actuators.MoveNorth import MoveNorth
from parts.cells.actuators.MoveSouth import MoveSouth

from Thing import Thing
from World import World
from util import add_points
from settings import GeneCellType


class DummyBrain:

    def __init__(self):
        self.all_cells = []
        self.sensors = []
        self.actuators = []
        self.neurons = []

    def add_cell(self, cell):
        cell_type = cell.type
        if cell not in self.all_cells:
            self.all_cells.append(cell)
        if cell_type is GeneCellType.SENSOR:
            if cell not in self.sensors:
                self.sensors.append(cell)
        if cell_type is GeneCellType.ACTUATOR:
            if cell not in self.actuators:
                self.actuators.append(cell)
        if cell_type is GeneCellType.NEURON:
            if cell not in self.neurons:
                self.neurons.append(cell)


class TestAcionsInTheWorld(unittest.TestCase):

    def test_move_unimplemented(self):
        world = World(1000)
        start_pos = (20, 20)
        thing = Thing(start_pos, world)
        self.assertEqual(start_pos, thing.pos)
        world.things = []
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
            test_sum = (0.0, 0.0)
            for j in range(i+1):
                test_sum = add_points(test_sum, results[j])
                accumulator = actuator_list[j].add_action(accumulator)
            self.assertEqual(test_sum, accumulator.delta_pos)
            new_pos = add_points(start_pos, accumulator.delta_pos)
            self.assertEqual(add_points(test_sum, start_pos), new_pos)

        self.assertIsNotNone(world.thing_at(start_pos))
        self.assertEqual(thing, world.thing_at(start_pos))
        nx = int(new_pos[0])
        ny = int(new_pos[1])
        thing.pos = (nx, ny)
        self.assertEqual(start_pos, thing.pos)

    def test_dummy_brain_move_north_east(self):

        world = World(1000)
        start_pos = (20, 20)
        thing = Thing(start_pos, world)
        thing.brain = DummyBrain()
        self.assertEqual(start_pos, thing.pos)
        world.things = []
        world.add_thing_to_world(thing)
        self.assertEqual(1, len(world.things))
        self.assertEqual(thing, world.things[0])
        self.assertIsNotNone(world.thing_at(start_pos))
        self.assertEqual(thing, world.thing_at(start_pos))
        actuator_list = [
            MoveEast(thing),
            MoveWest(thing),
            MoveNorth(thing),
            MoveSouth(thing)
            ]

        for cell in actuator_list:
            self.assertEqual(GeneCellType.ACTUATOR, cell.type)
            thing.brain.add_cell(cell)
        self.assertEqual(4, len(thing.brain.all_cells))
        self.assertEqual(4, len(thing.brain.actuators))
        self.assertEqual(1, len(world.things))
        self.assertEqual(thing, world.things[0])
        self.assertEqual(4, len(world.things[0].brain.actuators))
        for cell in thing.brain.actuators:
            self.assertIn(cell, actuator_list)
        for cell in actuator_list:
            self.assertIn(cell, thing.brain.actuators)

        values = [0.6, 0.0, 0.6, 0.0]  # east, west, north, south
        for i in range(len(values)):
            actuator_list[i].value = values[i]

        world.one_step_all()
        self.assertIsNone(world.thing_at(start_pos))
        self.assertEqual((21, 21), thing.pos)
        self.assertEqual(thing, world.thing_at(thing.pos))

    def test_dummy_brain_move_south_east_then_east(self):

        world = World(1000)
        start_pos = (20, 20)
        thing = Thing(start_pos, world)
        thing.brain = DummyBrain()
        self.assertEqual(start_pos, thing.pos)
        world.things = []
        world.add_thing_to_world(thing)
        self.assertEqual(1, len(world.things))
        self.assertEqual(thing, world.things[0])
        self.assertIsNotNone(world.thing_at(start_pos))
        self.assertEqual(thing, world.thing_at(start_pos))
        actuator_list = [
            MoveEast(thing),
            MoveWest(thing),
            MoveNorth(thing),
            MoveSouth(thing)
            ]

        for cell in actuator_list:
            self.assertEqual(GeneCellType.ACTUATOR, cell.type)
            thing.brain.add_cell(cell)
        self.assertEqual(4, len(thing.brain.all_cells))
        self.assertEqual(4, len(thing.brain.actuators))
        self.assertEqual(1, len(world.things))
        self.assertEqual(thing, world.things[0])
        self.assertEqual(4, len(world.things[0].brain.actuators))
        for cell in thing.brain.actuators:
            self.assertIn(cell, actuator_list)
        for cell in actuator_list:
            self.assertIn(cell, thing.brain.actuators)

        values = [1.0, 0.0, 0.0, 1.0]  # east, west, north, south
        for i in range(len(values)):
            actuator_list[i].value = values[i]

        world.one_step_all()
        self.assertIsNone(world.thing_at(start_pos))
        self.assertEqual((21, 19), thing.pos)
        self.assertEqual(thing, world.thing_at(thing.pos))

        values = [1.0, 0.0, 0.0, 0.0]  # east, west, north, south
        for i in range(len(values)):
            actuator_list[i].value = values[i]

        world.one_step_all()
        self.assertEqual((22, 19), thing.pos)
        self.assertEqual(thing, world.thing_at(thing.pos))

