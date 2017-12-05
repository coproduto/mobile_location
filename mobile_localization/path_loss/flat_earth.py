from .enums import CitySize, AreaKind
import numpy as np

class FlatEarth:
  def __init__(
      self,
      frequency,
      transmitter_height,
      receiver_height
  ):
    self.frequency = frequency
    self.transmitter_height = transmitter_height
    self.receiver_height = receiver_height

  def path_loss(self, distance):
    l1 = -20 * np.log10(self.transmitter_height)
    l2 = -20 * np.log10(self.receiver_height)
    lo = 120 + 10 * 4 * np.log10(distance)
    return l1 + l2 + lo
