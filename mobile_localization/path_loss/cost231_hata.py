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
    if self.frequency < 150 or self.frequency > 2000:
      raise ValueError('The frequency for the Cost231-Hata model is out of bounds')

    c = 0
    if self.area_kind == AreaKind.URBAN:
      c = 3

    ar = (1.1 * np.log10(self.frequency) - 0.7) * self.receiver_height
    - (1.56 * np.log(self.frequency) - 0.8)
      
    loss = 46.3 + 33.9 * np.log10(self.frequency)
    - 13.82 * np.log10(self.transmitter_height)
    - ar + (44.9 + 6.55 * np.log(self.transmitter_height)) * np.log(distance) + c

    return loss
