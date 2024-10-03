import unittest
import os
import json
import pickle

from geoprocessing.coords_utils import process_coordinates, compute_distance


sample_path = os.path.abspath('samples')


class TestProcessCoordinates(unittest.TestCase):
    def test_process_coordinates(self):
        with open(f"{sample_path}/seattle_roads.ls", 'rb') as f:
            seattle_roads = pickle.load(f)

        with open(f"{sample_path}/seattle_data.json") as f:
            json_file = json.load(f)
            trip = json_file['trip']

        with open(f"{sample_path}/seattle_road_matrix.pkl", 'rb') as f:
            expected = pickle.load(f)

        result_matrix = process_coordinates(seattle_roads, trip, 200, 150)
        self.assertEqual(expected, result_matrix)

    def test_compute_distance(self):
        with open(f"{sample_path}/seattle_data.json") as f:
            json_file = json.load(f)
            trip = json_file['trip']
            expected = json_file['distances']

        with open(f"{sample_path}/seattle_road_matrix.pkl", 'rb') as f:
            matrix = pickle.load(f)

        distances = compute_distance(list(map(lambda x: [x[1], x[0]], trip)), matrix)
        self.assertEqual(expected, distances)


if __name__ == '__main__':
    unittest.main()
