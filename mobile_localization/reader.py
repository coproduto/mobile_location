import csv
from collections import namedtuple
import pandas as pd

Result = namedtuple('Result', ['success', 'value'])

def not_none(value):
  if value is None:
    raise TypeError('None found when value was expected')
  else:
    return value

def make_erb(erb_dict):
  try:
    converted_dict = {
      'nr': not_none(erb_dict['nr']),
      'name': not_none(erb_dict['name']),
      'lat': float(erb_dict['lat']),
      'lon': float(erb_dict['lon']),
      'band': not_none(erb_dict['band']),
      'bcch': int(erb_dict['bcch']),
      'eirp': float(erb_dict['eirp'])
    }
    return Result(success=True, value=pd.Series(converted_dict))
  except (ValueError, TypeError) as e:
    return Result(success=False, value=None)

def make_measurement(measurement_dict):
  try:
    converted_dict = {
      'lat': float(measurement_dict['lat']),
      'lon': float(measurement_dict['lon']),
      'RSSI_1': float(measurement_dict['RSSI_1']),
      'RSSI_2': float(measurement_dict['RSSI_2']),
      'RSSI_3': float(measurement_dict['RSSI_3']),
      'RSSI_4': float(measurement_dict['RSSI_4']),
      'RSSI_5': float(measurement_dict['RSSI_5']),
      'RSSI_6': float(measurement_dict['RSSI_6'])
    }
    return Result(success=True, value=pd.Series(converted_dict))
  except (ValueError, TypeError) as e:
    return Result(success=False, value=None)

def read_csv_file(csv_file, postprocess):
  reader = csv.DictReader(csv_file)
  output = []
  for line in reader:
    processed = postprocess(line)
    if not processed.success:
      return Result(success=False, value=None)
    else:
      output.append(processed.value)
  return Result(success=True, value=output)

def read_erbs_file(erbs_file):
  return read_csv_file(erbs_file, make_erb)

def read_measurements_file(measurements_file):
  return read_csv_file(measurements_file, make_measurement)
      
def open_csv_file(name, reader):
  with open(name, newline='') as csv_file:
    result = reader(csv_file)
    if result.success:
      return pd.DataFrame(result.value)
    else:
      return None
