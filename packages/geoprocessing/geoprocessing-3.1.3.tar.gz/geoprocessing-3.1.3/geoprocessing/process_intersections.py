''' Geoprocessing tool to map a set of coordinates to a set of geographic zones. '''
from typing import Dict, List, NamedTuple
from functools import reduce
from datetime import datetime

from .coords_utils import LineString, CoordinatesWithTimestamp, CoordinatesList, DATETIME_FORMAT
from .coords_utils import reverse_coordinates, coordinates_to_list
from .coords_utils import get_intersections, compute_coords_distance
from .geom_utils import process_geometries


MIN_TRIP_DISTANCE = 150


class ZoneIntersection(NamedTuple):
    coordinates: CoordinatesWithTimestamp


ZoneIntersectionData = Dict[str, List[List[ZoneIntersection]]]


def init_intersection_zone_data(x, y):
    return {
        'entry_direction': x[1],
        'exit_direction': x[2],
        'tunnel': x[3] == 'true',
        'geometry': y
    }


def get_intersection_zones(folder: str, zones: str) -> dict:
    ''' Returns the intersection zones.

    Args:
        folder : path to the folser that contains the intersection zones
        zones  : the name of the shapefile that contains the geometries
    '''
    geometries = []
    geometry_properties = []
    list(map(process_geometries(folder, geometries, geometry_properties, True, True), zones))
    return dict((z, init_intersection_zone_data(x, y)) for x, y, z in zip(geometry_properties, geometries, zones))


def init_boolean_intersections(geometry: dict, coordinates: List[CoordinatesWithTimestamp]):
    coords = list(filter(lambda x: 'added' not in x, coordinates)) if geometry['tunnel'] else coordinates
    trip = LineString(reverse_coordinates(coordinates_to_list(coords))) if len(coords) >= 2 else None
    # which gantries intersect the trip
    return False if trip is None else geometry['geometry'].intersects(trip)


def process_geometries_intersections(geometries: List[dict],
                                     coordinates: List[CoordinatesWithTimestamp]):
    ''' Finds if a trip intersects a number of geometries

    Args:
        geometries  : geometries of interest
        coordinates : the GPS coordinates defining the trip
    '''
    trip = LineString(reverse_coordinates(coordinates_to_list(coordinates)))
    # which ganties intersect the trip
    boolean_intersections = list(map(lambda geo: init_boolean_intersections(geo, coordinates), geometries))
    intersecting_indexes = list(filter(lambda i: boolean_intersections[i], range(0, len(boolean_intersections))))
    intersections = list(map(lambda i: get_intersections(geometries[i]['geometry'], trip), intersecting_indexes))
    intersections = remove_incorrect_intersections(intersections, intersecting_indexes, trip)
    return compose_intersection_dict(geometries, coordinates, intersecting_indexes, intersections)


def remove_incorrect_intersections(intersections: List[List[int]],
                                   intersecting_indexes: List[int],
                                   trip: LineString) -> List[int]:
    ''' Returns a new list with intersection that have not occured because of bad GPS accuracy.

    Args:
        intersections        : a set of indexes that represent the closest points of the trip to the intersection.
        intersecting_indexes : the indexes of intersectiong gantry/intersection zones
        trip                 : the trip of interest
    '''
    # len(intersecting_indexes) == len(intersections)
    def filter_incorrects_at(index):
        return list(filter(lambda i: not is_incorrect(i, trip), intersections[index]))

    return list(map(filter_incorrects_at, range(0, len(intersecting_indexes))))


def compose_intersection_dict(geometries: List[dict],
                              coordinates: List[CoordinatesWithTimestamp],
                              intersecting_indexes: List[int],
                              intersections: List[List[int]]):
    ''' Returns a dictionary of intersections with timestamps.

    Args:
        geometries           : geometries of interest.
        coordinates          : a set of GPS points defining the trip of interest.
        intersecting_indexes : the idexes of geometry object that are intersected by the trip.
        intersections        : the list of points of the trip that are closest to the intersections.
    '''
    def dict_at(index: int):
        return {'coordinates': coordinates[index]}

    def compose_dict_at(index: int):
        i = intersecting_indexes.index(index) if index in intersecting_indexes else -1
        return list(map(dict_at, intersections[i])) if i >= 0 else []

    return dict((geometries[i]['geometry_name'], compose_dict_at(i)) for i in range(0, len(geometries)))


def is_incorrect(index: int, trip: LineString) -> bool:
    ''' Returns True if the intersections is detected only because bad GPS accuracy, False otherwise.

    Args:
        index : the closest point of the trip to the intersection
        trip  : trip of interest
    '''
    coords = list(map(lambda x: trip.coords[x], range(0, len(trip.coords))))
    return compute_coords_distance(coords) < MIN_TRIP_DISTANCE


def remove_tunnel_coords(geometries: dict, coordinates: CoordinatesList) -> CoordinatesList:
    ''' Removes inserted coords from the subtrip for the tunnels.

    Args:
        geometries  : the geometries and the list of associated properties
        coordinates : the list of parts of trips.
    '''
    return list(map(
        lambda i: list(filter(
            lambda x: 'added' not in x, coordinates[i]
        )) if geometries.keys[i]['tunnel'] else coordinates[i],
        range(0, len(coordinates))
    ))


def process_intersections(folder: str,
                          coordinates: CoordinatesList,
                          zones: List[str]) -> ZoneIntersectionData:
    ''' Rerturn intersections between a list of trips and the zones.

    Args:
        folder      : path where the zone shapefiles are located
        coordinates : a set of coordinates (with or without timestamp) defining a trip
        zones       : names of zones that we want to map the coordiantes to
    '''
    coordinates = [coordinates] if isinstance(coordinates[0], dict) else coordinates

    geometries = []
    geometry_names = []
    list(map(process_geometries(folder, geometries, geometry_names, True), zones))
    zones = geometry_names
    intersection_zones = get_intersection_zones(folder, zones)  # necessery to find the tunnels

    geoms = list(map(lambda index: {
        'geometry': geometries[index],
        'geometry_name': geometry_names[index],
        'tunnel': intersection_zones[geometry_names[index]]['tunnel']
    }, range(len(geometries))))

    def merge_data(data, coords):
        res = process_geometries_intersections(geoms, coords)
        return dict((zone, data[zone] + [res[zone]] if res[zone] else data[zone]) for zone in zones)

    return sort_intersections(reduce(merge_data, coordinates, dict((zone, []) for zone in zones)))


def sort_value(coordinates: CoordinatesWithTimestamp):
    return datetime.strptime(coordinates['timestamp'], DATETIME_FORMAT) if 'timestamp' in coordinates else 1


def order_intersections(intersections: List[List[ZoneIntersection]]) -> List[List[ZoneIntersection]]:
    return list(map(lambda inter_list: sorted(inter_list, key=lambda x: sort_value(x['coordinates'])), intersections))


def sort_intersections(intersections: ZoneIntersectionData) -> ZoneIntersectionData:
    return {zone: order_intersections(intersections[zone]) for zone in intersections}
