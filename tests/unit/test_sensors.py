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
        thing = TestingThing(start_pos, DummyWorld())

        sensor_ew = LocationEastWest(thing)
        sensor_ew.set_sense_value()
        value = sensor_ew.get_value()
        self.assertEqual(0.5, value)

        sensor_ns = LocationNorthSouth(thing)
        sensor_ns.set_sense_value()
        value = sensor_ns.get_value()
        self.assertEqual(0.5, value)

