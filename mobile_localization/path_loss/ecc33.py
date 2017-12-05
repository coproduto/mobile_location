from .enums import CitySize, AreaKind
import numpy as np

class Ecc33:
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
    if self.frequency < 900 or self.frequency > 1900:
      raise ValueError('The frequency for the ECC-33 model is out of bounds')

    plfs = 92.4 + 20 * np.log10(distance) + 20 * np.log10(self.frequency/1000)
    plbm = 20.41 + 9.83 * np.log10(distance) + 7.894 * np.log10(self.frequency/1000)
    + 9.56 * (np.log10(self.frequency/1000)**2)
    gb = np.log10(self.transmitter_height/200) * (13.98 + 5.8 * np.log10(distance)**2)
    gm = (42.57 + 13.7 * np.log10(self.frequency/1000)) * (np.log10(self.receiver_height)-0.585)
    return plfs + plbm - gb - gm

    
