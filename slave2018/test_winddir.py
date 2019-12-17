from ADS1x15 import *
from time import sleep
import math

def map2volt(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def wind_dir( WindDirVoltage):

  Angle=9999
  AngleStr=''

  # Werte laut Datenblatt, aufsteigend zur Suche geordnet
  #int windrichtungVolt[] = {320, 410, 450, 620, 900, 1190, 1400, 1980, 2250, 2930, 3080, 3430, 3840, 4040, 4620, 4780};
  # Werte in Grad laut Datenblatt
  #int windRichtungGrad[] = {113,  68,  90, 158, 135, 203, 180,  23,  45, 248, 225, 338,   0, 292, 270, 315};

  if ((WindDirVoltage>=0)and(WindDirVoltage<365)):
      Angle = 90+22.5
      AngleStr = 'ESE'
  if ((WindDirVoltage>=365)and(WindDirVoltage<430)):
      Angle = 90-22.5
      AngleStr = 'ENE'
  if ((WindDirVoltage>=430)and(WindDirVoltage<535)):
      Angle = 90
      AngleStr = 'E'
  if ((WindDirVoltage>=535)and(WindDirVoltage<735)):
      Angle = 180-22.5
      AngleStr = 'SSE'
  if ((WindDirVoltage>=735)and(WindDirVoltage<1050)):
      Angle = 90+45
      AngleStr = 'SE'
  if ((WindDirVoltage>=1050)and(WindDirVoltage<1300)):
      Angle = 180+22.5
      AngleStr = 'SSW'
  if ((WindDirVoltage>=1300)and(WindDirVoltage<1700)):
      Angle = 180
      AngleStr = 'S'
  if ((WindDirVoltage>=1700)and(WindDirVoltage<2100)):
      Angle = 0+22.5
      AngleStr = 'NNE'
  if ((WindDirVoltage>=2100)and(WindDirVoltage<2550)):
      Angle = 0+22.5
      AngleStr = 'NE'
  if ((WindDirVoltage>=2550)and(WindDirVoltage<3000)):
      Angle = 270-22.5
      AngleStr = 'SSW'
  if ((WindDirVoltage>=3000)and(WindDirVoltage<3250)):
      Angle = 270-45
      AngleStr = 'SW'
  if ((WindDirVoltage>=3250)and(WindDirVoltage<3630)):
      Angle = 360-22.5
      AngleStr = 'NNW'
  if ((WindDirVoltage>=3630)and(WindDirVoltage<3940)):
      Angle = 0
      AngleStr = 'N'
  if ((WindDirVoltage>=3940)and(WindDirVoltage<4140)):
      Angle = 360-22.5
      AngleStr = 'WNW'
  if ((WindDirVoltage>=4140)and(WindDirVoltage<4440)):
      Angle = 360-45
      AngleStr = 'NW'
  if ((WindDirVoltage>=4440)and(WindDirVoltage<4700)):
      Angle = 270
      AngleStr = 'W'

  return Angle, AngleStr

# Connect winddir on one side to GND and another to ADC channel 0 pin with par resistor
adc = ADS1015(address=0x48, busnum=1)
# Gain can be: 2/3 1 2 4 8 16
value = adc.read_adc(0, gain=1) # Scale gain for values up to 5V (NOTE: reverse gain values...)
print('ADC read value: '+str(value))
volt = map2volt(value, 1, 1535, 1, 4600); # Read from A0 values from 0-2047 (12bit) and map to volt
print('ADC value 1-2047 mapped to 1-5000V: '+str(volt))
Angle,AngleStr=wind_dir(volt)
print('Detected direction: ' + AngleStr) # Angle, AngleStr

