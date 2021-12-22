# see Readme.md; Dave Miller's sensors, specifically see: getSensors.cpp
#   https://github.com/davidrmiller/biosim4/blob/main/src/getSensor.cpp
import unittest
from util import add_points
from parts.cells.sensors.Age import Age
from parts.cells.sensors.NearestBoundary import NearestBoundary
from parts.cells.sensors.NearestBoundaryEastWest import NearestBoundaryEastWest
from parts.cells.sensors.NearestBoundaryNorthSouth import NearestBoundaryNorthSouth
from parts.cells.sensors.LastMoveDirectionX import LastMoveDirectionX
from parts.cells.sensors.LastMoveDirectionY import LastMoveDirectionY
from parts.cells.sensors.LocationEastWest import LocationEastWest
from parts.cells.sensors.LocationNorthSouth import LocationNorthSouth
from parts.cells.sensors.Oscillator import Oscillator
from parts.cells.sensors.LongprobePopulationForward import LongprobePopulationFoward
from parts.cells.sensors.PopulationDensityNeighborhood import PopulationDensityNeighborhood
from parts.cells.sensors.PopulationDensityFoward import PopulationDensityFoward
from parts.cells.sensors.PopulationDensityLeftRight import PopulationDensityLeftRight
# from parts.cells.sensors.LongprobeBarrierForward import LongprobeBarrierFoward
# from parts.cells.sensors.BarrierFoward import BarrierFoward
# from parts.cells.sensors.BarrierLeftRight import BarrierLeftRight
from parts.cells.sensors.Random import Random
# from parts.cells.sensors.SignalDensityNeighborhood import SignalDensityNeighborhood
# from parts.cells.sensors.SignalDensityForward import SignalDensityForward
# from parts.cells.sensors.SignalDensityLeftRight import SignalDensityLeftRight
# from parts.cells.sensors.GeneticSimilarityForward import GeneticSimilarityForward

from Thing import Thing


class DummyWorld:

    def __init__(self, height, width):
        self.max_number_of_steps = 1000
        self.width = height
        self.height = width
        self.grid = [[None for _ in range(height)] for _ in range(width)]
        self.dummy_oscillator_value = 0.0
        self.dummy_random_value = 0.0

    def add_thing_to_world(self, thing):
        (x, y) = thing.pos
        self.grid[x][y] = thing

    def thing_at(self, pos):
        (x, y) = pos
        return self.grid[x][y]

    def get_oscillator_value(self):
        return self.dummy_oscillator_value

    def get_random_value_for_sensor(self):
        return self.dummy_random_value

    def is_free_grid_cell(self, x, y):
        return self.grid[x][y] is None


class DummyThing(Thing):

    def __init__(self, start_pos, world):
        super().__init__(start_pos, world)
        # note, actual direction, not intended (that is, updated on actual move)
        self.last_move_direction = (0, 0)  # (x, y): x is one of -1, 0, 1; same with y
        self.value_for_test = None
        self.neighborhood_cache = [None] * 8

    def update(self):
        # suppress action that depends on World
        pass

    def cache_local_neighorhood(self):
        # 'northward' (from top-center) clockwise
        local = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        # that is   N      NE      E       SE        S         SW       W        NW
        current_direction_index = -1
        for i in range(8):
            if local[i] == self.last_move_direction:
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


class TestSensors(unittest.TestCase):

    def test_sensor_age(self):
        start_pos = (10, 10)
        thing = DummyThing(start_pos, DummyWorld(1000, 1000))
        thing.age = 300
        sensor = Age(thing)
        sensor.set_sense_value()
        value = sensor.get_value()
        self.assertEqual(0.3, value)

    def test_sensor_abs_location(self):
        world = DummyWorld(1000, 1000)
        x = world.width / 2
        y = world.height / 2
        start_pos = (x, y)
        thing = DummyThing(start_pos, world)

        sensor_ew = LocationEastWest(thing)
        sensor_ew.set_sense_value()
        value = sensor_ew.get_value()
        self.assertEqual(0.5, value)

        sensor_ns = LocationNorthSouth(thing)
        sensor_ns.set_sense_value()
        value = sensor_ns.get_value()
        self.assertEqual(0.5, value)

    def test_distance_to_boundary(self):
        world = DummyWorld(1000, 1000)
        start_pos_center = (int(world.width / 2), int(world.height / 2))
        thing_center = DummyThing(start_pos_center, world)
        start_pos_ul = (int(world.width / 4), int(world.height / 4))
        thing_upper_left = DummyThing(start_pos_ul, world)

        self.assertEqual(500, thing_center.pos[0])
        self.assertEqual(500, thing_center.pos[1])

        self.assertEqual(250, thing_upper_left.pos[0])
        self.assertEqual(250, thing_upper_left.pos[1])

        sensor_center_min_dist = NearestBoundary(thing_center)
        sensor_center_min_x_dist = NearestBoundaryEastWest(thing_center)
        sensor_center_min_y_dist = NearestBoundaryNorthSouth(thing_center)

        sensor_ul_min_dist = NearestBoundary(thing_upper_left)
        sensor_ul_min_x_dist = NearestBoundaryEastWest(thing_upper_left)
        sensor_ul_min_y_dist = NearestBoundaryNorthSouth(thing_upper_left)

        sensor_center_min_dist.set_sense_value()
        value = sensor_center_min_dist.get_value()
        self.assertEqual(0.0, value)

        sensor_center_min_x_dist.set_sense_value()
        value = sensor_center_min_dist.get_value()
        self.assertEqual(0.0, value)

        sensor_center_min_y_dist.set_sense_value()
        value = sensor_center_min_dist.get_value()
        self.assertEqual(0.0, value)

        sensor_ul_min_dist.set_sense_value()
        value = sensor_ul_min_dist.get_value()
        self.assertEqual(0.5, value)

        sensor_ul_min_x_dist.set_sense_value()
        value = sensor_ul_min_x_dist.get_value()
        self.assertEqual(0.5, value)

        sensor_ul_min_y_dist.set_sense_value()
        value = sensor_ul_min_y_dist.get_value()
        self.assertEqual(0.5, value)

    def test_oscillator_sensor(self):
        world = DummyWorld(1000, 1000)
        world.dummy_oscillator_value = 0.5
        start_pos = (0, 0)
        thing = DummyThing(start_pos, world)
        self.assertEqual(0.5, thing.world.get_oscillator_value())

        sensor = Oscillator(thing)
        sensor.set_sense_value()
        value = sensor.get_value()

        self.assertEqual(0.5, value)

    def test_random_sensor(self):
        world = DummyWorld(1000, 1000)
        world.dummy_random_value = 0.2
        start_pos = (0, 0)
        thing = DummyThing(start_pos, world)

        sensor = Random(thing)
        sensor.set_sense_value()
        value = sensor.get_value()

        self.assertEqual(0.2, thing.world.get_random_value_for_sensor())
        self.assertEqual(0.2, value)

    def test_last_move_sensors(self):
        world = DummyWorld(1000, 1000)
        start_pos = (0, 0)
        thing = DummyThing(start_pos, world)

        thing.last_move_direction = (-1, 1)

        sensorx = LastMoveDirectionX(thing)
        sensory = LastMoveDirectionY(thing)

        sensorx.set_sense_value()
        sensory.set_sense_value()

        self.assertEqual(-1, sensorx.value)
        self.assertEqual(1, sensory.value)

    def test_population_density(self):
        world = DummyWorld(1000, 1000)
        start_pos = (10, 10)

        # set up neighbors
        world.add_thing_to_world(DummyThing(add_points(start_pos, (-1, -1)), world))  # SW
        world.add_thing_to_world(DummyThing(add_points(start_pos, (-1, 0)), world))   # W
        world.add_thing_to_world(DummyThing(add_points(start_pos, (-1, +1)), world))  # NW
        world.add_thing_to_world(DummyThing(add_points(start_pos, (0, -1)), world))   # S
        world.add_thing_to_world(DummyThing(add_points(start_pos, (0, +1)), world))   # N
        world.add_thing_to_world(DummyThing(add_points(start_pos, (1, 1)), world))    # NE

        self.assertIsNotNone(world.thing_at((9, 9)))     # SW
        self.assertIsNotNone(world.thing_at((9, 10)))    # W
        self.assertIsNotNone(world.thing_at((9, 11)))    # NW
        self.assertIsNotNone(world.thing_at((10, 9)))    # S
        self.assertIsNone(world.thing_at((10, 10)))     # Center
        self.assertIsNotNone(world.thing_at((10, 11)))  # N
        self.assertIsNone(world.thing_at((11, 9)))      # SE
        self.assertIsNone(world.thing_at((11, 10)))     # E
        self.assertIsNotNone(world.thing_at((11, 11)))  # NE

        thing = DummyThing(start_pos, world)
        world.add_thing_to_world(thing)
        self.assertIsNotNone(world.thing_at((10, 10)))  # Center

        thing.last_move_direction = (0, 0)          # not moving
        thing.cache_local_neighorhood()             # assume N as default
        self.assertEqual(0, thing.value_for_test)   # index 0 in N (see implementation of Thing above)

        thing.last_move_direction = (1, 1)         # moving NE
        thing.cache_local_neighorhood()
        self.assertEqual(1, thing.value_for_test)  # see DummyThing, above

        thing.last_move_direction = (-1, 1)
        thing.cache_local_neighorhood()
        self.assertEqual(7, thing.value_for_test)  # see DummyThing, above

        thing.last_move_direction = (1, 0)         # for move direction E
        thing.cache_local_neighorhood()
        self.assertEqual(2, thing.value_for_test)
        # starting in direction traveled, moving clockwise
        # neighbor in       E     SE     S     SW    W     NW    N     NE
        self.assertEqual([False, False, True, True, True, True, True, True],
                         thing.neighborhood_cache)
        # in terms of forward, left, backword, right...
        # that is           F     FR     R     BR    B     BL    L    FL

        population_density_neighborhood = PopulationDensityNeighborhood(thing)
        population_density_foward = PopulationDensityFoward(thing)
        population_density_left_right = PopulationDensityLeftRight(thing)
        longprobe_population_forward = LongprobePopulationFoward(thing)

        population_density_neighborhood.set_sense_value()
        population_density_foward.set_sense_value()
        population_density_left_right.set_sense_value()
        longprobe_population_forward.set_sense_value()

        self.assertEqual(6, sum(thing.neighborhood_cache))
        self.assertAlmostEqual(0.75, float(sum(thing.neighborhood_cache))/8.0, 2)

        self.assertAlmostEqual(0.75, population_density_neighborhood.value)

        # self.assertEqual(-1, population_density_foward.value)
        # self.assertEqual(-1, population_density_left_right.value)
        # self.assertEqual(-1, longprobe_population_forward.value)

    # untested...

    def test_signal_density(self):
        # SignalDensityNeighborhood import SignalDensityNeighborhood
        # SignalDensityForward import SignalDensityForward
        # SignalDensityLeftRight import SignalDensityLeftRight
        pass

    def test_barrier_distance(self):
        # BarrierFoward import BarrierFoward
        # BarrierLeftRight import BarrierLeftRight
        # LongprobeBarrierForward import LongprobeBarrierFoward
        pass

    def test_foward_genetic_similarity(self):
        # GeneticSimilarityForward import GeneticSimilarityForward
        pass
