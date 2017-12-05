import os
from .reader import open_csv_file, read_erbs_file, read_measurements_file
from .path_loss import Cost231, Cost231Hata, FlatEarth, OkumuraHata
from .path_loss import FreeSpace, Ecc33, CitySize, AreaKind
from .geo import Coordinate, distance_in_km, azimuth

def start():
  print("Hello, world!")
  print("Current directory is ", os.getcwd())
  print("Trying to read erbs.csv")
  erbs = open_csv_file('erbs.csv', read_erbs_file)
  print(erbs)
  print("Trying to read medicoes.csv")
  measurements = open_csv_file('medicoes.csv', read_measurements_file)
  print(measurements)
