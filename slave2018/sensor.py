# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import logging
import math
import smbus
import time
from ctypes import c_short
from ctypes import c_byte
from ctypes import c_ubyte
import I2C



# COMMANDS
SI1145_PARAM_QUERY                      = 0x80
SI1145_PARAM_SET                        = 0xA0
SI1145_NOP                              = 0x0
SI1145_RESET                            = 0x01
SI1145_BUSADDR                          = 0x02
SI1145_PS_FORCE                         = 0x05
SI1145_ALS_FORCE                        = 0x06
SI1145_PSALS_FORCE                      = 0x07
SI1145_PS_PAUSE                         = 0x09
SI1145_ALS_PAUSE                        = 0x0A
SI1145_PSALS_PAUSE                      = 0xB
SI1145_PS_AUTO                          = 0x0D
SI1145_ALS_AUTO                         = 0x0E
SI1145_PSALS_AUTO                       = 0x0F
SI1145_GET_CAL                          = 0x12

# Parameters
SI1145_PARAM_I2CADDR                    = 0x00
SI1145_PARAM_CHLIST                     = 0x01
SI1145_PARAM_CHLIST_ENUV                = 0x80
SI1145_PARAM_CHLIST_ENAUX               = 0x40
SI1145_PARAM_CHLIST_ENALSIR             = 0x20
SI1145_PARAM_CHLIST_ENALSVIS            = 0x10
SI1145_PARAM_CHLIST_ENPS1               = 0x01
SI1145_PARAM_CHLIST_ENPS2               = 0x02
SI1145_PARAM_CHLIST_ENPS3               = 0x04

SI1145_PARAM_PSLED12SEL                 = 0x02
SI1145_PARAM_PSLED12SEL_PS2NONE         = 0x00
SI1145_PARAM_PSLED12SEL_PS2LED1         = 0x10
SI1145_PARAM_PSLED12SEL_PS2LED2         = 0x20
SI1145_PARAM_PSLED12SEL_PS2LED3         = 0x40
SI1145_PARAM_PSLED12SEL_PS1NONE         = 0x00
SI1145_PARAM_PSLED12SEL_PS1LED1         = 0x01
SI1145_PARAM_PSLED12SEL_PS1LED2         = 0x02
SI1145_PARAM_PSLED12SEL_PS1LED3         = 0x04

SI1145_PARAM_PSLED3SEL                  = 0x03
SI1145_PARAM_PSENCODE                   = 0x05
SI1145_PARAM_ALSENCODE                  = 0x06

SI1145_PARAM_PS1ADCMUX                  = 0x07
SI1145_PARAM_PS2ADCMUX                  = 0x08
SI1145_PARAM_PS3ADCMUX                  = 0x09
SI1145_PARAM_PSADCOUNTER                = 0x0A
SI1145_PARAM_PSADCGAIN                  = 0x0B
SI1145_PARAM_PSADCMISC                  = 0x0C
SI1145_PARAM_PSADCMISC_RANGE            = 0x20
SI1145_PARAM_PSADCMISC_PSMODE           = 0x04

SI1145_PARAM_ALSIRADCMUX                = 0x0E
SI1145_PARAM_AUXADCMUX                  = 0x0F

SI1145_PARAM_ALSVISADCOUNTER            = 0x10
SI1145_PARAM_ALSVISADCGAIN              = 0x11
SI1145_PARAM_ALSVISADCMISC              = 0x12
SI1145_PARAM_ALSVISADCMISC_VISRANGE     = 0x20

SI1145_PARAM_ALSIRADCOUNTER             = 0x1D
SI1145_PARAM_ALSIRADCGAIN               = 0x1E
SI1145_PARAM_ALSIRADCMISC               = 0x1F
SI1145_PARAM_ALSIRADCMISC_RANGE         = 0x20

SI1145_PARAM_ADCCOUNTER_511CLK          = 0x70

SI1145_PARAM_ADCMUX_SMALLIR             = 0x00
SI1145_PARAM_ADCMUX_LARGEIR             = 0x03



# REGISTERS
SI1145_REG_PARTID                       = 0x00
SI1145_REG_REVID                        = 0x01
SI1145_REG_SEQID                        = 0x02

SI1145_REG_INTCFG                       = 0x03
SI1145_REG_INTCFG_INTOE                 = 0x01
SI1145_REG_INTCFG_INTMODE               = 0x02

SI1145_REG_IRQEN                        = 0x04
SI1145_REG_IRQEN_ALSEVERYSAMPLE         = 0x01
SI1145_REG_IRQEN_PS1EVERYSAMPLE         = 0x04
SI1145_REG_IRQEN_PS2EVERYSAMPLE         = 0x08
SI1145_REG_IRQEN_PS3EVERYSAMPLE         = 0x10


SI1145_REG_IRQMODE1                     = 0x05
SI1145_REG_IRQMODE2                     = 0x06

SI1145_REG_HWKEY                        = 0x07
SI1145_REG_MEASRATE0                    = 0x08
SI1145_REG_MEASRATE1                    = 0x09
SI1145_REG_PSRATE                       = 0x0A
SI1145_REG_PSLED21                      = 0x0F
SI1145_REG_PSLED3                       = 0x10
SI1145_REG_UCOEFF0                      = 0x13
SI1145_REG_UCOEFF1                      = 0x14
SI1145_REG_UCOEFF2                      = 0x15
SI1145_REG_UCOEFF3                      = 0x16
SI1145_REG_PARAMWR                      = 0x17
SI1145_REG_COMMAND                      = 0x18
SI1145_REG_RESPONSE                     = 0x20
SI1145_REG_IRQSTAT                      = 0x21
SI1145_REG_IRQSTAT_ALS                  = 0x01

SI1145_REG_ALSVISDATA0                  = 0x22
SI1145_REG_ALSVISDATA1                  = 0x23
SI1145_REG_ALSIRDATA0                   = 0x24
SI1145_REG_ALSIRDATA1                   = 0x25
SI1145_REG_PS1DATA0                     = 0x26
SI1145_REG_PS1DATA1                     = 0x27
SI1145_REG_PS2DATA0                     = 0x28
SI1145_REG_PS2DATA1                     = 0x29
SI1145_REG_PS3DATA0                     = 0x2A
SI1145_REG_PS3DATA1                     = 0x2B
SI1145_REG_UVINDEX0                     = 0x2C
SI1145_REG_UVINDEX1                     = 0x2D
SI1145_REG_PARAMRD                      = 0x2E
SI1145_REG_CHIPSTAT                     = 0x30

# I2C Address
SI1145_ADDR                             = 0x60

# Default I2C address for device.
MCP9808_I2CADDR_DEFAULT        = 0x18

# Register addresses.
MCP9808_REG_CONFIG             = 0x01
MCP9808_REG_UPPER_TEMP         = 0x02
MCP9808_REG_LOWER_TEMP         = 0x03
MCP9808_REG_CRIT_TEMP          = 0x04
MCP9808_REG_AMBIENT_TEMP       = 0x05
MCP9808_REG_MANUF_ID           = 0x06
MCP9808_REG_DEVICE_ID          = 0x07

# Configuration register values.
MCP9808_REG_CONFIG_SHUTDOWN    = 0x0100
MCP9808_REG_CONFIG_CRITLOCKED  = 0x0080
MCP9808_REG_CONFIG_WINLOCKED   = 0x0040
MCP9808_REG_CONFIG_INTCLR      = 0x0020
MCP9808_REG_CONFIG_ALERTSTAT   = 0x0010
MCP9808_REG_CONFIG_ALERTCTRL   = 0x0008
MCP9808_REG_CONFIG_ALERTSEL    = 0x0002
MCP9808_REG_CONFIG_ALERTPOL    = 0x0002
MCP9808_REG_CONFIG_ALERTMODE   = 0x0001


class MCP9808(object):
	"""Class to represent an Adafruit MCP9808 precision temperature measurement
	board.
	"""

	def __init__(self, address, i2c=None, **kwargs):
		"""Initialize MCP9808 device on the specified I2C address and bus number.
		Address defaults to 0x18 and bus number defaults to the appropriate bus
		for the hardware.
		"""
		self._logger = logging.getLogger('Adafruit_MCP9808.MCP9808')
		if i2c is None:
			import Adafruit_GPIO.I2C as I2C
			i2c = I2C
		self._device = i2c.get_i2c_device(address, **kwargs)


	def begin(self):
		"""Start taking temperature measurements. Returns True if the device is
		intialized, False otherwise.
		"""
		# Check manufacturer and device ID match expected values.
		mid = self._device.readU16BE(MCP9808_REG_MANUF_ID)
		did = self._device.readU16BE(MCP9808_REG_DEVICE_ID)
		self._logger.debug('Read manufacturer ID: {0:04X}'.format(mid))
		self._logger.debug('Read device ID: {0:04X}'.format(did))
		return mid == 0x0054 and did == 0x0400

	def readTempC(self):
		"""Read sensor and return its value in degrees celsius."""
		# Read temperature register value.
		t = self._device.readU16BE(MCP9808_REG_AMBIENT_TEMP)
		self._logger.debug('Raw ambient temp register value: 0x{0:04X}'.format(t & 0xFFFF))
		# Scale and convert to signed value.
		temp = (t & 0x0FFF) / 16.0
		if t & 0x1000:
			temp -= 256.0
		return temp

def get_temp_mcp9808(address):
	sensor = MCP9808(address)
	# Optionally you can override the address and/or bus number:
	#sensor = MCP9808.MCP9808(address=0x20, busnum=2)
	# Initialize communication with the sensor.
	sensor.begin()
	return sensor.readTempC()

# BME Part
def getShort(data, index):
  # return two bytes from data as a signed 16-bit value
  return c_short((data[index+1] << 8) + data[index]).value

def getUShort(data, index):
  # return two bytes from data as an unsigned 16-bit value
  return (data[index+1] << 8) + data[index]

def getChar(data,index):
  # return one byte from data as a signed char
  result = data[index]
  if result > 127:
    result -= 256
  return result

def getUChar(data,index):
  # return one byte from data as an unsigned char
  result =  data[index] & 0xFF
  return result

def readBME280ID(addr):

  bus = smbus.SMBus(I2C.get_default_bus()) # Rev 2 Pi, Pi 2 & Pi 3 uses bus 1
                         # Rev 1 Pi uses bus 0
  # Chip ID Register Address
  REG_ID     = 0xD0
  (chip_id, chip_version) = bus.read_i2c_block_data(addr, REG_ID, 2)
  return (chip_id, chip_version)

def readBME280All(addr):

  bus = smbus.SMBus(I2C.get_default_bus()) # Rev 2 Pi, Pi 2 & Pi 3 uses bus 1
                         # Rev 1 Pi uses bus 0
  # Register Addresses
  REG_DATA = 0xF7
  REG_CONTROL = 0xF4
  REG_CONFIG  = 0xF5

  REG_CONTROL_HUM = 0xF2
  REG_HUM_MSB = 0xFD
  REG_HUM_LSB = 0xFE

  # Oversample setting - page 27
  OVERSAMPLE_TEMP = 2
  OVERSAMPLE_PRES = 2
  MODE = 1

  # Oversample setting for humidity register - page 26
  OVERSAMPLE_HUM = 2
  bus.write_byte_data(addr, REG_CONTROL_HUM, OVERSAMPLE_HUM)

  control = OVERSAMPLE_TEMP<<5 | OVERSAMPLE_PRES<<2 | MODE
  bus.write_byte_data(addr, REG_CONTROL, control)

  # Read blocks of calibration data from EEPROM
  # See Page 22 data sheet
  cal1 = bus.read_i2c_block_data(addr, 0x88, 24)
  cal2 = bus.read_i2c_block_data(addr, 0xA1, 1)
  cal3 = bus.read_i2c_block_data(addr, 0xE1, 7)

  # Convert byte data to word values
  dig_T1 = getUShort(cal1, 0)
  dig_T2 = getShort(cal1, 2)
  dig_T3 = getShort(cal1, 4)

  dig_P1 = getUShort(cal1, 6)
  dig_P2 = getShort(cal1, 8)
  dig_P3 = getShort(cal1, 10)
  dig_P4 = getShort(cal1, 12)
  dig_P5 = getShort(cal1, 14)
  dig_P6 = getShort(cal1, 16)
  dig_P7 = getShort(cal1, 18)
  dig_P8 = getShort(cal1, 20)
  dig_P9 = getShort(cal1, 22)

  dig_H1 = getUChar(cal2, 0)
  dig_H2 = getShort(cal3, 0)
  dig_H3 = getUChar(cal3, 2)

  dig_H4 = getChar(cal3, 3)
  dig_H4 = (dig_H4 << 24) >> 20
  dig_H4 = dig_H4 | (getChar(cal3, 4) & 0x0F)

  dig_H5 = getChar(cal3, 5)
  dig_H5 = (dig_H5 << 24) >> 20
  dig_H5 = dig_H5 | (getUChar(cal3, 4) >> 4 & 0x0F)

  dig_H6 = getChar(cal3, 6)

  # Wait in ms (Datasheet Appendix B: Measurement time and current calculation)
  wait_time = 1.25 + (2.3 * OVERSAMPLE_TEMP) + ((2.3 * OVERSAMPLE_PRES) + 0.575) + ((2.3 * OVERSAMPLE_HUM)+0.575)
  time.sleep(wait_time/1000)  # Wait the required time

  # Read temperature/pressure/humidity
  data = bus.read_i2c_block_data(addr, REG_DATA, 8)
  pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
  temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
  hum_raw = (data[6] << 8) | data[7]

  #Refine temperature
  var1 = ((((temp_raw>>3)-(dig_T1<<1)))*(dig_T2)) >> 11
  var2 = (((((temp_raw>>4) - (dig_T1)) * ((temp_raw>>4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
  t_fine = var1+var2
  temperature = float(((t_fine * 5) + 128) >> 8);

  # Refine pressure and adjust for temperature
  var1 = t_fine / 2.0 - 64000.0
  var2 = var1 * var1 * dig_P6 / 32768.0
  var2 = var2 + var1 * dig_P5 * 2.0
  var2 = var2 / 4.0 + dig_P4 * 65536.0
  var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
  var1 = (1.0 + var1 / 32768.0) * dig_P1
  if var1 == 0:
    pressure=0
  else:
    pressure = 1048576.0 - pres_raw
    pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
    var1 = dig_P9 * pressure * pressure / 2147483648.0
    var2 = pressure * dig_P8 / 32768.0
    pressure = pressure + (var1 + var2 + dig_P7) / 16.0

  # Refine humidity
  humidity = t_fine - 76800.0
  humidity = (hum_raw - (dig_H4 * 64.0 + dig_H5 / 16384.0 * humidity)) * (dig_H2 / 65536.0 * (1.0 + dig_H6 / 67108864.0 * humidity * (1.0 + dig_H3 / 67108864.0 * humidity)))
  humidity = humidity * (1.0 - dig_H1 * humidity / 524288.0)
  if humidity > 100:
    humidity = 100
  elif humidity < 0:
    humidity = 0

  return temperature/100.0,pressure/100.0,humidity


# Si1145 part
class SI1145(object):
      def __init__(self, address):

              busnum=I2C.get_default_bus()
              print('I2C Bus Number: '+str(busnum))
              print('I2C Address: '+str(address))

              self._logger = logging.getLogger('SI1145')

              # Create I2C device.
              self._device = I2C.Device(address, busnum)

              #reset device
              self._reset()

              # Load calibration values.
              self._load_calibration()

      # device reset
      def _reset(self):
              self._device.write8(SI1145_REG_MEASRATE0, 0)
              self._device.write8(SI1145_REG_MEASRATE1, 0)
              self._device.write8(SI1145_REG_IRQEN, 0)
              self._device.write8(SI1145_REG_IRQMODE1, 0)
              self._device.write8(SI1145_REG_IRQMODE2, 0)
              self._device.write8(SI1145_REG_INTCFG, 0)
              self._device.write8(SI1145_REG_IRQSTAT, 0xFF)

              self._device.write8(SI1145_REG_COMMAND, SI1145_RESET)
              time.sleep(.01)
              self._device.write8(SI1145_REG_HWKEY, 0x17)
              time.sleep(.01)

      # write Param
      def writeParam(self, p, v):
              self._device.write8(SI1145_REG_PARAMWR, v)
              self._device.write8(SI1145_REG_COMMAND, p | SI1145_PARAM_SET)
              paramVal = self._device.readU8(SI1145_REG_PARAMRD)
              return paramVal

      # load calibration to sensor
      def _load_calibration(self):
              # /***********************************/
              # Enable UVindex measurement coefficients!
              self._device.write8(SI1145_REG_UCOEFF0, 0x29)
              self._device.write8(SI1145_REG_UCOEFF1, 0x89)
              self._device.write8(SI1145_REG_UCOEFF2, 0x02)
              self._device.write8(SI1145_REG_UCOEFF3, 0x00)

              # Enable UV sensor
              self.writeParam(SI1145_PARAM_CHLIST, SI1145_PARAM_CHLIST_ENUV | SI1145_PARAM_CHLIST_ENALSIR | SI1145_PARAM_CHLIST_ENALSVIS | SI1145_PARAM_CHLIST_ENPS1)

              # Enable interrupt on every sample
              self._device.write8(SI1145_REG_INTCFG, SI1145_REG_INTCFG_INTOE)
              self._device.write8(SI1145_REG_IRQEN, SI1145_REG_IRQEN_ALSEVERYSAMPLE)

              # /****************************** Prox Sense 1 */

              # Program LED current
              self._device.write8(SI1145_REG_PSLED21, 0x03) # 20mA for LED 1 only
              self.writeParam(SI1145_PARAM_PS1ADCMUX, SI1145_PARAM_ADCMUX_LARGEIR)

              # Prox sensor #1 uses LED #1
              self.writeParam(SI1145_PARAM_PSLED12SEL, SI1145_PARAM_PSLED12SEL_PS1LED1)

              # Fastest clocks, clock div 1
              self.writeParam(SI1145_PARAM_PSADCGAIN, 0)

              # Take 511 clocks to measure
              self.writeParam(SI1145_PARAM_PSADCOUNTER, SI1145_PARAM_ADCCOUNTER_511CLK)

              # in prox mode, high range
              self.writeParam(SI1145_PARAM_PSADCMISC, SI1145_PARAM_PSADCMISC_RANGE | SI1145_PARAM_PSADCMISC_PSMODE)
              self.writeParam(SI1145_PARAM_ALSIRADCMUX, SI1145_PARAM_ADCMUX_SMALLIR)

              # Fastest clocks, clock div 1
              self.writeParam(SI1145_PARAM_ALSIRADCGAIN, 0)

              # Take 511 clocks to measure
              self.writeParam(SI1145_PARAM_ALSIRADCOUNTER, SI1145_PARAM_ADCCOUNTER_511CLK)

              # in high range mode
              self.writeParam(SI1145_PARAM_ALSIRADCMISC, SI1145_PARAM_ALSIRADCMISC_RANGE)

              # fastest clocks, clock div 1
              self.writeParam(SI1145_PARAM_ALSVISADCGAIN, 0)

              # Take 511 clocks to measure
              self.writeParam(SI1145_PARAM_ALSVISADCOUNTER, SI1145_PARAM_ADCCOUNTER_511CLK)

              # in high range mode (not normal signal)
              self.writeParam(SI1145_PARAM_ALSVISADCMISC, SI1145_PARAM_ALSVISADCMISC_VISRANGE)

              # measurement rate for auto
              self._device.write8(SI1145_REG_MEASRATE0, 0xFF) # 255 * 31.25uS = 8ms

              # auto run
              self._device.write8(SI1145_REG_COMMAND, SI1145_PSALS_AUTO)

      # returns the UV index * 100 (divide by 100 to get the index)
      def readUV(self):
              return self._device.readU16LE(0x2C)

      #returns visible + IR light levels
      def readVisible(self):
              return self._device.readU16LE(0x22)

      #returns IR light levels
      def readIR(self):
              return self._device.readU16LE(0x24)

      # Returns "Proximity" - assumes an IR LED is attached to LED
      def readProx(self):
              return self._device.readU16LE(0x26)

def read_si1145all(address):

  sensor = SI1145(address)
  vis = sensor.readVisible()
  IR = sensor.readIR()
  UV = sensor.readUV()
  uvIndex = UV / 100.0

  return vis,IR,uvIndex
