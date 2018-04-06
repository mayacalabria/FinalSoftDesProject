"""
Sketch code for creating court svg before integraring into NBAcode.py
Creates polygons for different zones according to the svg path

Requirements:

    pip install BeautifulSoup
    pip install svg.path
"""

import itertools
from bs4 import BeautifulSoup
from collections import OrderedDict
from svg.path import parse_path
from lxml import etree as ET

__all__ = ['zones']

SEGMENT_CTL_PT_PROPS = ['start', 'control', 'control1', 'control2', 'end']
"""An ordered list of names of `svg.path` properties that hold control points."""

def get_segment_control_points(segment):
    """Given an `svg.path` segment, return its list of control points.
    Each control point is a pair of floats `(x, y)`.

    This does the minimum to support the paths in the map files.
    In particular, it simply returns the endpoints of arc segments.
    """

    cpts = (getattr(segment, prop) for prop in SEGMENT_CTL_PT_PROPS if hasattr(segment, prop))
    return [(pt.real, pt.imag) for pt in cpts]

def path_to_points(path):
    """Given an `svg.path` Path, return a list of its control points.
    Each control point is a pair of floats `(x, y)`.
    """

    pts = (pt
           for segment in path
           for pt in get_segment_control_points(segment))
    # remove duplicates
    return [pti.__next__() for _, pti in itertools.groupby(pts)]


def svg_path_to_polygons(path_data):
    """Return a list of polygons that collectively approximate the SVG path whose string is `path_data`.
    This handles just enough cases to parse the map files.
    """
    path_strings = [s for s in path_data.split('m') if s]
    path_prefix = 'm'

    polygons = []
    for path_string in path_strings:
        if path_string[0] not in 'M':
            path_string = path_prefix + path_string
        path = parse_path(path_string)
        polygons.append(path_to_points(path))
        end_pt = path[-1].end
        path_prefix = 'M %f,%f m' % (end_pt.real, end_pt.imag)
    print (polygons)
    return polygons


def _load_zones(svg_filename = 'Basketball_-_NBA_-_field_diagram_-en.svg'):
    """Initialize the `countries` module variable."""

    zones = {}

    with open(svg_filename, 'r') as svg:
        soup = BeautifulSoup(svg.read(),'lxml')

    for p in soup.findAll('path'):
        zone_name = p.get('id', None)
        path_data = p.get('d', None)
        if zone_name and path_data:
            zones[zone_name] = svg_path_to_polygons(path_data)

    return OrderedDict(sorted(zones.items()))

zones= _load_zones()
"""A `dict` of zone names to lists of polygons. Each polygon is a list of points.
Each point is a tuple of floats `(x, y)`."""
svg_path_to_polygons(path_data)
