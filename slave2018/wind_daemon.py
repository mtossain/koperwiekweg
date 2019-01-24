import shelve
import datetime
import os
import random
import time
import json
import math
import numpy as np
import rpyc

from read_winddir import *
from read_windspeed import *
CRED = '\033[91m'
CGREEN = '\033[92m'
CEND = '\033[0m'

# Compute the values over the last 10mn: meanspeed, maxspeed, meandir

ftp_server           = '192.168.178.11'
WeatherService = rpyc.connect(ftp_server, 18861)

def nowStr():
    return( datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))

def meanangle(angles,weights=0,setting='degrees'):
    #computes the mean angle
    if weights==0:
         weights=np.ones(len(angles))
    sumsin=0
    sumcos=0
    if setting=='degrees':
        angles=np.array(angles)*math.pi/180
    for i in range(len(angles)):
        sumsin+=weights[i]/sum(weights)*math.sin(angles[i])
        sumcos+=weights[i]/sum(weights)*math.cos(angles[i])
    average=math.atan2(sumsin,sumcos)
    if setting=='degrees':
        average=average*180/math.pi
    return average

def deg2compass(deg):
     arr = ['NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N']
     return arr[int(abs((deg - 11.25) % 360)/ 22.5)]

def getDir():
    wind_dir_angle = 0
    wind_dir_str = ''
    try:
        wind_dir_angle, wind_dir_str = get_wind_dir_all()
    except:
        print(CRED+'[NOK] '+nowStr()+' Could not find the data from the Wind direction sensor'+CEND)
    return wind_dir_angle

def getSpeed():
    wind_speed=0
    try:
        wind_speed = get_windspeed()
    except:
        print(CRED+'[NOK] '+nowStr()+' Could not find the data from the Wind speed sensor'+CEND)
    return wind_speed

speed_list = [getSpeed()] # initialise the list
dir_list = [getDir()] # initialise the list

# Main loop
while(1):
    for i in range(30):
        speed = round(getSpeed(),1)
        dir = getDir()
        if len(speed_list)<(10*60): # still filling the last 10 min
            speed_list.insert(0,speed)
            dir_list.insert(0,dir)
        else: # list is full, add to start and add first
            speed_list.pop()
            dir_list.pop()
            speed_list.insert(0,speed)
            dir_list.insert(0,dir)

    speed_last10 = round(sum(speed_list) / float(len(speed_list)),1)
    gust_last10 = round(max(speed_list),1)
    dir_last10 = round(meanangle(dir_list,0,'degrees'),1)
    if dir_last10 < 0:
       dir_last10 = dir_last10 + 360
    dirstr_last10 = deg2compass(dir_last10)

    #print(speed_list[0:15])
    #print(dir_list[0:15])

    try:
        WeatherService.root.update_sensor_wind(speed_last10,dirstr_last10,dir_last10)
        print(CGREEN+'[OK] ' + nowStr() + ' v_avg:'+str(speed_last10)+\
        ' [km/h] v_max:'+str(gust_last10)+\
        ' [km/h] ang:'+str(dir_last10)+\
        ' [deg] '+str(dirstr_last10)+\
        CEND)
    except:
        print(CRED+'[NOK] Could not update weather service...'+CEND)
    time.sleep(5)
