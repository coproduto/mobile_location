from .enums import AreaKind, CitySize
import numpy as np

class Cost231:
  def __init__(
      self,
      frequency,
      transmitter_height,
      receiver_height,
      street_width,
      building_setback,
      mean_building_height,
      city_size
  ):
    self.frequency = frequency
    self.transmitter_height = transmitter_height
    self.receiver_height = receiver_height
    self.street_width = street_width
    self.building_setback = building_setback
    self.mean_building_height = mean_building_height
    self.city_size = city_size

  def path_loss(self, distance):
    if self.frequency < 150 or self.frequency > 2000:
      raise ValueError('The frequency for the Cost231 model is out of bounds')

    delta_h = self.receiver_height/self.transmitter_height
    height_loss = 18 * np.log(1 + delta_h)

    k_a = 54.0
    k_d = 18.0
    k_f = 4.0

    if self.mean_building_height > self.transmitter_height:
      height_loss = 0
      height_coef_n = (self.transmitter_height - self.mean_building_height)
      height_coef_d = (self.transmitter_height - self.receiver_height)
      k_d = k_d - 15 * height_coef_n/height_coef_d

    if self.mean_building_height <= self.transmitter_height and distance >= 0.5:
      k_a = k_a - 0.8 * delta_h
    elif self.mean_building_height <= self.transmitter_height and distance < 0.5:
      k_a = k_a

    if self.city_kind == CitySize.SMALL:
      k_f = k_f + 0.7 * (self.frequency / 925 - 1)
    else:
      k_f = k_f + 1.5 * (self.frequency / 925 - 1)

    free_space_loss = 32.4 + 20 * np.log10(distance) + 20 * np.log10(self.frequency)
    rooftop_loss = 8.2 + 10 * np.log(self.street_width) + 10 * np.log10(self.frequency) + 10 * np.log(delta_h)
    multipath_loss = height_loss + k_a + k_d * np.log10(distance) + k_f * np.log(self.frequency) - 9 * np.log10(self.building_setback)

    return free_space_loss + rooftop_loss + multipath_loss
