
import unittest
from shapley_value import ShapleyValue

class TestShapleyValue(unittest.TestCase):
    def test_calculate_shapley_values(self):
        players = ['A', 'B', 'C']
        coalition_values = {
            ('A',): 10,
            ('B',): 20,
            ('C',): 30,
            ('A', 'B'): 50,
            ('A', 'C'): 60,
            ('B', 'C'): 70,
            ('A', 'B', 'C'): 100
        }
        shapley = ShapleyValue(players, coalition_values)
        shapley_values = shapley.calculate_shapley_values()
        self.assertIsInstance(shapley_values, dict)
        self.assertEqual(len(shapley_values), len(players))
