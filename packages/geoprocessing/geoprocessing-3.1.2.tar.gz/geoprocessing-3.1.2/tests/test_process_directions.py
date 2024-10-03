import unittest

from .utils import gantry_path, load_result, gantries_files, filter_distances_for_intersections
from geoprocessing.process_directions import process_directions


class TestProcessDirections(unittest.TestCase):
    def test_process_directions(self):
        distances = load_result('process_distance', 'b10B9.json')
        coordinates = filter_distances_for_intersections(distances)
        intersections = load_result('process_intersections', 'b10B9.json')
        result = process_directions(gantry_path, intersections, gantries_files, coordinates)
        expected_result = load_result('process_directions', 'b10B9.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', 'b10DB.json')
        coordinates = filter_distances_for_intersections(distances)
        intersections = load_result('process_intersections', 'b10DB.json')
        result = process_directions(gantry_path, intersections, gantries_files, coordinates)
        expected_result = load_result('process_directions', 'b10DB.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', 'b26DB.json')
        coordinates = filter_distances_for_intersections(distances)
        intersections = load_result('process_intersections', 'b26DB.json')
        result = process_directions(gantry_path, intersections, gantries_files, coordinates)
        expected_result = load_result('process_directions', 'b26DB.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', 'b26F4.json')
        coordinates = filter_distances_for_intersections(distances)
        intersections = load_result('process_intersections', 'b26F4.json')
        result = process_directions(gantry_path, intersections, gantries_files, coordinates)
        expected_result = load_result('process_directions', 'b26F4.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', 'bA8D.json')
        coordinates = filter_distances_for_intersections(distances)
        intersections = load_result('process_intersections', 'bA8D.json')
        result = process_directions(gantry_path, intersections, gantries_files, coordinates)
        expected_result = load_result('process_directions', 'bA8D.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', 'bAD0.json')
        coordinates = filter_distances_for_intersections(distances)
        intersections = load_result('process_intersections', 'bAD0.json')
        result = process_directions(gantry_path, intersections, gantries_files, coordinates)
        expected_result = load_result('process_directions', 'bAD0.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', 'simulated_trip_1.json')
        coordinates = filter_distances_for_intersections(distances)
        intersections = load_result('process_intersections', 'simulated_trip_1.json')
        result = process_directions(gantry_path, intersections, gantries_files, coordinates)
        expected_result = load_result('process_directions', 'simulated_trip_1.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', 'simulated_trip_2.json')
        coordinates = filter_distances_for_intersections(distances)
        intersections = load_result('process_intersections', 'simulated_trip_2.json')
        result = process_directions(gantry_path, intersections, gantries_files, coordinates)
        expected_result = load_result('process_directions', 'simulated_trip_2.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', '75d34b3e1ddc7cf02b76f56fe64cdd8c767e9d7e.json')
        coordinates = filter_distances_for_intersections(distances)
        intersections = load_result('process_intersections', '75d34b3e1ddc7cf02b76f56fe64cdd8c767e9d7e.json')
        result = process_directions(gantry_path, intersections, gantries_files, coordinates)
        expected_result = load_result('process_directions', '75d34b3e1ddc7cf02b76f56fe64cdd8c767e9d7e.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', 'f9451b80157c55043d4ade9ec90721f0f6c4d3f8.json')
        coordinates = filter_distances_for_intersections(distances)
        intersections = load_result('process_intersections', 'f9451b80157c55043d4ade9ec90721f0f6c4d3f8.json')
        result = process_directions(gantry_path, intersections, gantries_files, coordinates)
        expected_result = load_result('process_directions', 'f9451b80157c55043d4ade9ec90721f0f6c4d3f8.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', '4a2397771b3f2518f9e8b81f1db38e2f0e1b5126.json')
        coordinates = filter_distances_for_intersections(distances)
        intersections = load_result('process_intersections', '4a2397771b3f2518f9e8b81f1db38e2f0e1b5126.json')
        result = process_directions(gantry_path, intersections, gantries_files, coordinates)
        expected_result = load_result('process_directions', '4a2397771b3f2518f9e8b81f1db38e2f0e1b5126.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', 'c5f284a42b87623c36c491c802f91029a5c1e4fa.json')
        coordinates = filter_distances_for_intersections(distances)
        intersections = load_result('process_intersections', 'c5f284a42b87623c36c491c802f91029a5c1e4fa.json')
        result = process_directions(gantry_path, intersections, gantries_files, coordinates)
        expected_result = load_result('process_directions', 'c5f284a42b87623c36c491c802f91029a5c1e4fa.json')
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
