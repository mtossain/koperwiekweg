import os
import time
import requests
import serial
import mysql.connector
import subprocess
import shelve
from datetime import datetime
import math
import json
import urllib2
from dateutil.parser import *
import datetime as dt

PasswordMysql = open("/home/pi/AuthBhostedMysql.txt",'r').read().split('\n')[0]

# Get the values from a previous run
shelve = shelve.open("config.db")
Temp=shelve['Temp']
Baro=shelve['Baro']
Humid=shelve['Humid']
Rain=shelve['Rain']
Wind=shelve['Wind']
WindDir=shelve['WindDir']
WindDirAngle=shelve['WindDirAngle']
UVIndex=shelve['UVIndex']
SunPower=0
TransmitPower=0
RainRate=0
LightningDist=0

# TBD Read the rain and lightning data from the RTLSDR WindDirectionAngle
# Publish that to wunderground

try:

    f = urllib2.urlopen('http://api.wunderground.com/api/c76852885ada6b8a/conditions/q/pws:IIJSSELS30.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)
    station_time = parse(parsed_json['current_observation']['observation_time_rfc822']).replace(tzinfo=None)
    now = dt.datetime.now()
    seconds = (now-station_time).total_seconds()
    if seconds > 5*60:
        print('Station IIJSELS30 is not updated since: '+str(int(seconds/60))+'min, taking Ijsselstein [NOK]')
        f = urllib2.urlopen('http://api.wunderground.com/api/c76852885ada6b8a/conditions/q/Ijsselstein.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
    #print(json.dumps(parsed_json, sort_keys=True,indent=4, separators=(',', ': ')))
    Baro = int(float(parsed_json['current_observation']['pressure_mb']))
    Temp = float(parsed_json['current_observation']['temp_c'])

    Wind = int(float(parsed_json['current_observation']['wind_kph']))
    WindDir = parsed_json['current_observation']['wind_dir']
    WindDirAngle = int(float(parsed_json['current_observation']['wind_degrees']))

    try:
        Rain = int(float(parsed_json['current_observation']['precip_today_metric']))
    except:
        Rain = shelve['Rain']

    humidity_str = parsed_json['current_observation']['relative_humidity']
    Humid = int(float(humidity_str[:-1]))
    if (Humid > 30):
	HumidReadings.append(Humid)
    Humid = mean(HumidReadings)
    if len(HumidReadings) == max_samples:
        HumidReadings.pop(0)

    if Temp<-50 or Temp>75:
        Temp = shelve['Temp']
    if Baro<750 or Baro>1250:
        Baro = shelve['Baro']
    if Wind<0 or Wind>500:
        Wind = shelve['Wind']
    if Humid<30 or Humid>100:
        Humid = shelve['Humid']
    if Rain<0 or Rain>100:
        Rain = shelve['Rain']

    shelve['Temp']=Temp
    shelve['Baro']=Baro
    shelve['Humid']=Humid
    shelve['Rain']=Rain
    shelve['Wind']=Wind
    shelve['WindDir']=WindDir
    shelve['WindDirAngle']=WindDirAngle
    print('Found data from wunderground.com [OK]')

except requests.exceptions.RequestException as e:
    print('Could not get the Aculink webpage [NOK]')
    Temp=shelve['Temp']
    Baro=shelve['Baro']
    Humid=shelve['Humid']
    Rain=shelve['Rain']
    Wind=shelve['Wind']
    WindDir=shelve['WindDir']
    WindDirAngle=shelve['WindDirAngle']

now = time.strftime("%Y-%m-%d %H:%M:%S")
print(now + ' T:'+str(Temp)+ ' P:'+str(Baro)+' H:'+str(Humid)+' R:'+str(Rain)+' W:'+str(Wind)+' WD:'+WindDir+' WDA:'+str(WindDirAngle)+' UVI:'+str(UVIndex)+' LD:'+str(LightningDist))

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
                                   "VALUES ('" + now + "','" + str(Temp)+ "','" + str(Baro)+ "','" + str(Humid)+ "','" + str(Wind)+ "','" + WindDir+ "','" + str(WindDirAngle)+ "','" + str(Rain)+ "','" + str(RainRate)+ "','" + str(UVIndex)+ "','" + str(TransmitPower)+ "','" + str(SunPower) + "','" + str(LightningDist) + "')")
    cnx.commit()
    cursor.close()
    cnx.close()

    print('Data uploaded to database [OK]')

except mysql.connector.Error as err:
    print("Could not connect to database [NOK]")
    print(err)

shelve.close()
