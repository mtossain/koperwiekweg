###############################################################################
# Read all sensor data (except rain & lightning) and push to master
# 2018 - M.Tossaint
###############################################################################
import os
import shelve
import ftplib

ftp_server = '192.168.1.156'
ftp_username = 'pi'
ftp_password = open("/home/pi/AuthMasterPi.txt",'r').read().split('\n')[0]
ftp_remote_path = "/home/pi/"

# Get the values from the last run
shelve = shelve.open("data_slave.db") # Save the data to file
temperature=shelve['temperature']
pressure=shelve['pressure']
humidity=shelve['humidity']
wind_speed=shelve['wind_speed']
wind_dir_str=shelve['wind_dir_str']
wind_dir_angle=shelve['wind_dir_angle']
uv_index=shelve['uv_index']
light_intensity=shelve['light_intensity']

# Read the sensor data
from read_bme280 import *
try:
    temperature_bme280,pressure,humidity = readBME280All()
    print('[OK] T_BME280: '+str(temperature_bme280)+' P: '+str(pressure) + ' H: '+str(humidity))
except:
    print('[NOK] Could not find the data from the BME280 pressure and humidity')

from read_mcp9808 import *
try:
    temperature = get_temp_mcp9808()
    print('[OK] T_MCP9808: '+str(temperature))
except:
    print('[NOK] Could not find the data from the MCP9808 temperature')

from read_si1145 import *
try:
    light_intensity,ir_value,uv_index = read_si1145all()
    print('[OK] L: '+str(light_intensity)+' IR: '+str(ir_value)+' UV: '+str(uv_index))
except:
    print('[NOK] Could not find the data from the SI1145 light and uv_index')

from read_winddir import *
try:
    wind_dir_angle, wind_dir_str = get_wind_dir_all()
    print('[OK] WA: '+str(wind_dir_angle)+' WD'+wind_dir_str)
except:
    print('[NOK] Could not find the data from the Wind direction sensor')

from read_windspeed import *
try:
    wind_speed = get_windspeed()
    print('[OK] W: '+str(wind_speed))
except:
    print('[NOK] Could not find the data from the Wind speed sensor')

try:
    os.system('raspistill -o cam.jpg') # Take the camera image
    print('[OK] Got the camera image')
except:
    print('[NOK] Could not take the camera image')

try:
    shelve['temperature']=temperature
    shelve['pressure']=pressure
    shelve['humidity']=humidity
    shelve['wind_speed']=wind_speed
    shelve['wind_dir_str']=wind_dir_str
    shelve['wind_dir_angle']=wind_dir_angle
    shelve['uv_index']=uv_index
    shelve['light_intensity']=light_intensity
    shelve.close()
except:
    print('[NOK] Could not shelve the data')

try:
    ftp_connection = ftplib.FTP(ftp_server, ftp_username, ftp_password)
    ftp_connection.cwd(ftp_remote_path)
    fh = open("data_slave.db", 'rb')
    ftp_connection.storbinary('STOR data_slave.db', fh)
    fh = open("cam.jpg", 'rb')
    ftp_connection.storbinary('STOR cam.jpg', fh)
    fh.close()
except:
    print('[NOK] Could not upload the data to the master')
