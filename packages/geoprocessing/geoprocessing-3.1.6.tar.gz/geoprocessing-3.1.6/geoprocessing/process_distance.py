''' Geoprocessing tool to map a set of coordinates to a set of geographic zones. '''
from typing import Dict, List, NamedTuple
from functools import reduce
from itertools import groupby, count
from numpy import array
from time import mktime
from copy import deepcopy
from dateutil.parser import parse
from shapely.geometry import Polygon

from .coords_utils import CoordinatesWithTimestamp, CoordinatesList, Geometry, add_intersection_coordinates
from .coords_utils import compute_distance, process_coordinates, reverse_coordinates, coordinates_to_list
from .coords_utils import NOT_AVAILABLE, same_coordinate
from .geom_utils import process_geometries

COORDS_OUTSIDE_ZONE_KEY = 'no_zone'
SEGMENT_KEY = 'segments'
DISTANCE_KEY = 'distance'
DURATION_KEY = 'duration'
ENTRIES_KEY = 'entries'
EXITS_KEY = 'exits'


class ZoneSegment(NamedTuple):
    distance: float
    duration: float
    coordinates: List[CoordinatesWithTimestamp]


class ZoneDistance(NamedTuple):
    distance: float
    duration: float
    segments: List[ZoneSegment]


ZoneDistanceData = Dict[str, ZoneDistance]


CONVERT_TO_UNIT = {
    'miles': lambda meters: round(meters / 1609.344, 3),
    'kilometers': lambda meters: round(meters / 1000, 3),
    'meters': lambda meters: round(meters, 3)
}


def join_lists(index, matrix):
    ''' Returns a list that contains the N-th elements of the lists in matrix.

    Args:
        index  : index of the elements to turn into list.
        matrix : a list of lists
    '''
    return array(list(map(lambda x: x[index], matrix)))


def diff_time_ms(a: str, b: str) -> float:
    a = mktime(parse(a).timetuple())
    b = mktime(parse(b).timetuple())
    return (a - b) * 1000.0


def valid_time(a: str) -> bool:
    return a != NOT_AVAILABLE


def compute_duration(coordinates: List[CoordinatesWithTimestamp]) -> float:
    a = coordinates[0]
    b = coordinates[-1]
    valid = 'timestamp' in a and valid_time(a['timestamp']) and 'timestamp' in b and valid_time(b['timestamp'])
    return diff_time_ms(b['timestamp'], a['timestamp']) if valid else 0


def compose_segment(segment: List[CoordinatesWithTimestamp],
                    unit: str,
                    include_coordinates: bool,
                    coordinates: List[CoordinatesWithTimestamp]) -> ZoneSegment:
    ''' Returns the segment data: duration, distance, number of entries and exits

    Args:
        segment             : the current segment (part of the trip)
        unit                : unit of distance -> "meters", "kilometers" or "miles"
        include_coordinates : include the coordinates in the result
        coordinates         : list of all coordinates for the current trip
    '''
    has_action = len(segment) > 2 and len(coordinates) > 2
    has_entry = has_action and not same_coordinate(segment[0], coordinates[0])
    has_exit = has_action and not same_coordinate(segment[-1], coordinates[-1])
    res = {
        DISTANCE_KEY: CONVERT_TO_UNIT[unit](
            compute_distance(coordinates_to_list(segment), [[True]*len(segment)])[0]
        ),
        DURATION_KEY: 0 if len(segment) < 2 else compute_duration(segment),
        ENTRIES_KEY: int(has_entry),
        EXITS_KEY: int(has_exit)
    }
    if include_coordinates:
        res['coordinates'] = segment
    return res


def coords_per_zone(coordinates: List[CoordinatesWithTimestamp], arr: List[bool]):
    ''' Splits the coordinates into subset where each subset is a group of consecutive coordinates
        travelled inside a zone of interest.

    Args:
        coordinates : the coordinates of the whole trip.
        arr         : booleans associated to coordinates that show if the N-th coordinate
                      is inside the zone of interest.
    '''
    def group_coords(group):
        return list(map(lambda x: coordinates[x], group))

    in_zone = list(filter(lambda x: arr[x], range(0, len(arr))))
    # group consecutive indexes, then map indexes with coordinates
    return [group_coords(group) for _, group in groupby(in_zone, lambda n, c=count(): n-next(c))]


def zone_split(matrix: List[List[bool]], coordinates: List[CoordinatesWithTimestamp], zones: List[str]):
    ''' Splits coordinates according to the zone appartenance.

    Args:
        matrix      : the matrix computed in the "process_distance" function.
        coordinates : the set of WGS84 coordinates (GPS)
        zones       : "zones" variable from "process_distance" function
    '''
    res = dict((name, []) for name in zones)
    for name, arr in zip(zones, matrix):
        res[name].extend(coords_per_zone(coordinates, arr))
    return res


def process_individual_distance(coordinates: List[CoordinatesWithTimestamp],
                                zones: List[str],
                                geometries: List[Geometry],
                                unit: str,
                                include_coordinates: bool) -> ZoneDistanceData:
    coordinates = add_intersection_coordinates(geometries, coordinates)
    matrix = process_coordinates(geometries, reverse_coordinates(coordinates_to_list(coordinates)), 200, 150)
    splits = zone_split(matrix, coordinates, zones)

    # cumulative_list is a list of N booleans. N is equalt to the length of coordinates
    # N-th boolean is True if the N-th coordinate is inside any geogrpahic zone, False otherwise
    cumulative_list = array(list(map(lambda x: join_lists(x, matrix), range(0, len(matrix[0])))))
    cumulative_list = array(list(map(lambda x: bool(sum(x)), cumulative_list)))
    # flipping cumulative_list so it can be used as it was part of 'matrix'
    # it shows the coordinates inside no any zone
    splits[COORDS_OUTSIDE_ZONE_KEY] = coords_per_zone(coordinates, list(map(lambda x: not x, cumulative_list)))

    def zone_data(zone: str):
        segments = reduce(
            lambda prev, split: prev + [compose_segment(split, unit, include_coordinates, coordinates)],
            splits[zone],
            []
        )
        return {
            SEGMENT_KEY: segments,
            DISTANCE_KEY: reduce(lambda prev, segment: prev + segment[DISTANCE_KEY], segments, 0),
            DURATION_KEY: reduce(lambda prev, segment: prev + segment[DURATION_KEY], segments, 0),
            ENTRIES_KEY: reduce(lambda prev, segment: prev + segment[ENTRIES_KEY], segments, 0),
            EXITS_KEY: reduce(lambda prev, segment: prev + segment[EXITS_KEY], segments, 0)
        }
    return dict((zone, zone_data(zone)) for zone in zones)


def process_distance(folder: str,
                     coordinates: CoordinatesList,
                     zones: List[str],
                     unit: str,
                     include_coordinates=False) -> ZoneDistanceData:
    ''' Compiles the distance of each trip in the zones.

    Args:
        folder              : path where the zone shapefiles are located
        coordinates         : a set of coordinates (including or excluding timestamp) defining a trip
        zones               : names of zones that we want to map the coordinates to
        unit                : unit of distance -> "meters", "kilometers" or "miles"
        include_coordinates : return the coordinates per zone if True, only distances otherwise
    '''
    coordinates = [coordinates] if isinstance(coordinates[0], dict) else coordinates

    geometries = []
    geometry_names = []
    list(map(process_geometries(folder, geometries, geometry_names), zones))
    zones = zones + [COORDS_OUTSIDE_ZONE_KEY]

    # in the case if the congestion zones are described as LineStrings instead of Polygons
    geometries = [g if isinstance(g, Polygon) else Polygon(g) for g in geometries]

    zones_datas = list(map(lambda coords: process_individual_distance(coords,
                                                                      zones,
                                                                      geometries,
                                                                      unit,
                                                                      include_coordinates),
                           coordinates))

    def merge_data(obj, data):
        for zone in zones:
            obj[zone][SEGMENT_KEY].extend(data[zone][SEGMENT_KEY])
            obj[zone][DISTANCE_KEY] += data[zone][DISTANCE_KEY]
            obj[zone][DURATION_KEY] += data[zone][DURATION_KEY]
            obj[zone][ENTRIES_KEY] += data[zone][ENTRIES_KEY]
            obj[zone][EXITS_KEY] += data[zone][EXITS_KEY]
        return obj

    default_value = {SEGMENT_KEY: [], DISTANCE_KEY: 0, DURATION_KEY: 0, ENTRIES_KEY: 0, EXITS_KEY: 0}
    return reduce(merge_data, zones_datas, dict((zone, deepcopy(default_value)) for zone in zones))
