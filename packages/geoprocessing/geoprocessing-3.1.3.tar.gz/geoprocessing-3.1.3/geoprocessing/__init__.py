from typing import List

from .file_utils import download_shapefile
from .coords_utils import CoordinatesList
from .process_distance import ZoneDistanceData, process_distance
from .process_intersections import ZoneIntersectionData, process_intersections
from .process_directions import ZoneDirectionData, process_directions
from .order_directions import ZoneDirectionOrderedData, order_directions


class Geoprocessing:
    def __init__(self, downloads_path: str, zone_url: str, zones: List[str]):
        '''
        Args:
            downloads_path  : path where the files will be downloaded
            zone_url        : base url of the zone files
            zones           : names of zones that we want to map the coordiantes to
        '''
        self.downloads_path = downloads_path
        self.zones = zones
        # make sure zones shapefile are downloaded
        list(map(download_shapefile(downloads_path, zone_url), zones))

    def process_distance(self,
                         coordinates: CoordinatesList,
                         unit='kilometers',
                         include_coordinates=False) -> ZoneDistanceData:
        ''' Calculate the distance per zone from a set of coordinates.

        Args:
            coordinates         : a set of coordinates (lat, lng, timestamp) defining a trip
            unit                : unit of distance -> "meters", "kilometers" or "miles"
            include_coordinates : include the coordinates per zone if True

        Returns:
            Distance travelled in each zone, with segments found within.
        '''
        return process_distance(self.downloads_path, coordinates, self.zones, unit, include_coordinates)

    def process_intersections(self, coordinates: CoordinatesList) -> ZoneIntersectionData:
        ''' Calculate the intersections of a set of coordinates with the zones.

        Args:
            coordinates: a set of coordinates (lat, lng, timestamp) defining a trip

        Returns:
            Intersetions in each zone, with coordinates of entry/exit.
        '''
        return process_intersections(self.downloads_path, coordinates, self.zones)

    def process_directions(self,
                           intersections: ZoneIntersectionData,
                           coordinates: CoordinatesList) -> ZoneDirectionData:
        ''' Calculate the directions of intersections for a set of coordinates with the zones.

        Args:
            intersections : list of intersections per zone
            coordinates   : a set of coordinates (lat, lng, timestamp) defining a trip

        Returns:
            Intersetions in each zone, with coordinates of entry/exit.
        '''
        return process_directions(self.downloads_path, intersections, self.zones, coordinates)

    def order_directions(self,
                         directions: ZoneDirectionData,
                         coordinates: CoordinatesList) -> ZoneDirectionOrderedData:
        ''' Insert the order of the inersections for a set of coordinates.

        Args:
            directions  : the list of intersections (with direction) per zone.
            coordinates : a set of coordinates (lat, lng, timestamp) defining a trip
        '''
        return order_directions(directions, coordinates)
