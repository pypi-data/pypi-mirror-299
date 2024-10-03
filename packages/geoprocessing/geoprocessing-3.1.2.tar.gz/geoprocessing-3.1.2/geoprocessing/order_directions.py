''' Geoprocessing tool to order the directions in a set of intersections. '''
from typing import Dict, List, NamedTuple
from functools import reduce

from .process_directions import ZoneDirectionData
from .process_intersections import sort_value
from .coords_utils import CoordinatesWithTimestamp, CoordinatesList


class ZoneIntersectionWithDirectionAndOrder(NamedTuple):
    coordinates: CoordinatesWithTimestamp
    action: str
    direction: str
    order: int


ZoneDirectionOrderedData = Dict[str, List[List[ZoneIntersectionWithDirectionAndOrder]]]


def order_directions(directions: ZoneDirectionData,
                     coordinates: CoordinatesList) -> ZoneDirectionOrderedData:
    ''' Adds indexes indicating the order of intersections.

    Args:
        directions  : the result returned by process_directions function.
        coordinates : the coordinates of the trip in their initial order.
    '''
    # merge all intersections into a single list
    merged = reduce(lambda prev, zone: prev + directions[zone], directions, [])
    if len(merged) > 0 and 'timestamp' in merged[0]['coordinates']:
        merged = list({v['coordinates']['timestamp']: v for v in merged}.values())
        merged.sort(key=lambda x: sort_value(x['coordinates']))
        orders = dict((merged[i]['coordinates']['timestamp'], i + 1) for i in range(0, len(merged)))
        for zone in directions:
            for value in directions[zone]:
                value['order'] = orders[value['coordinates']['timestamp']]
    return directions
