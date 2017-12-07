from .enums import CitySize, AreaKind
import numpy as np

class OkumuraHata:
  def __init__(
      self,
      frequency,
      transmitter_height,
      receiver_height,
      city_size,
      area_kind,
  ):
     self.frequency = frequency
     self.transmitter_height = transmitter_height
     self.receiver_height = receiver_height
     self.city_size = city_size,
     self.area_kind = area_kind

  def _height_correction(self):
    if self.city_size == CitySize.LARGE and self.frequency <= 200:
      return 8.29 * (np.log10(1.54 * self.receiver_height)**2) - 1.1
    elif self.city_size == CitySize.LARGE:
      return 3.2 * (np.log10(11.75 * self.receiver_height)**2) - 4.97
    else:
      return 0.8 + (1.1 * np.log10(self.frequency) - 0.7) * self.receiver_height - 1.56 * np.log10(self.frequency)
     
  def _base_loss(self, distance):
    constant_factor = 69.55
    frequency_factor = 26.16 * np.log10(self.frequency)
    base_height_factor = 13.82 * np.log10(self.transmitter_height)
    distance_factor = (44.9 - 6.55 * np.log10(self.transmitter_height)) * np.log10(distance)
    return constant_factor + frequency_factor - base_height_factor - self._height_correction() + self.distance_factor

  def _suburban_loss(self, distance):
    frequency_factor = 2 * (np.log10(self.frequency/28.0)**2)
    constant_factor = 5.4

    return self._base_loss(distance) - frequency_factor - constant_factor

  def _rural_loss(self, distance):
    frequency_factor = 4.78 * (np.log10(self.frequency)**2) - 18.33 * (np.log10(self.frequency))
    constant_factor = 40.94

    return self._base_loss(distance) - frequency_factor - constant_factor
     
  def path_loss(self, distance):
    if self.area_kind == AreaKind.URBAN:
      return self._base_loss(distance)
    elif self.area_kind == AreaKind.SUBURBAN:
      return self._suburban_loss(distance)
    elif self.area_kind == AreaKind.RURAL:
      return self._rural_loss(distance)
    else:
      raise ArgumentError("Invalid area type")
