import numpy as np
from collections import namedtuple

Coordinate = namedtuple('Coordinate', ['latitude', 'longitude'])

def sin_d(angle):
  return np.sin(angle * np.pi/180)

def cos_d(angle):
  return np.cos(angle * np.pi/180)

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

