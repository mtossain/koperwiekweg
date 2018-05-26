###############################################################################
# Read all sensor data (except rain & lightning) and push to master
# 2018 - M.Tossaint
###############################################################################
import os
import shelve
import ftplib
import datetime

upload_to_master = True
ftp_server = '192.168.1.156'
ftp_username = 'pi'
ftp_password = open("/home/pi/AuthMasterPi.txt",'r').read().split('\n')[0]
local_path = '/ramtmp/'
shelve_name_slave = local_path + 'data_slave.db'

def nowStr():
    return( datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))

# Read the sensor data
from read_bme280 import *
try:
    temperature_bme280,pressure,humidity = readBME280All()
    temperature_bme280 = round(temperature_bme280,1)
    pressure = round(pressure,1)
    humidity = round(humidity,1)
    print('[OK] '+nowStr()+' BME280 Temperature: '+str(temperature_bme280)+' Pressure: '+str(pressure) + ' Humidity: '+str(humidity))
except:
    print('[NOK] '+nowStr()+' Could not find the data from the BME280 pressure and humidity')

from read_mcp9808 import *
try:
    temperature = get_temp_mcp9808()
    temperature = round(temperature,1)
    print('[OK] '+nowStr()+' MCP9808 Temperature: '+str(temperature))
except:
    print('[NOK] '+nowStr()+' Could not find the data from the MCP9808 temperature')

from read_si1145 import *
try:
    light_intensity,ir_value,uv_index = read_si1145all()
    print('[OK] '+nowStr()+' SI1145 Intensity: '+str(light_intensity)+' IR: '+str(ir_value)+' UV: '+str(uv_index))
except:
    print('[NOK] '+nowStr()+' Could not find the data from the SI1145 light and uv_index')

from read_winddir import *
try:
    wind_dir_angle, wind_dir_str = get_wind_dir_all()
    print('[OK] '+nowStr()+' Wind Angle: '+str(wind_dir_angle)+' Wind Dir: '+wind_dir_str)
except:
    print('[NOK] '+nowStr()+' Could not find the data from the Wind direction sensor')

from read_windspeed import *
try:
    wind_speed = get_windspeed()
    wind_speed = round(wind_speed,1)
    print('[OK] '+nowStr()+' Wind Speed: '+str(wind_speed))
except:
    print('[NOK] '+nowStr()+' Could not find the data from the Wind speed sensor')

try:
    os.system('raspistill -o '+local_path+'cam.jpg') # Take the camera image
    print('[OK] '+nowStr()+' Got the camera image: '+local_path+'cam.jpg')
except:
    print('[NOK] '+nowStr()+' Could not take the camera image')

try:
    #shelve = shelve.open('data_slave.db') # Save the data to file
    shelve = shelve.open(shelve_name_slave) # Save the data to file
    shelve['temperature']=temperature
    shelve['pressure']=pressure
    shelve['humidity']=humidity
    shelve['wind_speed']=wind_speed
    shelve['wind_dir_str']=wind_dir_str
    shelve['wind_dir_angle']=wind_dir_angle
    shelve['uv_index']=uv_index
    shelve['light_intensity']=light_intensity
    shelve.close()
    print('[OK] '+nowStr()+' Shelved the data to file: '+shelve_name_slave)
except:
    print('[NOK] '+nowStr()+' Could not shelve the data')

if upload_to_master:
    try:
        ftp_connection = ftplib.FTP(ftp_server, ftp_username, ftp_password)
        fh = open(local_path+"data_slave.db", 'rb')
        ftp_connection.storbinary('STOR data_slave.db', fh)
        fh2 = open(local_path+"cam.jpg", 'rb')
        ftp_connection.storbinary('STOR cam.jpg', fh2)
        fh2.close()
        print('[OK] '+nowStr()+' Uploaded data to the ftp master: '+ftp_server)
    except:
        print('[NOK] '+nowStr()+' Could not upload the data to the master.')
