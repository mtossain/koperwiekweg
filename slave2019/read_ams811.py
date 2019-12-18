#this example reads and prints CO2 equiv. measurement, TVOC measurement, and temp every 2 seconds

from time import sleep
from Adafruit_CCS811 import Adafruit_CCS811


def get_ams811_data(temperature):
    ccs =  Adafruit_CCS811()
    while not ccs.available():
        pass

    ccs.tempOffset = temperature - 25.0

    if ccs.available():
        temp = ccs.calculateTemperature()
        if not ccs.readData():
            return ccs.geteCO2(),ccs.getTVOC()
