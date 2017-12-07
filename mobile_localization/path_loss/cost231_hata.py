from .enums import CitySize, AreaKind
import numpy as np

class Cost231Hata:
  def __init__(
      self,
      frequency,
      transmitter_height,
      receiver_height,
      area_kind
  ):
    self.frequency = frequency
    self.transmitter_height = transmitter_height
    self.receiver_height = receiver_height
    self.area_kind = area_kind

  def path_loss(self, distance):
    constant_factor = 46.3
    frequency_factor = 33.9 * np.log10(self.frequency)
    c = 3 if self.area_kind.value == AreaKind.URBAN.value else 0
    base_height_factor = 13.82 * np.log10(self.transmitter_height)
    distance_factor = (44.9 - 6.55 * np.log10(self.transmitter_height)) * np.log10(distance)
    height_correction_factor = 0.8 + (1.1 * np.log10(self.frequency) * self.receiver_height) - 1.56 * np.log10(self.frequency)
    if self.area_kind.value == AreaKind.URBAN.value:
      height_correction_factor = 3.2 * np.log10(11.75 * self.receiver_height)**2 - 4.97

    loss = constant_factor + frequency_factor - base_height_factor - height_correction_factor + distance_factor + c

    return loss
