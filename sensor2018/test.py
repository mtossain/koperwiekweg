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


from read_winddir import *
try:
    wind_dir_angle, wind_dir_str = get_wind_dir_all()
    print('[OK] '+nowStr()+' WA: '+str(wind_dir_angle)+' WD: '+wind_dir_str)
except:
    print('[NOK] '+nowStr()+' Could not find the data from the Wind direction sensor')
