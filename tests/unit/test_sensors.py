# see Readme.md; Dave Miller's sensors, specifically see: getSensors.cpp
#   https://github.com/davidrmiller/biosim4/blob/main/src/getSensor.cpp
import unittest
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
from parts.cells.sensors.LongprobeBarrierForward import LongprobeBarrierFoward
from parts.cells.sensors.PopulationDensityNeighborhood import PopulationDensityNeighborhood
from parts.cells.sensors.PopulationDensityFoward import PopulationDensityFoward
from parts.cells.sensors.PopulationDensityLeftRight import PopulationDensityLeftRight
from parts.cells.sensors.BarrierFoward import BarrierFoward
from parts.cells.sensors.BarrierLeftRight import BarrierLeftRight
from parts.cells.sensors.Random import Random
from parts.cells.sensors.SignalDensityNeighborhood import SignalDensityNeighborhood
from parts.cells.sensors.SignalDensityForward import SignalDensityForward
from parts.cells.sensors.SignalDensityLeftRight import SignalDensityLeftRight
from parts.cells.sensors.GeneticSimilarityForward import GeneticSimilarityForward

from Thing import Thing


class DummyWorld:

    def __init__(self):
        self.max_number_of_steps = 1000
        self.width = 1000
        self.height = 1000
        self.dummy_oscillator_value = 0.0
        self.dummy_random_value = 0.0

    def get_oscillator_value(self):
        return self.dummy_oscillator_value

    def get_random_value_for_sensor(self):
        return self.dummy_random_value


class TestingThing(Thing):

    def update(self):
        # suppress action that depends on World
        pass


class TestSensors(unittest.TestCase):

    def test_sensor_age(self):
        start_pos = (10, 10)
        thing = TestingThing(start_pos, DummyWorld())
        thing.age = 300
        sensor = Age(thing)
        sensor.set_sense_value()
        value = sensor.get_value()
        self.assertEqual(0.3, value)

    def test_sensor_abs_location(self):
        world = DummyWorld()
        x = world.width / 2
        y = world.height / 2
        start_pos = (x, y)
        thing = TestingThing(start_pos, world)

        sensor_ew = LocationEastWest(thing)
        sensor_ew.set_sense_value()
        value = sensor_ew.get_value()
        self.assertEqual(0.5, value)

        sensor_ns = LocationNorthSouth(thing)
        sensor_ns.set_sense_value()
        value = sensor_ns.get_value()
        self.assertEqual(0.5, value)

    def test_distance_to_boundary(self):
        world = DummyWorld()
        start_pos_center = (int(world.width / 2), int(world.height / 2))
        thing_center = TestingThing(start_pos_center, world)
        start_pos_ul = (int(world.width / 4), int(world.height / 4))
        thing_upper_left = TestingThing(start_pos_ul, world)

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
        world = DummyWorld()
        world.dummy_oscillator_value = 0.5
        start_pos = (0, 0)
        thing = TestingThing(start_pos, world)
        self.assertEqual(0.5, thing.world.get_oscillator_value())

        sensor = Oscillator(thing)
        sensor.set_sense_value()
        value = sensor.get_value()

        self.assertEqual(0.5, value)

    def test_random_sensor(self):
        world = DummyWorld()
        world.dummy_random_value = 0.2
        start_pos = (0, 0)
        thing = TestingThing(start_pos, world)

        sensor = Random(thing)
        sensor.set_sense_value()
        value = sensor.get_value()

        self.assertEqual(0.2, thing.world.get_random_value_for_sensor())
        self.assertEqual(0.2, value)


