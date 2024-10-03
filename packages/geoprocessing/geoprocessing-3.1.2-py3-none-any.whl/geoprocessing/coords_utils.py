from typing import List, Union, NamedTuple
from shapely.geometry import Point, LineString, MultiLineString, Polygon, MultiPolygon, LinearRing, GeometryCollection
import shapely.vectorized
import numpy
from numpy import array
from dateutil.parser import parse
from math import radians, cos, sin, asin, sqrt
from functools import reduce

from .geom_utils import is_line, is_polygon

Num = Union[int, float]
Coordinates = List[List[float]]
Geometry = Union[LineString, MultiLineString, Polygon, MultiPolygon]

PRECISION_ERROR = pow(10, -10)
NOT_AVAILABLE = 'N/A'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


class CoordinatesWithTimestamp(NamedTuple):
    lat: float
    lng: float
    timestamp: any


CoordinatesList = Union[List[CoordinatesWithTimestamp], List[List[CoordinatesWithTimestamp]]]


def next_available_timestamp(coordinates: List[CoordinatesWithTimestamp]) -> str:
    return next((obj['timestamp'] for obj in coordinates if obj['timestamp'] != NOT_AVAILABLE), NOT_AVAILABLE)


def median_time(time1: str, time2: str):
    time1 = parse(time1)
    time2 = parse(time2)
    time = time1 + (time2 - time1) / 2
    return time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+'Z'


def fix_timestamps(coordinates: List[CoordinatesWithTimestamp]) -> List[CoordinatesWithTimestamp]:
    ''' The add_intersection_coordinates function inserts coordinates with timestamps "N/A". In the case
        if we need timestamps, we need to fix them first.

    Args:
        coordinates : coordinates of the trip.
    '''
    def fix_timestamp_at(index: int):
        before = next_available_timestamp(reversed(coordinates[:index]))
        after = next_available_timestamp(coordinates[index:])
        coordinates[index]['timestamp'] = median_time(
            before, after) if before != NOT_AVAILABLE and after != NOT_AVAILABLE else NOT_AVAILABLE
        return coordinates[index]

    return list(map(
        lambda i: fix_timestamp_at(i) if coordinates[i]['timestamp'] == NOT_AVAILABLE else coordinates[i],
        range(0, len(coordinates))
    ))


def insert_coordinates(coordinates: List[CoordinatesWithTimestamp],
                       new_coordinate: List[float],
                       near_coordinate: CoordinatesWithTimestamp,
                       before: bool):
    ''' Insert a new coordinates near a coordinate that already exists in the list of coordinates.

    Args:
        coordinates       : the list of all GPS cordiantes of the trip.
        new_coordinate    : the new coordinates to insert in the list of coordinates.
        near_coordinate   : the coordinate near which the new coordinate should be inserted.
        before            : True if the new coordinate should be inserted chronologically before the near coordinate,
                            False otherwise.
    '''
    idx = coordinates_index(coordinates, near_coordinate, before)
    if idx >= 0:
        coordinate = {'lat': new_coordinate[1], 'lng': new_coordinate[0]}
        if 'timestamp' in coordinates[0]:
            coordinate['timestamp'] = NOT_AVAILABLE
        # we should ignore this points in case of tunnels
        coordinate['added'] = True
        coordinates.insert(idx, coordinate)
    return idx


def find_point(point: Point,
               intersection: LineString,
               coordinates: List[CoordinatesWithTimestamp],
               index: int,
               first: bool) -> CoordinatesWithTimestamp:
    ''' Finding the point after so that the first intersection point could take its position.

    Args:
        point        : the point of intersection.
        intersection : the intersection of the trip with a zone.
        coordinates  : the list of all coordinates.
        index        : the index of the previously inserted point.
        first        : True if it is the first point of the intersection, False otherwise.

    Note:
        The new point should be inderted between the two closest points starting from the index,
        and should take the median timestamp.
    '''
    if len(intersection.coords) > 2:
        coordinate = intersection.coords[1] if first else intersection.coords[-2]
        return {'lat': coordinate[1], 'lng': coordinate[0]}

    points = list(map(lambda p: Point(p['lng'], p['lat']), coordinates))
    for i in range(index, len(coordinates)):
        if points[i].distance(point) < points[i].distance(points[i+1]):
            # if the first is True, than the new point should be inserted after the found point,
            # else it should be inserted before the found point.
            return coordinates[i+int(first)]


def add_intersection_with_line(geometry: Geometry, coordinates: List[CoordinatesWithTimestamp]):
    def process_intersection(index, intersection):
        insertion_index = 0
        coordinate = intersection.coords[0]
        point = Point(coordinate)
        if geometry.exterior.distance(point) < PRECISION_ERROR:
            near_coordinate = find_point(point, intersection, coordinates, index, first=True)
            insertion_index = insert_coordinates(coordinates, coordinate, near_coordinate, before=True)

        coordinate = intersection.coords[-1]
        point = Point(coordinate)
        if geometry.exterior.distance(point) < PRECISION_ERROR:
            near_coordinate = find_point(point, intersection, coordinates, index, first=False)
            insertion_index = insert_coordinates(coordinates, coordinate, near_coordinate, before=False)

        return insertion_index
    return process_intersection


def add_intersection(geometry: Geometry, trip, coordinates: List[CoordinatesWithTimestamp]):
    intersection = geometry.intersection(trip)

    lines = extract_valid_lines(intersection)

    if lines:
        reduce(add_intersection_with_line(geometry, coordinates), lines, 0)


def extract_valid_lines(intersection: Geometry) -> List[LineString]:
    ''' Extract valid LineString objects with coordinates from the intersection. '''
    if isinstance(intersection, LineString):
        return [intersection] if len(intersection.coords) > 0 else []
    elif isinstance(intersection, MultiLineString):
        return [line for line in intersection.geoms if len(line.coords) > 0]
    elif isinstance(intersection, GeometryCollection):
        return [geom for geom in intersection.geoms if isinstance(geom, LineString) and len(geom.coords) > 0]
    else:
        return []


def add_intersection_coordinates(geometries: List[Geometry], coordinates: List[CoordinatesWithTimestamp]):
    ''' Adds coordinates at the places where the trip intersects with the congestion zone.

    Args:
        geometries  : list of the geometries representing the congestion zone.
        coordinates : the coordinates of the trip.
    '''
    points = reverse_coordinates(coordinates_to_list(coordinates))
    trip = LineString(points)

    # Apply the add_intersection function to each geometry
    list(map(lambda geometry: add_intersection(geometry, trip, coordinates), geometries))

    # Fix timestamps if they are present in the coordinates
    return fix_timestamps(coordinates) if 'timestamp' in coordinates[0] else coordinates


def process_coordinates(geometries: List[Geometry], points: Coordinates, threshold: Num, fechet_threshold: Num):
    ps = [Point(p) for p in points]
    return list(map(process_geometry_coordinates(ps, points, threshold, fechet_threshold), geometries))


def get_intersections(geometry: Geometry, trip: Geometry) -> List[int]:
    ''' Returns the points of the trip that are closest to the intersections between geometry and trip.

    Args:
        geometry : polygon that indicates the intersection zone.
        trip     : LineString that represents the trip.
    '''
    intersection = geometry.intersection(trip)

    # Handle MultiLineString or LineString
    if isinstance(intersection, LineString):
        intersections = [intersection]
    elif isinstance(intersection, MultiLineString):
        intersections = list(intersection.geoms)  # Extract individual LineStrings
    else:
        intersections = [intersection]

    return list(map(lambda inter: find_closest_point_index(trip, inter), intersections))


def find_closest_point_index(trip: LineString, intersection: Point) -> int:
    ''' Find the closest index of the coordinate of the trip to the givent intersection.

    Args:
        trip         : trip of interest
        intersection : intersection of interest
    '''
    intersection = Point(intersection.coords[0])
    distances = list(map(lambda coord: Point(coord).distance(intersection), trip.coords[1:]))
    min_distance = numpy.amin(distances)
    min_distance_index = numpy.where(distances == min_distance)[0][0]
    return int(min_distance_index)


def fix_close_coordinates(linearring: LinearRing, array: List[bool], coords: Coordinates) -> List[bool]:
    ''' Flags the points of the border as the points that are in a zone, if they are flages as not in the zone
        only because of a precison error.

    Args:
        linearring : the shape of the perimeter of a zone.
        array      : a list indicating if a point is inside the zone or not.
        coords     : the coords of a trip.
    '''
    return list(map(lambda i: array[i] or linearring.distance(Point(coords[i])) < PRECISION_ERROR,
                    range(0, len(array))))


def process_geometry_coordinates(points: List[Point], coords: Coordinates, threshold: Num, fechet_threshold: Num):
    def process(geom: Geometry) -> List[bool]:
        if is_polygon(geom):
            # TODO what if we only use intersections
            xs = array(list(map(lambda x: x[0], coords)))
            ys = array(list(map(lambda x: x[1], coords)))
            # shapely.vectorized.contains returns numpy.array but we expect a list
            res = shapely.vectorized.contains(geom, xs, ys).tolist()
            linearring = geom.exterior
            return fix_close_coordinates(linearring, res, coords)
        elif is_line(geom):
            return fechet(geom, points, threshold, fechet_threshold)
    return process


def compute_distance(points: Coordinates, matrix: List[List[bool]]) -> List[float]:
    ''' Computes the total distances inside a zone/close to a road.

    Args:
        points : coordinates of the trip
        matrix : matrix returned by the function process_coordinates

    Returns:
        A list of floats where each float represents the total distance
        in meters travelled during the trip (points) inside a geometry
        or close to a geometry.
    '''
    return list(map(lambda arr: compute_coords_distance(points, arr), matrix))


def compute_coords_distance(points: Coordinates, arr: List[bool] = []):
    arr = arr if len(arr) > 0 else len(points)*[True]

    def distance_segment(i):
        return haversine(points[i][0], points[i][1], points[i+1][0], points[i+1][1]) if arr[i] else 0.0

    return reduce(lambda prev, i: prev + distance_segment(i), range(0, len(points)-1), 0.0)


def haversine(lat1: float, lon1: float, lat2: float, lon2: float):
    ''' Computes the great circle distance between two points on the earth

    Args:
        lat1 : latitude of the first point
        lon1 : longitude of the first point
        lat2 : latitude of the second point
        lon2 : longitude of the second point
    Returns:
        distance between the 2 points in decimal degrees
    '''
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6366557  # Radius of earth in meters at latitude of seattle
    return c * r


def closest_point(point: Point, road: Geometry):
    return road.interpolate(road.project(point)).coords[0]


def closest_points(points: List, road: Geometry):
    ''' Get the closest points of the road to a trip.

    Args:
        points  : points that represent a trip.
        road    : curve that describs the road.
    Returns
        array of closest points
    '''
    # coordinates of the closest points on the road to p
    closest_points = list(map(lambda p: closest_point(Point(p), road), points))
    return [
        list(map(lambda x: x[0], closest_points)),
        list(map(lambda x: x[1], closest_points))
    ]


def distance_to_point(road: Geometry):
    def distance(point: Point):
        # coordinates of the closest point on the road to p
        closest = closest_point(point, road)
        return haversine(closest[1], closest[0], point.coords[0][1], point.coords[0][0])
    return distance


def distance_to_points(road: Geometry, points: List[Point]):
    ''' Get the distance between a curve and an array of GPS points

    Args:
        road    : a shapely object representing a road
        points  : a trip made by a driver
    Returns
        array of distances in meters
    '''
    return list(map(distance_to_point(road), points))


def _rep(road_points: Coordinates, trip_points: Coordinates, begin: int, end: int, threshold=0.15) -> bool:
    rps = [road_points[0][begin:end], road_points[1][begin:end]]
    tps = [trip_points[0][begin:end], trip_points[1][begin:end]]
    road_corr = numpy.corrcoef(rps)[0][1]
    trip_corr = numpy.corrcoef(tps)[0][1]
    return abs(road_corr - trip_corr) < threshold


def correlation(road_points: Coordinates, trip_points: Coordinates) -> bool:
    ''' Checks if two set of points (which represent a segment) have a similar corelation.
    If two points have the same correlation, there is a big chance that the trip was made on the road.

    Note:
        https://en.wikipedia.org/wiki/Pearson_correlation_coefficient

    Args:
        road_points : represents the GPS points that define the road.
        trip_points : represents the GPS points of a trip.
    Returns
        True if two set of points have a similar corelation, False otherwise
    '''
    road_points = array(road_points)
    trip_points = array(trip_points)
    return _rep(road_points, trip_points, 0, len(trip_points)) or (
        len(road_points[0]) > 30 and _rep(road_points, trip_points, 0, -15)
    ) or (
        len(road_points[0]) > 30 and _rep(road_points, trip_points, 15, len(road_points[0]))
    ) or (
        len(road_points[0]) > 45 and _rep(road_points, trip_points, 15, -15)
    )


def object_fct(distances: List[float], threshold: Num, line: Geometry, points: List[Point]) -> bool:
    ''' The objective function of the algorithm. Computes whether the average distance of the points
    from the road is smaller than the treshold and the shapes of the road and the segment are similar.

    Args:
        distances   : the distances between two lines.
        threshold  : defines the threeeshold for the distances between the lines.

    Returns:
        True if distances is an array of distances between two segments
        is smaller than a threshold and their correlations are similar,
        False otherwise.
    '''
    ratio = sum(distances) / len(distances)
    ps = [
        list(map(lambda x: x.coords[0][0], points)),
        list(map(lambda x: x.coords[0][1], points))
    ]
    return ratio < threshold and correlation(closest_points(points, line), ps)


def fechet(line: Geometry, points: List[Point], threshold: Num, fechet_threshold: Num) -> List[bool]:
    ''' Computes if the set of points is close enough to a Geometry.

    Args:
        points           : a set of points that could form a segment.
        line             : a road that we in want to know the segment is close enough.
        threshold        : the max distance of between the points and the road for the
                           points to be considered as a segment.
        fechet_threshold : the max distance of points from the road to be considered as
                           part of a segment

    Return:
        Each Nth boolean values represents if the Nth points is part of a segment or not.
    '''
    def fechet_subset(distances, subset):
        return [
            object_fct(list(map(lambda x: distances[x], subset)),
                       fechet_threshold,
                       line,
                       list(map(lambda x: points[x], subset)))
        ] * len(subset) if isinstance(subset, list) else [False]

    distances = distance_to_points(line, points)
    pass_threshold = list(map(lambda dist: dist < threshold, distances))
    subsets = make_subsets(pass_threshold)

    return list(reduce(lambda prev, subset: prev + fechet_subset(distances, subset), subsets, []))


def make_subsets(booleans: List[bool]) -> List[Union[List[int], None]]:
    ''' Returns a list of subsets, where each subset forms a potential segment. A subset is a list of indexes.

    Note:
        There is a little hack with None values in the list - if the points is not close to
        the current geometry, we will insert a None that will be used in the fechet function.

    Args:
        booleans : a list of booleans where Nth boolean is True if Nth points is potentially in a segment.

    Return:
        Each inner list in the resulting list is a list containing points of a potential segment.
    '''
    subset = []
    result = []
    for b in range(0, len(booleans)):
        if booleans[b]:
            subset.append(b)
            continue
        elif subset:
            result.append(subset)
            subset = []
        result.append(None)
    return result


def coordinates_index(coordinates: List[CoordinatesWithTimestamp],
                      coordinate: CoordinatesWithTimestamp,
                      before: bool) -> int:
    ''' Returns the potision where a new coordinates should be inserted in the list of all coordinates.

    Args:
        coordinates : list of the coordinates of the trip.
        coordinate  : the coordinate to insert into the list of coordinates.
        before      : True if the new coordinate should be placed before a group of identical coordinates,
                      False otherwise.

    Note:
        The problem with finding a position to insert the new coordinate is that there are points that have
        the same latitude and longitude but different timestamps. To place the new coordinate without destroying
        the order of points we use the before parameter.
    '''
    index = find_coordinates_index(coordinates, coordinate)
    return index if before else index + find_last_coordinates_index(coordinates[index+1:], coordinate, 1)


def find_last_coordinates_index(coordinates: List[CoordinatesWithTimestamp],
                                coordinate: CoordinatesWithTimestamp,
                                start: int) -> int:
    idx = find_coordinates_index(coordinates, coordinate)
    return start if idx is None else find_last_coordinates_index(coordinates[idx+1:], coordinate, start+idx+1)


def find_coordinates_index(coordinates: List[CoordinatesWithTimestamp], coordinate: CoordinatesWithTimestamp) -> int:
    return next((i for (i, d) in enumerate(coordinates) if same_coordinate(d, coordinate)), None)


def same_coordinate(coord1: CoordinatesWithTimestamp, coord2: CoordinatesWithTimestamp):
    return coord1['lat'] == coord2['lat'] and coord1['lng'] == coord2['lng']


def reverse_coordinates(coordinates: Coordinates) -> Coordinates:
    return list(map(lambda x: [x[1], x[0]], coordinates))


def coordinates_to_list(coordinates: List[CoordinatesWithTimestamp]) -> Coordinates:
    return list(map(lambda x: [x['lat'], x['lng']], coordinates))
