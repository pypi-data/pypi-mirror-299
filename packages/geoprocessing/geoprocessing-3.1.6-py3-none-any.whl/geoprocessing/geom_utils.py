from typing import Union, List
import logging
import fiona
from shapely.geometry import shape, LineString, MultiLineString, Polygon, MultiPolygon
from shapely.ops import unary_union


def is_polygon(geom: Union[Polygon, MultiPolygon]) -> bool:
    return type(geom) in (Polygon, MultiPolygon)


def is_line(geom: Union[LineString, MultiLineString]) -> bool:
    return type(geom) in (LineString, MultiLineString)


def process_zone(folder: str, zone: str, union: bool):
    ''' Extracts geometries from shapefiles.

    Args:
        folder : the folder that contains shapefiles.
        zone   : the name of the shapefile to process.

    Note:
        This function is supposed to be called only from process_distance
        and handles the case of LineStrings (roads) and Polygons (conjgestion zones).
    '''
    logging.info(f"process_zone: {zone}")
    collection = fiona.open(f"{folder}/{zone}.shp")
    collection = list(filter(lambda x: x['geometry'], collection))  # removing all object with no geometries
    shapes = list(map(lambda x: shape(x['geometry']), collection))

    # the case if a road is described with multiple LineStrings
    # it is possible that we will use one shapefile for many roads (the last line) -> not recomended
    # seems better to use a shapefile per road
    if collection[0]['geometry']['type'] == 'LineString':
        # all the objects in one collections are suppose to have the same keys in the 'properties' value
        return (shapes, list(map(lambda x: x['properties']['name'], collection)))

    #  the case if a zone is described using many a set of Polygons
    else:  # Polygon, MultiPolygon
        return ([unary_union(shapes)], [zone])


def process_zone_with_directions(folder: str, zone: str):
    ''' Extracts geometries from shapefiles.

    Args:
        folder : the folder that contains shapefiles.
        zone   : the name of the shapefile to process.

    Note:
        This function is supposed to be called from process_intersections and process_directions
        and handles the case of a shapefile containing many separeted Polygons.
    '''
    logging.info(f"process_zone_with_directions: {zone}")
    collection = fiona.open(f"{folder}/{zone}.shp")
    collection = list(filter(lambda x: x['geometry'], collection))  # removing all object with no geometries
    shapes = list(map(lambda x: shape(x['geometry']), collection))

    properties = list(map(lambda x: (x['properties']['name'],
                                     x['properties']['entry_dir'],
                                     x['properties']['exit_dir'],
                                     x['properties']['tunnel']), collection))
    return (shapes, properties)


def process_geometries(folder: str, geometries: List, geometry_names: List[str], union=False, directions=False):
    def process_single(zone: str):
        # used only by process_distance
        shapes, names = process_zone(folder, zone, union)
        geometries.extend(shapes)
        geometry_names.extend(names)

    def process_single_with_directions(zone: str):
        # used by process_intersections and process_directions
        shapes, properties = process_zone_with_directions(folder, zone)
        geometries.extend(shapes)
        geometry_names.extend(properties)
    return process_single if not directions else process_single_with_directions
