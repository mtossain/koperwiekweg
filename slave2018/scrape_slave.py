###############################################################################
# Read all sensor data (except rain & lightning) and push to master
# 2018 - M.Tossaint
###############################################################################
import os
os.system('modprobe i2c_bcm2835 baudrate=400000')
import time
time.sleep(3) # Wait for baudrate to change
import shelve
import ftplib
import datetime
import rpyc

CRED = '\033[91m'
CGREEN = '\033[92m'
CEND = '\033[0m'

flag_upload_to_master = False
flag_camera           = False
flag_mcp9808          = False
flag_sht3x            = True
flag_ams811           = True
ftp_server            = open("/home/pi/MasterIP.txt",'r').read().split('\n')[0]
ftp_username          = 'pi'
ftp_password          = open("/home/pi/AuthMasterPi.txt",'r').read().split('\n')[0]
local_path            = '/ramtmp/'

def nowStr():
    return( datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))

try:
    WeatherService2 = rpyc.connect(ftp_server, 18861)
    print(CGREEN+'[OK] Connected to the WeatherServer')
except:
    print(CRED+'[NOK] Not connected to the WeatherServer')

# Read the sensor data
from read_bme280 import *
pressure=0
humidity=0
temperature=0
try:
    temperature,pressure,humidity = readBME280All()
    temperature = round(temperature,1)
    pressure = round(pressure,1)
    humidity = round(humidity,1)
    print(CGREEN+'[OK]  '+nowStr()+' BME280 T: '+str(temperature)+' [degC] P: '+str(pressure) + ' [mBar] H: '+str(humidity)+' [%]')
except:
    print(CRED+'[NOK] '+nowStr()+' Could not find the data from the BME280 pressure and humidity'+CEND)


if flag_sht3x:
    from read_sht3x import *
    try:
        humidity, temperature_sht3x = get_sht3x_data()
        temperature_sht3x = round(temperature_sht3x,1)
        humidity = round(humidity,1)
        print(CGREEN+'[OK]  '+nowStr()+' SHT3X H:'+str(humidity)+' [%] T: '+str(temperature_sht3x)+' [degC]')
    except:
        print(CRED+'[NOK] '+nowStr()+' Could not find the data from the SHT3X data')


if flag_mcp9808:
    from read_mcp9808 import *
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
    print(CGREEN+'[OK]  '+nowStr()+' SI1145 I: '+str(light_intensity)+' [-] IR: '+str(ir_value)+' [-] UV: '+str(uv_index)+' [-]')
    if uv_index>10:
        uv_index=0
except:
    print(CRED+'[NOK] '+nowStr()+' Could not find SI1145 light and uv_index'+CEND)


# Assume temperature is from BME280 or MCP9808
os.system('modprobe i2c_bcm2835 baudrate=10000')
time.sleep(3)
if flag_ams811:
    from read_ams811 import *
    try:
        co2,tvoc = get_ams811_data(temperature)
        print(CGREEN+'[OK]  '+nowStr()+' AMS811 eCO2: '+str(co2)+' [ppm] TVOC: '+str(tvoc)+' [ppm]')
    except:
        print(CRED+'[NOK] '+nowStr()+' Could not find AMS811 CO2 data'+CEND)


if flag_camera:
    try:
        os.system('raspistill -h 1054 -w 1054 -o '+local_path+'cam.jpg') # Take the camera image
        os.system('raspistill -h 1944 -w 1944 -o '+local_path+'cam_hd.jpg') # Take the camera image
        print('[OK]  '+nowStr()+' Got the camera image: '+local_path+'cam.jpg')
    except:
        print(CRED+'[NOK] '+nowStr()+' Could not take the camera image'+CEND)

try:
    WeatherService2.root.update_sensor_2018(temperature,pressure,humidity,uv_index,light_intensity,nowStr())
    print(CGREEN+'[OK] Uploaded data to weather server'+CEND)
except:
    print(CRED+'[NOK] Could not update weather service...'+CEND)

if flag_upload_to_master:
    try:
        if flag_camera:
            ftp_connection = ftplib.FTP(ftp_server, ftp_username, ftp_password)
            fh2 = open(local_path+"cam.jpg", 'rb')
            ftp_connection.storbinary('STOR /ramtmp/cam.jpg', fh2)
            fh2.close()
            fh = open(local_path+"cam_hd.jpg", 'rb')
            ftp_connection.storbinary('STOR /ramtmp/cam_hd.jpg', fh)
            fh.close()
        print('[OK]  '+nowStr()+' Uploaded data to the ftp master: '+ftp_server)
    except:
        print(CRED+'[NOK] '+nowStr()+' Could not upload the data to the master.'+CEND)
