###############################################################################
# Read all sensor data (except rain & lightning) and push to wunderground
# 2018 - M.Tossaint
###############################################################################

from read_bme280 import *
temperature_bme280,pressure,humidity = readBME280All()

from read_mcp9898 import *
temperature = get_temp_mcp9808()

from read_si1145 import *
vis,IR,uv_index = read_si1145all()

from read_winddir import *
wind_dir_angle, wind_dir_str = get_wind_dir_all()

from read_windspeed import *
wind_speed = get_windspeed()

# MAKE THE CAMERA PICTURE
# TBD

import requests

def hpa_to_inches(pressure_in_hpa):
    pressure_in_inches_of_m = pressure_in_hpa * 0.02953
    return pressure_in_inches_of_m

def mm_to_inches(rainfall_in_mm):
    rainfall_in_inches = rainfall_in_mm * 0.0393701
    return rainfall_in_inches

def degc_to_degf(temperature_in_c):
    temperature_in_f = (temperature_in_c * (9/5.0)) + 32
    return temperature_in_f

def kmh_to_mph(speed_in_kmh):
    speed_in_mph = speed_in_kmh * 0.621371
    return speed_in_mph

# TBD TBD


ground_temp = 0 # soil temp

wind_speed = 5.6129 # kmph
wind_gust = 12.9030 # kmph
wind_average = 180 # wind direction
rainfall = 2.270 # goes to mm/hr
dailyrainfall = 13.0 # total rain today in mm


temp_str = "{0:.2f}".format(degc_to_degf(temperature))
ground_temp_str = "{0:.2f}".format(degc_to_degf(ground_temp))
humidity_str = "{0:.2f}".format(humidity)
pressure_in_str = "{0:.2f}".format(hpa_to_inches(pressure))
wind_speed_mph_str = "{0:.2f}".format(kmh_to_mph(wind_speed))
wind_gust_mph_str = "{0:.2f}".format(kmh_to_mph(wind_gust))
wind_average_str = str(wind_average)
rainfall_in_str = "{0:.2f}".format(mm_to_inches(rainfall))
daily_rainfall_in_str = "{0:.2f}".format(mm_to_inches(dailyrainfall))
uv_str = str(uv_index)

# create a string to hold the first part of the URL
WUurl = 'https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?'
WU_station_id = "IIJSSELS27" # Replace XXXX with your PWS ID
WU_station_pwd = "t1j51fnq" # Replace YYYY with your Password
WUcreds = "ID=" + WU_station_id + "&PASSWORD="+ WU_station_pwd
date_str = "&dateutc=now"
action_str = "&action=updateraw"

r= requests.get(
    WUurl +
    WUcreds +
    date_str +
    "&humidity=" + humidity_str +
    "&baromin=" + pressure_in_str +
    "&windspeedmph=" + wind_speed_mph_str +
    "&windgustmph=" + wind_gust_mph_str +
    "&tempf=" + temp_str +
    "&dailyrainin=" + daily_rainfall_in_str +
    "&rainin=" + rainfall_in_str +
    "&soiltempf=" + ground_temp_str +
    "&winddir=" + wind_average_str +
    "&UV=" + uv_str +
    action_str)

print("Received " + str(r.status_code) + " " + str(r.text))
