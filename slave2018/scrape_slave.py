###############################################################################
# Read all sensor data (except rain & lightning) and push to master
# 2018 - M.Tossaint
###############################################################################
import os
import shelve
import ftplib
import datetime
import rpyc
CRED = '\033[91m'
CGREEN = '\033[92m'
CEND = '\033[0m'

flag_upload_to_master = True
flag_camera           = True

ftp_server            = next(open('/home/pi/MasterIP.txt')) 
ftp_username          = 'pi'
ftp_password          = open("/home/pi/AuthMasterPi.txt",'r').read().split('\n')[0]
local_path            = '/ramtmp/'
WeatherService = rpyc.connect(ftp_server, 18861)

def nowStr():
    return( datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))

# Read the sensor data
from read_bme280 import *
pressure=0
humidity=0
try:
    temperature_bme280,pressure,humidity = readBME280All()
    temperature_bme280 = round(temperature_bme280,1)
    pressure = round(pressure,1)
    humidity = round(humidity,1)
    print('[OK]  '+nowStr()+' BME280 T: '+str(temperature_bme280)+' [degC] P: '+str(pressure) + ' [mBar] H: '+str(humidity)+' [%]')
except:
    print(CRED+'[NOK] '+nowStr()+' Could not find the data from the BME280 pressure and humidity'+CEND)

from read_mcp9808 import *
temperature=0
try:
    temperature = get_temp_mcp9808()
    temperature = round(temperature,1)
    print('[OK]  '+nowStr()+' MCP9808 T: '+str(temperature)+' [degC]')
except:
    print(CRED+'[NOK] '+nowStr()+' Could not find MCP9808 temperature'+CEND)

from read_si1145 import *
light_intensity=0
ir_value=0
uv_index=0
try:
    light_intensity,ir_value,uv_index = read_si1145all()
    print('[OK]  '+nowStr()+' SI1145 I: '+str(light_intensity)+' [-] IR: '+str(ir_value)+' [-] UV: '+str(uv_index)+' [-]')
except:
    print(CRED+'[NOK] '+nowStr()+' Could not find SI1145 light and uv_index'+CEND)


if flag_camera:
    try:
        os.system('raspistill -o '+local_path+'cam.jpg') # Take the camera image
        print('[OK]  '+nowStr()+' Got the camera image: '+local_path+'cam.jpg')
    except:
        print(CRED+'[NOK] '+nowStr()+' Could not take the camera image'+CEND)

try:
    WeatherService.root.update_sensor_2018(temperature,pressure,humidity,uv_index,light_intensity)
    print(CGREEN+'[OK] Uploaded data to weather server'+CEND)
except:
    print(CRED+'[NOK] Could not update weather service...'+CEND)


if flag_upload_to_master:
    try:
        if flag_camera:
            fh2 = open(local_path+"cam.jpg", 'rb')
            ftp_connection.storbinary('STOR /ramtmp/cam.jpg', fh2)
            fh2.close()
        print('[OK]  '+nowStr()+' Uploaded data to the ftp master: '+ftp_server)
    except:
        print(CRED+'[NOK] '+nowStr()+' Could not upload the data to the master.'+CEND)
