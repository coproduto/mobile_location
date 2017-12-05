from .enums import CitySize, AreaKind
import numpy as np

class FreeSpace:
  def __init__(self, frequency):
    self.frequency = frequency

  def path_loss(self, distance):
    return 32.44 + 20 * np.log10(distance) + 20 * np.log10(self.frequency)

