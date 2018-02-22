import Adafruit_ADS1x15
from time import sleep
import math

# Connect windspeed on one side to GND and another to ADC channel 0 pin???
#adc = Adafruit_ADS1x15.ADS1015() # default address 0x48
adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

def map2volt(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def wind_dir( WindDirVoltage):

  # Werte laut Datenblatt, aufsteigend zur Suche geordnet
  #int windrichtungVolt[] = {320, 410, 450, 620, 900, 1190, 1400, 1980, 2250, 2930, 3080, 3430, 3840, 4040, 4620, 4780};
  # Werte in Grad laut Datenblatt
  #int windRichtungGrad[] = {113,  68,  90, 158, 135, 203, 180,  23,  45, 248, 225, 338,   0, 292, 270, 315};

  if ((WindDirVoltage>=0)&&(WindDirVoltage<365)):
      Angle = 90+22.5
      AngleStr = 'ESE'
  if ((WindDirVoltage>=365)&&(WindDirVoltage<430)):
      Angle = 90-22.5
      AngleStr = 'ENE'
  if ((WindDirVoltage>=430)&&(WindDirVoltage<535)):
      Angle = 90
      AngleStr = 'E'
  if ((WindDirVoltage>=535)&&(WindDirVoltage<735)):
      Angle = 180-22.5
      AngleStr = 'SSE'
  if ((WindDirVoltage>=735)&&(WindDirVoltage<1050)):
      Angle = 90+45
      AngleStr = 'SE'
  if ((WindDirVoltage>=1050)&&(WindDirVoltage<1300)):
      Angle = 180+22.5
      AngleStr = 'SSW'
  if ((WindDirVoltage>=1300)&&(WindDirVoltage<1700)):
      Angle = 180
      AngleStr = 'S'
  if ((WindDirVoltage>=1700)&&(WindDirVoltage<2100)):
      Angle = 0+22.5
      AngleStr = 'NNE'
  if ((WindDirVoltage>=2100)&&(WindDirVoltage<2550)):
      Angle = 0+22.5
      AngleStr = 'NE'
  if ((WindDirVoltage>=2550)&&(WindDirVoltage<3000)):
      Angle = 270-22.5
      AngleStr = 'SSW'
  if ((WindDirVoltage>=3000)&&(WindDirVoltage<3250)):
      Angle = 270-45
      AngleStr = 'SW'
  if ((WindDirVoltage>=3250)&&(WindDirVoltage<3630)):
      Angle = 360-22.5
      AngleStr = 'NNW'
  if ((WindDirVoltage>=3630)&&(WindDirVoltage<3940)):
      Angle = 0
      AngleStr = 'N'
  if ((WindDirVoltage>=3940)&&(WindDirVoltage<4140)):
      Angle = 360-22.5
      AngleStr = 'WNW'
  if ((WindDirVoltage>=4140)&&(WindDirVoltage<4440)):
      Angle = 360-45
      AngleStr = 'NW'
  if ((WindDirVoltage>=4440)&&(WindDirVoltage<4700)):
      Angle = 270
      AngleStr = 'W'

  return Angle, AngleStr

while True:
  count = 0
  sleep(interval)
  values[i] = adc.read_adc(i, gain=1/1.25) # Scale gain for values up to 5V (NOTE: reverse gain values...)
  volt = map2volt(wind_dir, 1, 2047, 1, 5000); # Read from A0 values from 0-2047 (12bit) and map to volt
  Angle, AngleStr = wind_dir(volt)

  print ( str(Angle), "direction_angle")
  print ( AngleStr, "direction")
