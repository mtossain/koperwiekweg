###############################################################################
# Read all sensor data (except rain & lightning) and push to master
# 2018 - M.Tossaint
###############################################################################
import os
import shelve
import ftplib
import datetime
import rpyc
import logging
import math
import time
import I2C
from read_mcp9808 import *
from read_si1145 import *
import smooth

CRED = '\033[91m'
CGREEN = '\033[92m'
CEND = '\033[0m'

flag_upload_to_master = False
flag_camera           = False

ftp_server            = next(open('/home/pi/MasterIP.txt'))
ftp_username          = 'pi'
ftp_password          = open("/home/pi/AuthMasterPi.txt",'r').read().split('\n')[0]
local_path            = '/ramtmp/'
WeatherService = rpyc.connect(ftp_server, 18861)

def nowStr():
    return( datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))

temperature_s = smooth.Smooth(5,5)
pressure_s = smooth.Smooth(5,5)
humidity_s = smooth.Smooth(5,5)

for i in range(1):
#while (True):

    # Read the sensor data
    pressure=0
    humidity=0
    temperature_bme280=0
    try:
        #temperature_bme280,pressure,humidity = read_bme280.readBME280All(0x76)
        temperature_bme280 = round(temperature_bme280,1)
        pressure=round(pressure_s.add_step(pressure),1) # smooth the data
        humidity=round(humidity_s.add_step(humidity),1) # smooth the data
        print('[OK]  '+nowStr()+' BME280 T: '+str(temperature_bme280)+' [degC] P: '+str(pressure) + ' [mBar] H: '+str(humidity)+' [%]')
    except:
        print(CRED+'[NOK] '+nowStr()+' Could not find the data from the BME280 pressure and humidity'+CEND)

    temperature=0
    try:
        temperature = read_mcp9808.get_temp_mcp9808(0x18)
        temperature=round(temperature_s.add_step(temperature),1) # smooth the data
        print('[OK]  '+nowStr()+' MCP9808 T: '+str(temperature)+' [degC]')
    except:
        print(CRED+'[NOK] '+nowStr()+' Could not find MCP9808 temperature'+CEND)

    light_intensity=0
    ir_value=0
    uv_index=0
    try:
        light_intensity,ir_value,uv_index = read_si1145.read_si1145all(0x60)
        print('[OK]  '+nowStr()+' SI1145 I: '+str(light_intensity)+' [-] IR: '+str(ir_value)+' [-] UV: '+str(uv_index)+' [-]')
    except:
        print(CRED+'[NOK] '+nowStr()+' Could not find SI1145 light and uv_index'+CEND)

    if flag_camera:
        try:
            os.system('raspistill -h 1054 -w 1054 -o '+local_path+'cam.jpg') # Take the camera image
            print('[OK]  '+nowStr()+' Got the camera image: '+local_path+'cam.jpg')
        except:
            print(CRED+'[NOK] '+nowStr()+' Could not take the camera image'+CEND)


    if flag_upload_to_master:
        try:
            WeatherService.root.update_sensor_2018(temperature,pressure,humidity,uv_index,light_intensity)
            print(CGREEN+'[OK] Uploaded data to weather server'+CEND)
        except:
            print(CRED+'[NOK] Could not update weather service...'+CEND)


        try:
            if flag_camera:
                ftp_connection = ftplib.FTP(ftp_server, ftp_username, ftp_password)
                fh2 = open(local_path+"cam.jpg", 'rb')
                ftp_connection.storbinary('STOR /ramtmp/cam.jpg', fh2)
                fh2.close()
            print('[OK]  '+nowStr()+' Uploaded data to the ftp master: '+ftp_server)
        except:
            print(CRED+'[NOK] '+nowStr()+' Could not upload the data to the master.'+CEND)

    time.sleep(10)
