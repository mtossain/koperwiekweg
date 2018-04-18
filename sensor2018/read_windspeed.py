################################################################################
# Script for measuring wind wind_speed
# M. Tossaint
# v1 2018-02-15
################################################################################

from gpiozero import DigitalInputDevice
from time import sleep
import math

# Connect windspeed on one side to GND and another to GPIO pin
# No resistor needed... Detection on LOW/FALSE
pinReadSpeed = 26       # GPIO Pin for input
count = 0               # Rotation Counter
radius_cm = 9.0		# Radius of the anemometer
interval = 2		# Duration to report on speed
ADJUSTMENT = 1.18	# Adjustment for weight of cups

CM_IN_A_KM = 100000.0
SECS_IN_AN_HOUR = 3600

wind_speed_sensor = DigitalInputDevice(pinReadSpeed,pull_up=True)

def calculate_speed(time_sec):
    global count
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = count / 2.0
    dist_km = (circumference_cm * rotations) / CM_IN_A_KM
    km_per_sec = dist_km / time_sec
    km_per_hour = km_per_sec * SECS_IN_AN_HOUR

    return km_per_hour * ADJUSTMENT

def spin():
    global count
    count = count + 1

wind_speed_sensor.when_activated = spin

def get_windspeed():

    count = 0
    sleep(interval)
    return calculate_speed(interval)
