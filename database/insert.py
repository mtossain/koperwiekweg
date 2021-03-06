import time
import mysql.connector
import csv
import numpy as np
import argparse
#from datetime import datetime
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("start_date")
parser.add_argument("stop_date")
args = parser.parse_args()

startDatetime = datetime.datetime.strptime(args.start_date, '%Y%m%d')
stopDatetime = datetime.datetime.strptime(args.stop_date, '%Y%m%d')+datetime.timedelta(days=1)

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
    print(args.stop_date)
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM AcuRiteSensor WHERE SensorDateTime BETWEEN "+\
        "CAST('"+args.start_date+"' AS DATE) AND CAST('"+stopDatetime.strftime('%Y%m%d')+"' AS DATE)")
    cnx.commit()
    cursor.close()
    print('[OK] Deleted records from the database')
    time.sleep(1)
    
    print('Get the date from the insert file')
    ifile  = open('knmi.txt', "rt")
    reader = csv.reader(ifile)
    rownum = 0
    for row in reader:
        colnum = 0
        for col in row:
            if colnum == 1:
                Date = col
            if colnum == 2:
                Hour = int(col)
            if colnum == 3:
                WindDirAngle = int(col)
            if colnum == 5:
                Wind = int(int(col)/10*3.6) # Convert from 0.1m/s to km/h
            if colnum == 7:
                Temp = float(col)/10
            if colnum == 11:
                UVIndex = float(col)/60 # Estimate from calibration with others
            if colnum == 13:
                Rain = int(int(col)/10)
            if colnum == 14:
                Baro = int(int(col)/10)
            if colnum == 17:
                Humid = int(col)
            colnum += 1
        
        # Find from angle the wind direction name
        WindDirStr = ["N","NEN","NE","NEE","E","SEE","SE","ESS","S","SWS","SW","SWW","W","NWW","NW","NWN","N"] # At 350 still has to go
        condition = np.abs(np.arange(0.0,361.0,22.5) - WindDirAngle)<11.25 # returns an array with true/false
        WindDirNP = np.extract(condition, WindDirStr) # use extract to get the winddir where true
        WindDir = str(WindDirNP[0])
 
        RainRate = 0
        SunPower = 0;
    
        for i in range(0, 59, 3): # Simulate there was a measurement every 3 minutes...
            # Small mistake at end of the day... if end of month... not often
            DateStr = Date[6:8]
            if Hour==24:
                DateStr = str(int(DateStr)+1).zfill(2)
                Hour=0
            DateTimeNow = Date[0:4] + "-" + Date[4:6] + "-" + DateStr + ' '+ str(Hour).zfill(2)  + ":" + str(i).zfill(2)+":00"
            print('Upload datetime: '+DateTimeNow)
            # Upload the row to the database
            cursor = cnx.cursor()
            cursor.execute("INSERT INTO AcuRiteSensor (SensorDateTime, Temperature, Pressure, Humidity, WindSpeed, WindDirection, WindDirectionAngle, Rainfall, RainfallRate, UVIndex, SunPower) " +
                           "VALUES ('" + DateTimeNow + "','" + str(Temp)+ "','" + str(Baro)+ "','" + str(Humid)+ "','" + str(Wind)+ "','" + WindDir+ "','" + str(WindDirAngle)+ "','" + str(Rain)+ "','" + str(RainRate)+ "','" + str(UVIndex)+ "','"  + str(SunPower) + "')")
            print(DateTimeNow + "','" + str(Temp)+ "','" + str(Baro)+ "','" + str(Humid)+ "','" + str(Wind)+ "','" + str(WindDir)+ "','" + str(WindDirAngle)+ "','" + str(Rain)+ "','" + str(RainRate)+ "','" + str(UVIndex)+ "','"  + str(SunPower))
            cnx.commit()
            cursor.close()
    
        print('Uploaded to SQL another row: '+str(rownum))   
        rownum += 1
    
    cnx.close()        

except mysql.connector.Error as err:
    print("Could not connect to database [NOK]")
    print (err)
