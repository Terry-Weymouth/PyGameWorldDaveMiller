import unittest
from parts.BrainFactory import BrainFactory


class TestBrain(unittest.TestCase):

    def test_make_true_connections(self):
        factory = BrainFactory()
