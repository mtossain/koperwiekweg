import shelve
import datetime
import os
import random
import time
import json
import math
import numpy as np
from read_winddir import *
from read_windspeed import *

# Compute the values over the last 10mn: meanspeed, maxspeed, meandir

ram_drive            = '/ramtmp/'
shelve_wind          = ram_drive+'wind.db'

def nowStr():
    return( datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))

def meanangle(angles,weights=0,setting='degrees'):
    '''computes the mean angle'''
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
     if (deg<0):
        deg=deg+360
     arr = ['NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N']
     return arr[int(abs((deg - 11.25) % 360)/ 22.5)]



def getDir():
    try:
        wind_dir_angle, wind_dir_str = get_wind_dir_all()
    except:
        print('[NOK] '+nowStr()+' Could not find the data from the Wind direction sensor')
    return wind_dir_angle

def getSpeed():
    try:
        wind_speed = get_windspeed()
    except:
        print('[NOK] '+nowStr()+' Could not find the data from the Wind speed sensor')
    return wind_speed

speed_list = [getSpeed()] # initialise the list
dir_list = [getDir()] # initialise the list

# Main loop
while(1):
    for i in range(30):
        speed = getSpeed()
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
    dirstr_last10 = deg2compass(dir_last10)

    # save to file
    d = shelve.open(shelve_wind) # Save the data to file
    d['wind_10mn_speed']=speed_last10
    d['wind_10mn_gust']=gust_last10
    d['wind_10mn_dir_angle']=dir_last10
    d['wind_10mn_dir_str']=dirstr_last10
    d.close()

    print('[OK] ' + nowStr() + ' v_avg:'+str(speed_last10)+\
    ' [km/h] v_max:'+str(gust_last10)+\
    ' [km/h] ang:'+str(dir_last10)+\
    ' [deg] ang_str:'+str(dirstr_last10)
    )
