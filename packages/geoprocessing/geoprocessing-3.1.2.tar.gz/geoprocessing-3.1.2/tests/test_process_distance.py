import unittest

from .utils import sample_path, cordon_path, load_sample, load_result, cordon_files
from geoprocessing.process_distance import process_distance, COORDS_OUTSIDE_ZONE_KEY


class TestProcessDistance(unittest.TestCase):
    def test_process_distance_single_coordinates_zones(self):
        sample = load_sample('sample.json')
        coords = sample['coords']
        result = process_distance(sample_path, coords, sample['zones'], 'kilometers', True)
        self.assertEqual(2, len(result))
        self.assertEqual(1, len(result['sample']['segments']))
        self.assertEqual(1, len(result[COORDS_OUTSIDE_ZONE_KEY]['segments']))
        self.assertTrue('added' in coords[2])
        self.assertEqual([coords[3], coords[4]], result['sample']['segments'][0]['coordinates'][1:])
        self.assertEqual(90000, result['sample']['duration'])
        self.assertEqual([coords[0], coords[1]], result[COORDS_OUTSIDE_ZONE_KEY]['segments'][0]['coordinates'])
        self.assertEqual(60000, result[COORDS_OUTSIDE_ZONE_KEY]['duration'])

    def test_process_distance_single_coordinates_zones_no_timestamps(self):
        sample = load_sample('sample.json')
        coords = sample['coords']
        # remove the timestamp from the coordinates
        coords = list(map(lambda x: {'lat': x['lat'], 'lng': x['lng']}, coords))
        result = process_distance(sample_path, coords, sample['zones'], 'kilometers', True)
        self.assertEqual([coords[3], coords[4]], result['sample']['segments'][0]['coordinates'][1:])
        self.assertEqual(0, result['sample']['duration'])
        self.assertEqual([coords[0], coords[1]], result[COORDS_OUTSIDE_ZONE_KEY]['segments'][0]['coordinates'])
        self.assertEqual(0, result[COORDS_OUTSIDE_ZONE_KEY]['duration'])

    def test_process_distance_single_no_coordinates(self):
        sample = load_sample('sample.json')
        result = process_distance(sample_path, sample['coords'], sample['zones'], 'kilometers')
        self.assertFalse('coordinates' in result['sample']['segments'][0])
        self.assertFalse('coordinates' in result[COORDS_OUTSIDE_ZONE_KEY]['segments'][0])

    def test_process_distance_single_coordinates_distance_meters(self):
        sample = load_sample('sample.json')
        result = process_distance(sample_path, sample['coords'], sample['zones'], 'meters')
        self.assertEqual(515.396, result['sample']['distance'])
        self.assertEqual(349.246, result[COORDS_OUTSIDE_ZONE_KEY]['distance'])

    def test_process_distance_single_coordinates_distance_kilometers(self):
        sample = load_sample('sample.json')
        result = process_distance(sample_path, sample['coords'], sample['zones'], 'kilometers')
        self.assertEqual(0.515, result['sample']['distance'])
        self.assertEqual(0.349, result[COORDS_OUTSIDE_ZONE_KEY]['distance'])

    def test_process_distance_single_coordinates_distance_miles(self):
        sample = load_sample('sample.json')
        result = process_distance(sample_path, sample['coords'], sample['zones'], 'miles')
        self.assertEqual(0.32, result['sample']['distance'])
        self.assertEqual(0.217, result[COORDS_OUTSIDE_ZONE_KEY]['distance'])

    def test_process_distance_multiple_coordinates_zones(self):
        sample = load_sample('sample.json')
        coords = sample['coords']
        result = process_distance(sample_path, [coords, coords], sample['zones'], 'kilometers', True)
        self.assertEqual(2, len(result))
        self.assertEqual(2, len(result['sample']['segments']))
        self.assertEqual(2, len(result[COORDS_OUTSIDE_ZONE_KEY]['segments']))
        self.assertEqual([coords[4], coords[5]], result['sample']['segments'][0]['coordinates'][1:])
        self.assertEqual([coords[4], coords[5]], result['sample']['segments'][1]['coordinates'][2:])
        self.assertEqual(90000*2, result['sample']['duration'])
        self.assertEqual([coords[0], coords[1]], result[COORDS_OUTSIDE_ZONE_KEY]['segments'][0]['coordinates'])
        self.assertEqual([coords[0], coords[1]], result[COORDS_OUTSIDE_ZONE_KEY]['segments'][1]['coordinates'])
        self.assertEqual(60000*2, result[COORDS_OUTSIDE_ZONE_KEY]['duration'])

    def test_process_distance_multiple_coordinates_distance_miles(self):
        sample = load_sample('sample.json')
        coords = sample['coords']
        result = process_distance(sample_path, [coords, coords], sample['zones'], 'miles')
        self.assertEqual(0.32 * 2, result['sample']['distance'])
        self.assertEqual(0.217 * 2, result[COORDS_OUTSIDE_ZONE_KEY]['distance'])

    def test_process_distance(self):
        trip_id = 'b10B9.json'
        trip = load_sample(f"geotab/{trip_id}")
        result = process_distance(cordon_path, trip['coordinates'], cordon_files, 'miles', True)
        expected_result = load_result('process_distance', trip_id)
        self.assertEqual(result, expected_result)

        trip_id = 'b10DB.json'
        trip = load_sample(f"geotab/{trip_id}")
        result = process_distance(cordon_path, trip['coordinates'], cordon_files, 'miles', True)
        expected_result = load_result('process_distance', trip_id)
        self.assertEqual(result, expected_result)

        trip_id = 'b26DB.json'
        trip = load_sample(f"geotab/{trip_id}")
        result = process_distance(cordon_path, trip['coordinates'], cordon_files, 'miles', True)
        expected_result = load_result('process_distance', trip_id)
        self.assertEqual(result, expected_result)

        trip_id = 'b26F4.json'
        trip = load_sample(f"geotab/{trip_id}")
        result = process_distance(cordon_path, trip['coordinates'], cordon_files, 'miles', True)
        expected_result = load_result('process_distance', trip_id)
        self.assertEqual(result, expected_result)

        trip_id = 'bA8D.json'
        trip = load_sample(f"geotab/{trip_id}")
        result = process_distance(cordon_path, trip['coordinates'], cordon_files, 'miles', True)
        expected_result = load_result('process_distance', trip_id)
        self.assertEqual(result, expected_result)

        trip_id = 'bAD0.json'
        trip = load_sample(f"geotab/{trip_id}")
        result = process_distance(cordon_path, trip['coordinates'], cordon_files, 'miles', True)
        expected_result = load_result('process_distance', trip_id)
        self.assertEqual(result, expected_result)

        # a U-turn trip that enter and exits through Park Avenue
        trip_id = 'simulated_trip_1.json'
        trip = load_sample(trip_id)
        result = process_distance(cordon_path, trip['coordinates'], cordon_files, 'miles', True)
        expected_result = load_result('process_distance', trip_id)
        self.assertEqual(result, expected_result)

        # an entry -> pass-through -> exit trip through Broadway
        trip_id = 'simulated_trip_2.json'
        trip = load_sample(trip_id)
        result = process_distance(cordon_path, trip['coordinates'], cordon_files, 'miles', True)
        expected_result = load_result('process_distance', trip_id)
        self.assertEqual(result, expected_result)

        trip_id = '75d34b3e1ddc7cf02b76f56fe64cdd8c767e9d7e.json'
        trip = load_sample(f"wejo/{trip_id}")
        result = process_distance(cordon_path, trip['coordinates'], cordon_files, 'miles', True)
        expected_result = load_result('process_distance', '75d34b3e1ddc7cf02b76f56fe64cdd8c767e9d7e.json')
        self.assertEqual(result, expected_result)

        trip_id = 'f9451b80157c55043d4ade9ec90721f0f6c4d3f8.json'
        trip = load_sample(f"wejo/{trip_id}")
        result = process_distance(cordon_path, trip['coordinates'], cordon_files, 'miles', True)
        expected_result = load_result('process_distance', trip_id)
        self.assertEqual(result, expected_result)

        trip_id = '4a2397771b3f2518f9e8b81f1db38e2f0e1b5126.json'
        trip = load_sample(f"wejo/{trip_id}")
        result = process_distance(cordon_path, trip['coordinates'], cordon_files, 'miles', True)
        expected_result = load_result('process_distance', trip_id)
        self.assertEqual(result, expected_result)

        trip_id = 'c5f284a42b87623c36c491c802f91029a5c1e4fa.json'
        trip = load_sample(f"wejo/{trip_id}")
        result = process_distance(cordon_path, trip['coordinates'], cordon_files, 'miles', True)
        expected_result = load_result('process_distance', trip_id)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
