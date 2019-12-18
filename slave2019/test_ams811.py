#this example reads and prints CO2 equiv. measurement, TVOC measurement, and temp every 2 seconds
import os
import time
from time import sleep
from Adafruit_CCS811 import Adafruit_CCS811
os.system('modprobe i2c_bcm2835 baudrate=10000')
time.sleep(3)

ccs =  Adafruit_CCS811()
while not ccs.available():
    pass

ccs.tempOffset = 20 - 25.0

if ccs.available():
    temp = ccs.calculateTemperature()
    if not ccs.readData():
        print('CO2: '+str(ccs.geteCO2())+' TVOC: '+str(ccs.getTVOC()))

os.system('modprobe i2c_bcm2835 baudrate=400000')
time.sleep(3)
