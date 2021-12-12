import unittest
from parts.BrainFactory import BrainFactory


class TestBrain(unittest.TestCase):

    def test_make_initial_connections(self):
        factory = BrainFactory()
