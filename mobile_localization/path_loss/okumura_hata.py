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

  def path_loss(self, distance):
    if self.frequency < 500 or self.frequency > 1500:
      raise ValueError('The frequency for the Okumura-Hata model is out of bounds')

    a = 0
    if self.frequency <= 200 and city_size == CitySize.LARGE:
      a = 8.29 * (np.log10(1.54 * self.receiver_height))**2 - 1.1
    elif self.frequency >= 400 and city_size == CitySize.LARGE:
      a = 3.2 * (np.log10(11.75 * self.receiver_height))**2 - 4.97
    else:
      a = 1.1 * (np.log10(self.frequency - 0.7)) * self.receiver_height
      - 1.56 * np.log10(self.frequency - 0.8)

      urban_loss = 69.55 + 26.16*np.log10(self.frequency)
      - 13.82 * np.log10(self.transmitter_height) - a
      + (44.9 - 6.55 * np.log10(self.transmitter_height)) * np.log10(distance)

      if self.area_kind == AreaKind.OPEN:
        return urban_loss - 4.78 * (np.log10(self.frequency)**2)
        + 18.33 * np.log10(self.frequency) - 40.94
      elif self.area_kind == AreaKind.SUBURBAN:
        return urban_loss - 2 * (np.log10(self.frequency/28))**2 - 5.4
      return urban_loss
