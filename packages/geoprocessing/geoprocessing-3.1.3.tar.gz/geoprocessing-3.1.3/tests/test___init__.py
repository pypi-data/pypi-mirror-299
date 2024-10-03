import unittest
from unittest.mock import patch
import os

from geoprocessing import Geoprocessing

sample_path = os.path.abspath('samples')


class TestGeoprocessing(unittest.TestCase):
    @patch('geoprocessing.file_utils.download_url')
    def test_init_download_shapefiles(self, mock_download_url):
        Geoprocessing(sample_path, '', ['zone1'])
        self.assertEqual(mock_download_url.call_count, 3)

    @patch('geoprocessing.process_distance')
    @patch('geoprocessing.file_utils.download_url')
    def test_process_distance(self, _m, mock_process_distance):
        zones = ['zone1']
        coordinates = []
        geoproc = Geoprocessing(sample_path, '', zones)

        geoproc.process_distance(coordinates)
        mock_process_distance.assert_called_once_with(sample_path, coordinates, zones, 'kilometers', False)

    @patch('geoprocessing.process_intersections')
    @patch('geoprocessing.file_utils.download_url')
    def test_process_intersections(self, _m, mock_process_intersections):
        zones = ['zone1']
        coordinates = []
        geoproc = Geoprocessing(sample_path, '', zones)

        geoproc.process_intersections(coordinates)
        mock_process_intersections.assert_called_once_with(sample_path, coordinates, zones)

    @patch('geoprocessing.process_directions')
    @patch('geoprocessing.file_utils.download_url')
    def test_process_directions(self, _m, mock_process_directions):
        zones = ['zone1']
        intersections = {}
        coordinates = []
        geoproc = Geoprocessing(sample_path, '', zones)

        geoproc.process_directions(intersections, coordinates)
        mock_process_directions.assert_called_once_with(sample_path, intersections, zones, coordinates)


if __name__ == '__main__':
    unittest.main()
