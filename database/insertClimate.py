import time
import os
import mysql.connector
import csv
import numpy as np
#from datetime import datetime
import datetime
import netCDF4
# high level functions for working with NetCDF files
import xarray as xr

##############################################################################
# Update all variables for a certain time interval, taken from a KNMI file
##############################################################################
# Run variables:
PasswordMysql = open("/home/pi/AuthBhostedMysql.txt",'r').read().split('\n')[0]
##############################################################################


# Upload the row to the database
try:
    time.sleep(1)
    cnx = mysql.connector.connect(
         host="127.0.0.1", # your host, usually localhost
         port=3306,
         user="hjvveluw_mtossain", # your username
         passwd=PasswordMysql, # your password
         database="hjvveluw_wopr") # name of the data base
    print('[OK] Connected to database')
    time.sleep(1)

    # Delete the rows first in the database
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM `KnmiClimate`")
    cnx.commit()
    cursor.close()
    print('[OK] Deleted records from the database')
    time.sleep(1)

    print('*** Get the data from knmi')
    os.system('rm -Rf KIS*')
    os.system('wget https://data.knmi.nl/download/etmaalgegevensKNMIstations/1/noversion/1951/01/01/KIS___OPER_P___OBS_____L2.nc')
    dataset = xr.open_dataset('KIS___OPER_P___OBS_____L2.nc')
    ds_debilt = dataset.sel(station='270')

    time = np.array(dataset.variables['time'])
    DDVEC = np.array(ds_debilt.variables['DDVEC'])
    FHVEC = np.array(ds_debilt.variables['FHVEC'])
    TG = np.array(ds_debilt.variables['TG'])
    RH = np.array(ds_debilt.variables['RH'])
    UG = np.array(ds_debilt.variables['UG'])
    EV24 = np.array(ds_debilt.variables['EV24'])
    PG = np.array(ds_debilt.variables['PG'])


    print('*** Insert into the database')
    cursor = cnx.cursor()
    rownum=0
    for t in time: # Simulate there was a measurement every 3 minutes...
        print(str(rownum)+' Upload datetime: '+str(t)+ ' Temperature: '+str(TG[rownum]))
        # Upload the row to the database
        cursor.execute("INSERT INTO KnmiClimate (KnmiDateTime, DDVEC, FHVEC, TG, RH, UG, EV24, PG) " +
                       "VALUES ('" + str(t) + "','" + str(DDVEC[rownum])+ "','" + str(FHVEC[rownum])+ "','" +
                       str(TG[rownum]) + "','" + str(RH[rownum]) + "','" + str(UG[rownum]) + "','" + str(EV24[rownum]) +
                         "','" + str(PG[rownum]) + "')")
        cnx.commit()
        rownum += 1

    cursor.close()
    cnx.close()

except mysql.connector.Error as err:
    print("[NOK] Could not connect to database")
    print (err)
