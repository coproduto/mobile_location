import os
import sys
import numpy as np
import pandas as pd
from .reader import open_csv_file, read_erbs_file, read_measurements_file
from .path_loss import Cost231, Cost231Hata, FlatEarth, OkumuraHata
from .path_loss import FreeSpace, Ecc33, CitySize, AreaKind
from .geo import Coordinate, distance_in_km, azimuth
from .grid import Grid, Point, loss_matrix_from_grid
from .enums import CitySize, AreaKind

def make_coord_matrix(grid):
  print('making coordinate grid')
  print('will take approx.', int(np.round(grid.vertical_cell_count/180)), 'minutes')
  coord_grid = grid.make_coord_grid()
  print('done')
  return coord_grid

def compute_loss(method, distance):
  loss_estimator = None
  if method == 'free_space':
    loss_estimator = FreeSpace(frequency = 1800)
  elif method == 'flat_earth':
    loss_estimator = FlatEarth(
      frequency = 1800,
      transmitter_height = 100,
      receiver_height = 1.5
    )
  elif method == 'okumura':
    loss_estimator = OkumuraHata(
      frequency = 1800,
      transmitter_height = 100,
      receiver_height = 1.5,
      city_size = CitySize.MEDIUM,
      area_kind = AreaKind.SUBURBAN
    )
  elif method == 'cost_hata':
    loss_estimator = Cost231Hata(
      frequency = 1800,
      transmitter_height = 100,
      receiver_height = 1.5,
      area_kind = AreaKind.SUBURBAN
    )
  elif method == 'ecc33':
    loss_estimator = Ecc33(
      frequency = 1800,
      transmitter_height = 100,
      receiver_height = 1.5,
    )

  if loss_estimator is None:
    raise ValueError('Invalid loss estimator')

  return loss_estimator.path_loss(distance)
  

def make_loss_matrix(method, station_coord, grid):
  loss_estimator = None
  if method == 'free_space':
    loss_estimator = FreeSpace(frequency = 1800)
  elif method == 'flat_earth':
    loss_estimator = FlatEarth(
      frequency = 1800,
      transmitter_height = 100,
      receiver_height = 1.5
    )
  elif method == 'okumura':
    loss_estimator = OkumuraHata(
      frequency = 1800,
      transmitter_height = 100,
      receiver_height = 1.5,
      city_size = CitySize.MEDIUM,
      area_kind = AreaKind.SUBURBAN
    )
  elif method == 'cost_hata':
    loss_estimator = Cost231Hata(
      frequency = 1800,
      transmitter_height = 100,
      receiver_height = 1.5,
      area_kind = AreaKind.SUBURBAN
    )
  elif method == 'ecc33':
    loss_estimator = Ecc33(
      frequency = 1800,
      transmitter_height = 100,
      receiver_height = 1.5,
    )

  if loss_estimator is None:
    raise ValueError('Invalid loss estimator')

  print('making loss matrix')
  loss_matrix = loss_matrix_from_grid(grid, station_coord, loss_estimator.path_loss)
  print('done')
  return loss_matrix

def read_coord_grid(matrix):
    return [list(map(lambda pair: Coordinate(pair[0], pair[1]), line)) for line in matrix]

def make_loss_vector(station_powers, dictionary):
  loss_list = []
  for index, power in enumerate(station_powers):
    loss_list.append(station_powers[index] - dictionary['RSSI_' + str(index + 1)])
  return np.array(loss_list)

def start():
  if len(sys.argv) > 1:
    measurements_file = sys.argv[1]
  else:
    measurements_file = 'testLoc.csv'
  print('opening', measurements_file)
  
  method = 'cost_hata'
  print("Current directory is ", os.getcwd())
  erbs = open_csv_file('erbs.csv', read_erbs_file)
  measurements = open_csv_file(measurements_file, read_measurements_file)

  top_left = Coordinate(-8.065, -34.91)
  bottom_right = Coordinate(-8.08, -34.887)
  resolution = 10
  grid = Grid(top_left, bottom_right, resolution)
  coord_matrix = make_coord_matrix(grid)

  loss_matrices = []
  erb_coords = []
  erb_power = []
  for index, erb in erbs.iterrows():
    station = Coordinate(erbs.ix[index].lat, erbs.ix[index].lon)
    erb_coords.append(station)
    erb_power.append(erbs.ix[index].eirp)
    filename = method + '_' + str(index) + '.csv'
    if os.path.isfile(filename):
      with open(filename) as csvfile:
        loss_frame = pd.read_csv(csvfile)
        loss_matrices.append(np.delete(loss_frame.values, 0, axis=1))
    else:
      loss_matrix = make_loss_matrix(method, station, coord_matrix)
      loss_frame = pd.DataFrame(loss_matrix)
      loss_frame.to_csv(filename)
      loss_matrices.append(loss_matrix)

  loss_vectors = []
  for index, dictionary in measurements.iterrows():
    loss_vectors.append(make_loss_vector(erb_power, dictionary))

  loss_array = np.array(loss_vectors)
  full_loss_matrix = np.stack(loss_matrices, axis=-1)

  print('generating output...')
  output = [0] * measurements.shape[0]
  for index, measurement in measurements.iterrows():
    error_matrix = np.apply_along_axis(
      arr = full_loss_matrix,
      func1d = lambda v: np.linalg.norm(v-loss_vectors[index]),
      axis = 2
    )
    expected_position = np.argmin(error_matrix)
    error_matrix_lines, error_matrix_cols = error_matrix.shape
    expected_position_line = expected_position // error_matrix_cols
    expected_position_col = expected_position % error_matrix_cols

    actual_position = Coordinate(measurements.ix[index]['lat'], measurements.ix[index]['lon'])
    predicted_position = grid.coordinates_at_cell_center(
      Point(expected_position_col, expected_position_line)
    )

    output_dictionary = {
      'predicted_lat': predicted_position.latitude,
      'predicted_lon': predicted_position.longitude,
      'actual_lat': actual_position.latitude,
      'actual_lon': actual_position.longitude,
      'error': np.linalg.norm(full_loss_matrix[expected_position_line][expected_position_col] - loss_vectors[index]),
      'distance': distance_in_km(actual_position, predicted_position)
    }

    output[index] = pd.Series(output_dictionary)
    print(index + 1, 'done of', measurements.shape[0])
      
  output_frame = pd.DataFrame(output)
  output_frame.to_csv(method + '_output.csv')

  print('Mean error:', output_frame['error'].mean())
  print('Median error:', output_frame['error'].median())
  print('Error standard dev:', output_frame['error'].std())
  print('Mean distance:', output_frame['distance'].mean())
  print('Median distance:', output_frame['distance'].median())
  print('Distance standard dev:', output_frame['distance'].std())

def test():
  methods = [
    'free_space',
    'flat_earth',
    'okumura',
    'cost_hata',
    'ecc33'
  ]
  erbs = open_csv_file('erbs.csv', read_erbs_file)
  measurements = open_csv_file('medicoes.csv', read_measurements_file)

  erb_coords = []
  erb_power = []
  for index, erb in erbs.iterrows():
    station = Coordinate(erbs.ix[index].lat, erbs.ix[index].lon)
    erb_coords.append(station)
    erb_power.append(erbs.ix[index].eirp)
      
  error_array = np.zeros(len(methods))
  for method_index, method in enumerate(methods):
    print('evaluating method', method)
    actual_loss_vectors = np.zeros((measurements.shape[0], 6))
    predicted_loss_vectors = np.zeros((measurements.shape[0], 6))
    for index, dictionary in measurements.iterrows():
      print(index + 1, 'measurements out of', measurements.shape[0], 'done')
      position = Coordinate(dictionary['lat'], dictionary['lon'])
      actual_loss_vectors[index] = make_loss_vector(erb_power, dictionary)
      predicted_losses = []
      for coord in erb_coords:
        distance = distance_in_km(coord, position)
        loss = compute_loss(method, distance)
        predicted_losses.append(loss)
      predicted_loss_vectors[index] = np.array(predicted_losses)
    difference_array = predicted_loss_vectors - actual_loss_vectors
    mean_square_error = np.mean(np.square(np.ndarray.flatten(difference_array)))
    error_array[method_index] = mean_square_error
          
  errors = zip(methods, error_array.tolist())
  print(list(errors))

  print('minimum error is', methods[np.argmin(error_array)], 'with', error_array[np.argmin(error_array)])

      
      
