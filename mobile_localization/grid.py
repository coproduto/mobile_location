import numpy as np
from .geo import Coordinate, distance_in_km, bearing, coordinate_at_distance
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
        print(upper_edge_length)
        print(left_edge_length)

        self.origin = top_left
        self.upper_edge_length = upper_edge_length
        self.left_edge_length = left_edge_length
        self.resolution = resolution
        self.horizontal_cell_count = int(np.ceil(upper_edge_length / resolution))
        self.vertical_cell_count = int(np.ceil(left_edge_length / resolution))

        print(self.horizontal_cell_count)
        print(self.vertical_cell_count)

    def coordinates_at_cell_center(self, point):
        start = self.origin
        bearing = (np.rad2deg(np.arctan2(point.y, point.x)) + 90) % 360
        x_distance = point.x * self.resolution
        y_distance = point.y * self.resolution
        distance = np.sqrt(x_distance**2 + y_distance**2) / 1000
        return coordinate_at_distance(start, distance, bearing)

    def make_coord_grid(self):
        grid = np.mgrid[0:self.vertical_cell_count, 0:self.horizontal_cell_count]
        pair_grid = np.stack((grid[0], grid[1]), axis=2).tolist()
        coord_grid = [list(map(lambda pair: self.coordinates_at_cell_center(Point(pair[0], pair[1])), line)) for line in pair_grid]
        return coord_grid



def loss_matrix_from_grid(coord_grid, station_coords, loss_function):
    print('making loss matrix')
    loss_grid = [list(map(lambda coord: loss_function(distance_in_km(station_coords, coord)), line)) for line in coord_grid]
    print('done')
    return np.array(loss_grid)

        
