import unittest
from unittest.mock import patch, call, MagicMock
import os

from geoprocessing.file_utils import download, download_url, download_shapefile, has_ext, mkdirs

sample_path = os.path.abspath('samples')


class FakeRequest:
    def iter_content(self, _n):
        return ['test']


class TestFileUtils(unittest.TestCase):
    @patch('builtins.open')
    @patch('requests.get', return_value=FakeRequest())
    def test_download_write_file(self, mock_request, mock_open):
        download(sample_path, 'file')
        mock_open.assert_called_once_with('file', 'wb')

    @patch('geoprocessing.file_utils.download')
    def test_download_url_file_exist(self, mock_download):
        url = 'http://server.com/test.txt'
        basename = 'basename'
        os.path.basename = MagicMock(return_value=basename)
        os.path.isfile = MagicMock(return_value=True)

        download_url(sample_path, url)
        mock_download.assert_not_called()

    @patch('geoprocessing.file_utils.download')
    def test_download_url_file_not_exist(self, mock_download):
        url = 'http://server.com/test.txt'
        basename = 'basename'
        os.path.basename = MagicMock(return_value=basename)
        os.path.isfile = MagicMock(return_value=False)

        download_url(sample_path, url)
        mock_download.assert_called_once_with(url, f"{sample_path}/basename")

    @patch('geoprocessing.file_utils.download_url')
    def test_download_shapefile(self, mock_download_url):
        base_url = 'base_url'
        zone = 'zoneId'

        download_shapefile(sample_path, base_url)(zone)
        self.assertEqual(mock_download_url.call_args_list, [
            call(sample_path, base_url + '/' + zone + '.shp'),
            call(sample_path, base_url + '/' + zone + '.dbf'),
            call(sample_path, base_url + '/' + zone + '.shx')
        ])

    def test_has_ext(self):
        self.assertTrue(has_ext('.txt')('test.txt'))
        self.assertFalse(has_ext('.txt')('test.md'))

    @patch('os.makedirs')
    @patch('os.path.isdir')
    def test_mkdirs_exists(self, isdir_mock, makedirs_mock):
        isdir_mock.return_value = True
        mkdirs('test')
        makedirs_mock.assert_not_called()

    @patch('os.makedirs')
    @patch('os.path.isdir')
    def test_mkdirs_not_exist(self, isdir_mock, makedirs_mock):
        isdir_mock.return_value = False
        mkdirs('test')
        makedirs_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
