import os
import time
import requests
import serial
import mysql.connector
import shelve
from datetime import datetime
import math
import json
import rpyc
import datetime as dt
import datetime
import ftplib
CRED   ='\033[91m'
CGREEN ='\033[92m'
CEND   ='\033[0m'

###############################################################################
# CONFIGURATION
upload_fisheye       = True
upload_database      = True
upload_wunderground  = True
read_master          = True
read_slave           = True

WU_url               = 'https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?'
WU_station_id        = "IIJSSELS27" # ID
WU_station_pwd       = "t1j51fnq" # PASS

PasswordFTP          = open('/home/pi/AuthBhostedFTP.txt','r').read().split('\n')[0]
PasswordMysql        = open("/home/pi/AuthBhostedMysql.txt",'r').read().split('\n')[0]
database_user        = "hjvveluw_mtossain"
database_pass        = "hjvveluw_wopr"
ram_drive            = "/ramtmp/"
WeatherService = rpyc.connect("localhost", 18861)

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
def nowStr():
    return( datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))

###############################################################################
# PART 1: Camera image
if upload_fisheye:
    try:
        print('*** Converting camera fisheye image')
        os.system("convert "+ram_drive+"cam.jpg -page -20+35 -background none -flatten "+ram_drive+"back.jpg") # translate the image to the middle
        os.system("convert -size 1024x1024 xc:none -fill "+ram_drive+"back.jpg -draw 'circle 512,512 20,512' "+ram_drive+"back2.png") # cut out the circle
        os.system("convert -size 1024x1024 xc:none "+ram_drive+"back2.png -rotate '-90' -flop  -composite "+ram_drive+"dome.png") # rotate around axis
        print('[OK] '+nowStr()+' Converted camera image')
    except:
        print(CRED+'[NOK] '+nowStr()+' Could not convert camera image'+CEND)
    try:
        FileName = ram_drive+"dome.png"
        file = open(FileName,'rb') # file to send
        session = ftplib.FTP('s14.servitnow.nl','hjvveluw',PasswordFTP,timeout=30)
        session.cwd('/domains/koperwiekweg.nl/public_html')
        session.storbinary('STOR dome.png', file) # send the file
        file.close() # close file and FTP
        session.quit()
        print('[OK] '+nowStr() +' Uploaded fisheye '+FileName+' to FTP')
    except (ftplib.all_errors) as e:
        print (e)
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        print(CRED+'[NOK] '+nowStr() + ' Could not upload fisheye '+FileName+' to FTP'+CEND)

    try:
        r = requests.get('http://www.koperwiekweg.nl/copy_dome.php',timeout=15)
        print('[OK] '+nowStr()+' Copied image on server to avoid partly images on website when FTP ongoing')
    except (requests.ConnectionError, requests.Timeout, socket.timeout) as e:
        print (e)
        print(CRED+'[NOK] '+nowStr()+' Could not copy dome.png on server'+CEND)


###############################################################################
# Get the data from the weather server
try:
    temperature,pressure,humidity,rain,rain_rate,wind_speed,wind_dir_str,wind_dir_angle,uv_index,light_intensity = WeatherService.root.get_all()
    print(CGREEN+'[OK] ' + nowStr() + ' T:'+str(temperature)+ ' P:'+str(pressure)+' H:'+\
    str(humidity)+' R:'+str(rain)+' W:'+str(wind_speed)+' WD:'+wind_dir_str+\
    ' WDA:'+str(wind_dir_angle)+' UVI:'+str(uv_index)+' LI:'+str(light_intensity)+CEND)
except:
    print(CRED+'[NOK] Could not connect to weather server'+CEND)


###############################################################################
# PART 4: Write data to database
if upload_database and pressure>500: # valid data
    try:
        cnx = mysql.connector.connect(
             host="127.0.0.1", # your host, usually localhost
             port=3306,
             user=database_user, # your username
             passwd=PasswordMysql, # your password
             database='hjvveluw_wopr') # name of the data base
        cursor = cnx.cursor() # Use all the SQL you like
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO AcuRiteSensor (SensorDateTime, Temperature, Pressure, Humidity, " + \
        "WindSpeed, WindDirection, WindDirectionAngle, Rainfall, RainfallRate, UVIndex,TransmitPowerkW, SunPower, LightningDist) VALUES " + \
        "(\'"+ now +"\',\'" + str(temperature)+ "\',\'" + str(pressure)+ "\',\'" + \
        str(humidity)+ "\',\'" + str(wind_speed)+ "\',\'" + wind_dir_str+ "\',\'" + str(wind_dir_angle)+ \
        "\',\'" + str(rain)+ "\',\'" + str(rain_rate)+ "\',\'" + str(uv_index)+ "\',\'" + str(0)+ "\',\'" + \
        str(light_intensity) + "\',\'" + str(99999) + "\')")
        cnx.commit()
        cursor.close()
        cnx.close()
        print('[OK] ' + nowStr() + ' Data uploaded to database')
    except mysql.connector.Error as err:
        print('[NOK] ' + nowStr() + ' Could not connect to database [NOK]')
        print(err)


###############################################################################
# PART 5: Upload to wunderground
if upload_wunderground:

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

    try:
        r= requests.get(
            WU_url +
            "ID=" + WU_station_id + "&PASSWORD="+ WU_station_pwd +
            "&dateutc=now" +
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
            "&action=updateraw")
        print('[OK] '+nowStr() +' Received Wunderground status code: ' + str(r.status_code) + ' ' + str(r.text))
    except:
        print('[NOK] '+nowStr()+' Could not upload to Wunderground with status code: '+ str(r.status_code) + ' ' + str(r.text))
