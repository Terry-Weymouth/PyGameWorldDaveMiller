import unittest


class TestTest(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(6, sum([1, 2, 3]), "Should be 6")
