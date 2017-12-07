import numpy as np
from .geo import Coordinate, distance_in_km
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

class Grid:
    def __init__(self, top_left, bottom_right, resolution):
        top_right = Coordinate(
            latitude = top_left.latitude,
            longitude = bottom_right.longitude
        )
        bottom_left = Coordinate(
            latitude = bottom_right.latitude,
            longitude = top_left.longitude
        )

        upper_edge_length = distance_in_km(top_left, top_right) * 1000
        left_edge_length = distance_in_km(top_left, bottom_left) * 1000

        self.origin = top_left
        self.upper_edge_length = upper_edge_length
        self.left_edge_length = left_edge_length
        self.resolution = resolution
        self.horizontal_cell_count = upper_edge_length / resolution
        self.vertical_cell_count = left_edge_length / resolution

    def coordinates_at_point(self, point):
        pass
