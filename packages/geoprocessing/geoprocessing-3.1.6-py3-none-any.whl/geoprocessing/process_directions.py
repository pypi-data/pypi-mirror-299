''' Geoprocessing tool to determine the directions from a set of intersections. '''
from typing import Dict, List, NamedTuple
from shapely.geometry import Point, LineString, MultiLineString
from functools import reduce

from .process_intersections import ZoneIntersectionData, ZoneIntersection, get_intersection_zones
from .coords_utils import CoordinatesWithTimestamp, CoordinatesList, PRECISION_ERROR

ACTIONS = {
    'entry': 'Entry',
    'exit': 'Exit',
    'pass-through': 'PassThrough',
    'ignore': 'Pass Trough a Tunnel'
}

DIRECTION_FROM_ACTION = {
    ACTIONS['entry']: lambda zone: zone['entry_direction'],
    ACTIONS['exit']: lambda zone: zone['exit_direction'],
    # the case of PassThrough
    # does it metter to have a real direction in this case?
    ACTIONS['pass-through']: lambda zone: 'N/A',
    ACTIONS['ignore']: lambda zone: 'N/A'
}


class ZoneIntersectionWithDirection(NamedTuple):
    coordinates: CoordinatesWithTimestamp
    action: str
    direction: str


ZoneDirectionData = Dict[str, List[List[ZoneIntersectionWithDirection]]]


def process_directions(folder: str,
                       intersections: ZoneIntersectionData,
                       zones: List[str],
                       coordinates: CoordinatesList) -> ZoneDirectionData:
    ''' Determines the directions and actions for every intersection.

    Args:
        folder          : path where the zone shapefiles of intersection zones are located
        coordinates     : list of coordinates for each trip
        zones           : list of zones used to find the intersections
        intersections   : dictionary with a set of coordinates and timestamps associated to zone names.

    Note:
        coordinates is the output of the "process_distance" filtered by segments of interest
        intersections is the output of the "process_intersections"
    '''
    intersection_zones = get_intersection_zones(folder, zones)
    intersections = dict((
        zone,
        add_directions(intersections[zone], intersection_zones[zone], coordinates)
    ) for zone in intersections.keys())
    return {k: remove_pass_through_tunnel(v) for k, v in intersections.items()}


def remove_pass_through_tunnel(intersections: ZoneIntersectionData) -> ZoneIntersectionData:
    def filter_ignore(intersection):
        return list(filter(lambda inter: inter['action'] != ACTIONS['ignore'], intersection))

    return reduce(lambda res, intersection: res + filter_ignore(intersection), intersections, [])


def get_action(zone, segment, first_intersection: bool, last_intersection: bool):
    ''' Finds out the action commited during the intersection.

    Args:
        zone               : the intersection zone
        segment            : part of the trip that is inside the conjestion zone
        first_intersection : True if the observed intersection is at the begining of the segment, False otherwise
        last_intersection  : True if the observed intersection is at the end of the segment, False otherwise
    '''
    if first_intersection and zone['geometry'].contains(Point(segment[0])):
        return 'entry'
    elif last_intersection and zone['geometry'].contains(Point(segment[-1])):
        return 'exit'
    return 'ignore' if zone['tunnel'] else 'pass-through'


def complete_intersections(zone, segment, intersections: List[ZoneIntersection], index: int, limit: int):
    action = get_action(zone, segment, index == 0, index == limit - 1)
    return {**intersections[index], **get_action_direction(zone, action)}


def add_directions(intersections: List[List[ZoneIntersection]], zone: dict, coordinates: CoordinatesList):
    ''' Adds the values of action and direction to the intersection.

    Args:
        intersections : the intersection that should be completed.
        zone          : the intersected geometry and its parameters.
        coordinates   : the coordinates of the trip that intersects the zone at intersection.
    '''
    def add_directions_segment(inter_set: List[ZoneIntersection]):
        # all the intersections in inter_set are from the same segment
        segment = find_matching_coordinates(inter_set[0]['coordinates'], coordinates, zone['tunnel'])

        trip = LineString(segment)
        inters = zone['geometry'].intersection(trip)

        # Handle MultiLineString or LineString
        if isinstance(inters, LineString):
            inters = [inters]
        elif isinstance(inters, MultiLineString):
            inters = list(inters.geoms)  # Use .geoms to access the individual LineString objects

        enum_inters = list(enumerate(inters))

        # this should never happend, but it always a good practice to make the assertion
        assert len(inters) == len(inter_set), 'The number of intersections detected at process_directions \
                                                is not the same as the number of intersections detected at \
                                                process_intersections'

        return list(
            map(lambda args: complete_intersections(zone, segment, inter_set, args[0], len(enum_inters)), enum_inters)
        )

    return list(map(add_directions_segment, intersections))


def get_action_direction(zone, action_key):
    action = ACTIONS[action_key]
    direction = DIRECTION_FROM_ACTION[action](zone)
    return {'action': action, 'direction': direction}


def is_inside(zone: dict, coord: (float, float)) -> bool:
    point = Point(coord)
    return zone['geometry'].contains(point) or zone['geometry'].distance(point) < PRECISION_ERROR


def find_matching_coordinates(coordinates: CoordinatesWithTimestamp, segments: CoordinatesList, tunnel=False) -> list:
    segments = list(filter(lambda segment: coordinates in segment, segments))
    if len(segments) != 1:
        raise ValueError('The number of segments should be always equal to 1.')

    segment = list(filter(lambda x: 'added' not in x, segments[0])) if tunnel else segments[0]
    return list(map(lambda x: (x['lng'], x['lat']), segment))
