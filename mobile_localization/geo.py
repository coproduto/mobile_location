import numpy as np
from collections import namedtuple

Coordinate = namedtuple('Coordinate', ['latitude', 'longitude'])

def sin_d(angle):
  return np.sin(np.deg2rad(angle))

def cos_d(angle):
  return np.cos(np.deg2rad(angle))

def distance_in_km(coordinate_a, coordinate_b):
  lat_sine = sin_d((coordinate_b.latitude - coordinate_a.latitude)/2) ** 2
  lon_sine = sin_d((coordinate_b.longitude - coordinate_a.longitude)/2) ** 2
  cosine_a = cos_d(coordinate_a.latitude)
  cosine_b = cos_d(coordinate_b.latitude)
  return 2 * 6372.8 * np.arcsin(np.sqrt(lat_sine + cosine_a * cosine_b * lon_sine))

def azimuth(coordinate_a, coordinate_b):
  numerator_cosine = cos_d(coordinate_b.latitude)
  numerator_sine = sin_d(coordinate_b.longitude - coordinate_a.longitude)
  denominator_a = sin_d(coordinate_b.latitude) * cos_d(coordinate_a.latitude)
  denominator_b = cos_d(coordinate_b.latitude) * sin_d(coordinate_a.latitude)
  denominator_c = cos_d(coordinate_b.longitude - coordinate_a.longitude)
  numerator = numerator_cosine * numerator_sine
  denominator = denominator_a - denominator_b * denominator_c
  argument = (np.arctan2(numerator, denominator) + 2 * np.pi) % (2 * np.pi)
  return np.rad2deg(argument)

def bearing(coordinate_a, coordinate_b):
  delta_lambda = coordinate_b.longitude - coordinate_a.longitude
  start_latitude = coordinate_a.latitude
  end_latitude = coordinate_b.latitude
  start_longitude = coordinate_a.longitude
  argument_num = sin_d(delta_lambda) * cos_d(end_latitude)
  argument_denom_1 = cos_d(start_latitude) * sin_d(end_latitude)
  argument_denom_2 = sin_d(start_latitude) * cos_d(end_latitude) * cos_d(delta_lambda)
  result = np.arctan2(argument_num, argument_denom_1 - argument_denom_2)

  return (np.rad2deg(result) + 360) % 360

def coordinate_at_distance(start, distance, bearing):
  rad_distance = distance / 6372.8
  arg_1 = sin_d(start.latitude) * np.cos(rad_distance)
  arg_2 = cos_d(start.latitude) * np.sin(rad_distance) * cos_d(bearing)
  target_latitude = np.arcsin(arg_1 + arg_2)
  numer = sin_d(bearing) * np.sin(rad_distance) * cos_d(start.latitude)
  denom = np.cos(rad_distance) - sin_d(start.latitude) * np.sin(target_latitude)
  target_longitude = start.longitude + ((np.rad2deg(np.arctan2(numer, denom)) + 540) % 360 - 180)

  return Coordinate(latitude = np.rad2deg(target_latitude), longitude = target_longitude)
