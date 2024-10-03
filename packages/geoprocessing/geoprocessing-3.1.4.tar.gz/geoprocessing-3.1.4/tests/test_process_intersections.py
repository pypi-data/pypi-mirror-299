import unittest
from shapely.geometry import shape
import fiona

from .utils import load_sample, load_result, filter_distances_for_intersections
from .utils import main_cordon_file, cordon_files, gantry_path, gantries_files
from geoprocessing.process_intersections import process_intersections, process_geometries_intersections


def get_geometries():
    gantries = [fiona.open(f"{gantry_path}/{x}.shp")[0] for x in gantries_files]

    geometries = []
    counter = 0
    for i in range(0, len(gantries)):
        counter += 1
        geometries.append({
            'geometry': shape(gantries[i]['geometry']),
            'geometry_name': gantries_files[i]
        })
    return geometries


class TestProcessIntersections(unittest.TestCase):
    def test_process_geometries_intersections_single_coordinates(self):
        geometries = get_geometries()

        trip = load_sample('geotab/bA8D.json')
        for geo in geometries:
            geo['tunnel'] = False
        result = process_geometries_intersections(geometries, trip['coordinates'])
        expected_result = load_result('process_geometries_intersections', 'bA8D.json')
        self.assertEqual(result, expected_result)

        trip = load_sample('geotab/bAD0.json')
        result = process_geometries_intersections(geometries, trip['coordinates'])
        expected_result = load_result('process_geometries_intersections', 'bAD0.json')
        self.assertEqual(result, expected_result)

    def test_process_intersections_single_coordinates(self):
        trip = load_sample('sample-process-distance.json')['zones']
        segments = trip[main_cordon_file]['segments']
        # distance = 0.348
        trip = segments[2]['coordinates']

        result = process_intersections(gantry_path, trip, gantries_files)
        # Park Avenue
        self.assertEqual(result['a3aba69d-7c92-4c97-97d8-ed31284ec203'][0], [{
            'coordinates': {'lat': 40.763443, 'lng': -73.9693069}
        }])
        # Madison Avenue
        self.assertEqual(result['9385972e-c32a-4b70-9528-55b9a4da39f2'][0], [{
            'coordinates': {'lat': 40.7635727, 'lng': -73.9713516}
        }])

    def test_process_intersections_multiple_coordinates(self):
        trip = load_sample('sample-process-distance.json')['zones']
        segments = trip[main_cordon_file]['segments']
        # distance = 0.348
        trip1 = segments[2]['coordinates']
        # distance = 1.004
        trip2 = segments[3]['coordinates']

        result = process_intersections(gantry_path, [trip1, trip2], gantries_files)
        self.assertEqual(result['a3aba69d-7c92-4c97-97d8-ed31284ec203'][0], [{
            'coordinates': {'lat': 40.763443, 'lng': -73.9693069}
        }])
        self.assertEqual(result['bf110a80-669e-4b5a-9f8c-718e7b89bdde'][0], [{
            'coordinates': {'lat': 40.7685394, 'lng': -73.9819489}
        }])

    def test_process_intersections_from_process_distance(self):
        distances = load_result('process_distance', 'b10B9.json')
        coordinates = filter_distances_for_intersections(distances, cordon_files)
        result = process_intersections(gantry_path, coordinates, gantries_files)
        expected_result = load_result('process_intersections', 'b10B9.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', 'b10DB.json')
        coordinates = filter_distances_for_intersections(distances, cordon_files)
        result = process_intersections(gantry_path, coordinates, gantries_files)
        expected_result = load_result('process_intersections', 'b10DB.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', 'b26DB.json')
        coordinates = filter_distances_for_intersections(distances, cordon_files)
        result = process_intersections(gantry_path, coordinates, gantries_files)
        expected_result = load_result('process_intersections', 'b26DB.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', 'b26F4.json')
        coordinates = filter_distances_for_intersections(distances, cordon_files)
        result = process_intersections(gantry_path, coordinates, gantries_files)
        expected_result = load_result('process_intersections', 'b26F4.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', 'bA8D.json')
        coordinates = filter_distances_for_intersections(distances, cordon_files)
        result = process_intersections(gantry_path, coordinates, gantries_files)
        expected_result = load_result('process_intersections', 'bA8D.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', 'bAD0.json')
        coordinates = filter_distances_for_intersections(distances, cordon_files)
        result = process_intersections(gantry_path, coordinates, gantries_files)
        expected_result = load_result('process_intersections', 'bAD0.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', 'simulated_trip_1.json')
        coordinates = filter_distances_for_intersections(distances, cordon_files)
        result = process_intersections(gantry_path, coordinates, gantries_files)
        expected_result = load_result('process_intersections', 'simulated_trip_1.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', 'simulated_trip_2.json')
        coordinates = filter_distances_for_intersections(distances, cordon_files)
        result = process_intersections(gantry_path, coordinates, gantries_files)
        expected_result = load_result('process_intersections', 'simulated_trip_2.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', '75d34b3e1ddc7cf02b76f56fe64cdd8c767e9d7e.json')
        coordinates = filter_distances_for_intersections(distances, cordon_files)
        result = process_intersections(gantry_path, coordinates, gantries_files)
        expected_result = load_result('process_intersections', '75d34b3e1ddc7cf02b76f56fe64cdd8c767e9d7e.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', 'f9451b80157c55043d4ade9ec90721f0f6c4d3f8.json')
        coordinates = filter_distances_for_intersections(distances, cordon_files)
        result = process_intersections(gantry_path, coordinates, gantries_files)
        expected_result = load_result('process_intersections', 'f9451b80157c55043d4ade9ec90721f0f6c4d3f8.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', '4a2397771b3f2518f9e8b81f1db38e2f0e1b5126.json')
        coordinates = filter_distances_for_intersections(distances, cordon_files)
        result = process_intersections(gantry_path, coordinates, gantries_files)
        expected_result = load_result('process_intersections', '4a2397771b3f2518f9e8b81f1db38e2f0e1b5126.json')
        self.assertEqual(result, expected_result)

        distances = load_result('process_distance', 'c5f284a42b87623c36c491c802f91029a5c1e4fa.json')
        coordinates = filter_distances_for_intersections(distances, cordon_files)
        result = process_intersections(gantry_path, coordinates, gantries_files)
        expected_result = load_result('process_intersections', 'c5f284a42b87623c36c491c802f91029a5c1e4fa.json')
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
