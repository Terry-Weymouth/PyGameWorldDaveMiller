import unittest
from parts.cells.brain_cell_types import SENSORS, ACTUATORS, NURONS
from settings import GeneCellType


class BrianCellTest(unittest.TestCase):

    def test_brain_cell_type(self):
        for cell in SENSORS:
            self.assertEqual(GeneCellType.SENSOR, cell.type)
        for cell in ACTUATORS:
            self.assertEqual(GeneCellType.ACTUATOR, cell.type)
        for cell in NURONS:
            self.assertEqual(GeneCellType.NEURON, cell.type)
