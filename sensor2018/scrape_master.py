import os
import time
import requests
import serial
import mysql.connector
import shelve
from datetime import datetime
import math
import json
import urllib2
from dateutil.parser import *
import datetime as dt

PasswordFTP = open('/home/pi/AuthBhostedFTP.txt','r').read().split('\n')[0]
PasswordMysql = open("/home/pi/AuthBhostedMysql.txt",'r').read().split('\n')[0]
ram_drive="/ramtmp/"

###############################################################################
# PART 1: Camera image
now = time.strftime("%Y-%m-%d %H:%M:%S")
print(now+' *** 1 - Generate Fisheye')
os.system("convert -size 2592x1944 xc:none -fill back1.png -draw 'circle 1296,972 1296,1' "+ram_drive+"back2.png") # cut out the circle
os.system("convert "+ram_drive+"back2.png -crop 1944x1944+325+00 "+ram_drive+"back3.png") # take square around circle
os.system("convert "+v+"back3.png -resize 1024x1024 "+ram_drive+"back4.png") # take square around circle
os.system("convert -size 1024x1024 xc:none "+ram_drive+"back4.png -rotate '-90' -composite "+ram_drive+"dome.png") # rotate around axis
print(now+' *** 2 - Move fisheye to FTP server')
try:
    FileName = ram_drive+"dome.png"
    file = open(FileName,'rb') # file to send
    session = ftplib.FTP('s14.servitnow.nl','hjvveluw',PasswordFTP,timeout=30)
    session.cwd('/domains/koperwiekweg.nl/public_html')
    session.storbinary('STOR dome.png', file) # send the file
    file.close() # close file and FTP
    session.quit()
    print(now +' Uploaded fisheye '+FileName+' to FTP [OK]')
except (socket.error, ftplib.all_errors) as e:
    print (e)
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    print(now + ' Could not upload fisheye '+FileName+' to FTP [NOK]')
print(now+' *** 3 - Copy image on server to avoid partly images on website when FTP ongoing')
try:
    r = requests.get('http://www.koperwiekweg.nl/copy_dome.php',timeout=15)
except (requests.ConnectionError, requests.Timeout, socket.timeout) as e:
    print (e)
    print(now +' Could not copy dome.png on server [NOK]')

###############################################################################
# PART 2: Get the rain and lightning data
rain=0
rain_rate=0
lightning_distance=0
    #
###############################################################################
# PART 3: Weather station data
shelve = shelve.open(ram_drive+"data_slave.db")
temperature=shelve['temperature']
pressure=shelve['pressure']
humidity=shelve['humidity']
wind_speed=shelve['wind_speed']
wind_dir_str=shelve['wind_dir_str']
wind_dir_angle=shelve['wind_dir_angle']
uv_index=shelve['uv_index']
light_intensity=shelve['light_intensity']

now = time.strftime("%Y-%m-%d %H:%M:%S")
print(now + ' T:'+str(temperature)+ ' P:'+str(pressure)+' H:'+str(humidity)+' R:'+str(rain)+' W:'+str(wind_speed)+
' WD:'+wind_dir_str+' WDA:'+str(wind_dir_angle)+' UVI:'+str(uv_index)+' LI:'+str(light_intensity))

try:
    cnx = mysql.connector.connect(
         host="127.0.0.1", # your host, usually localhost
         port=3306,
         user="hjvveluw_mtossain", # your username
         passwd=PasswordMysql, # your password
         database="hjvveluw_wopr") # name of the data base

    # Use all the SQL you like
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO AcuRiteSensor (SensorDateTime, Temperature, Pressure, Humidity, WindSpeed, WindDirection, WindDirectionAngle, Rainfall, RainfallRate, UVIndex,TransmitPowerkW, SunPower, LightningDist) " +
                                   "VALUES ('" + now + "','" + str(temperature)+ "','" + str(pressure)+ "','" + str(humidity)+ "','" + str(wind_speed)+ "','" + wind_dir_str+ "','" + str(wind_dir_angle)+ "','" + str(rain)+ "','" + str(rain_rate)+ "','" + str(uv_index)+ "','" + str(0)+ "','" + str(light_intensity) + "','" + str(lightning_distance) + "')")
    cnx.commit()
    cursor.close()
    cnx.close()

    print('Data uploaded to database [OK]')

except mysql.connector.Error as err:
    print("Could not connect to database [NOK]")
    print(err)

shelve.close()

###############################################################################
# PART 3: Upload to wunderground
#
now = time.strftime("%Y-%m-%d %H:%M:%S")
print(now + ' Upload to Wunderground')
temp_str = "{0:.2f}".format(degc_to_degf(temperature))
ground_temp_str = "{0:.2f}".format(degc_to_degf(temperature))
humidity_str = "{0:.2f}".format(humidity)
pressure_in_str = "{0:.2f}".format(hpa_to_inches(pressure))
wind_speed_mph_str = "{0:.2f}".format(kmh_to_mph(wind_speed))
wind_gust_mph_str = "{0:.2f}".format(kmh_to_mph(wind_speed))
wind_average_str = str(wind_speed)
rainfall_in_str = "{0:.2f}".format(mm_to_inches(rain_rate))
daily_rainfall_in_str = "{0:.2f}".format(mm_to_inches(rain))
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

now = time.strftime("%Y-%m-%d %H:%M:%S")
print(now+" Received " + str(r.status_code) + " " + str(r.text))
