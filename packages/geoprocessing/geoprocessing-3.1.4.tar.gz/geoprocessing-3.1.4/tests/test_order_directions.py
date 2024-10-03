import unittest

from .utils import load_result, load_sample
from geoprocessing.order_directions import order_directions


class TestOrderDirections(unittest.TestCase):
    def test_order_directions(self):
        directions = load_result('process_directions', 'b10B9.json')
        trip = load_sample('geotab/b10B9.json')
        result = order_directions(directions, trip['coordinates'])
        expected_result = load_result('order_directions', 'b10B9.json')
        self.assertEqual(expected_result, result)

        directions = load_result('process_directions', 'b10DB.json')
        trip = load_sample('geotab/b10DB.json')
        result = order_directions(directions, trip['coordinates'])
        expected_result = load_result('order_directions', 'b10DB.json')
        self.assertEqual(expected_result, result)

        directions = load_result('process_directions', 'b26DB.json')
        trip = load_sample('geotab/b26DB.json')
        result = order_directions(directions, trip['coordinates'])
        expected_result = load_result('order_directions', 'b26DB.json')
        self.assertEqual(expected_result, result)

        directions = load_result('process_directions', 'b26F4.json')
        trip = load_sample('geotab/b26F4.json')
        result = order_directions(directions, trip['coordinates'])
        expected_result = load_result('order_directions', 'b26F4.json')
        self.assertEqual(expected_result, result)

        directions = load_result('process_directions', 'bA8D.json')
        trip = load_sample('geotab/bA8D.json')
        result = order_directions(directions, trip['coordinates'])
        expected_result = load_result('order_directions', 'bA8D.json')
        self.assertEqual(expected_result, result)

        directions = load_result('process_directions', 'bAD0.json')
        trip = load_sample('geotab/bAD0.json')
        result = order_directions(directions, trip['coordinates'])
        expected_result = load_result('order_directions', 'bAD0.json')
        self.assertEqual(expected_result, result)

        directions = load_result('process_directions', 'simulated_trip_1.json')
        trip = load_sample('simulated_trip_1.json')
        result = order_directions(directions, trip['coordinates'])
        expected_result = load_result('order_directions', 'simulated_trip_1.json')
        self.assertEqual(expected_result, result)

        directions = load_result('process_directions', 'simulated_trip_2.json')
        trip = load_sample('simulated_trip_2.json')
        result = order_directions(directions, trip['coordinates'])
        expected_result = load_result('order_directions', 'simulated_trip_2.json')
        self.assertEqual(expected_result, result)

        directions = load_result('process_directions', '75d34b3e1ddc7cf02b76f56fe64cdd8c767e9d7e.json')
        trip = load_sample('wejo/75d34b3e1ddc7cf02b76f56fe64cdd8c767e9d7e.json')
        result = order_directions(directions, trip['coordinates'])
        expected_result = load_result('order_directions', '75d34b3e1ddc7cf02b76f56fe64cdd8c767e9d7e.json')
        self.assertEqual(expected_result, result)

        directions = load_result('process_directions', 'f9451b80157c55043d4ade9ec90721f0f6c4d3f8.json')
        trip = load_sample('wejo/f9451b80157c55043d4ade9ec90721f0f6c4d3f8.json')
        result = order_directions(directions, trip['coordinates'])
        expected_result = load_result('order_directions', 'f9451b80157c55043d4ade9ec90721f0f6c4d3f8.json')
        self.assertEqual(expected_result, result)

        directions = load_result('process_directions', '4a2397771b3f2518f9e8b81f1db38e2f0e1b5126.json')
        trip = load_sample('wejo/4a2397771b3f2518f9e8b81f1db38e2f0e1b5126.json')
        result = order_directions(directions, trip['coordinates'])
        expected_result = load_result('order_directions', '4a2397771b3f2518f9e8b81f1db38e2f0e1b5126.json')
        self.assertEqual(expected_result, result)

        directions = load_result('process_directions', 'c5f284a42b87623c36c491c802f91029a5c1e4fa.json')
        trip = load_sample('wejo/c5f284a42b87623c36c491c802f91029a5c1e4fa.json')
        result = order_directions(directions, trip['coordinates'])
        expected_result = load_result('order_directions', 'c5f284a42b87623c36c491c802f91029a5c1e4fa.json')
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
