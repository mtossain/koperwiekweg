import time
import mysql.connector
import csv
import numpy as np
##############################################################################
# Update one variable only for a certain time interval, taken from a KNMI file
# 0: Wind speed
# 1: Wind direction
# 2: Pressure
# 3: Humidity
# 4: UV Index
# 5: Rain
##############################################################################
# Run variables:
variable = 2
PasswordMysql = open("/home/pi/AuthBhostedMysql.txt",'r').read().split('\n')[0]
##############################################################################

# Upload the row to the database
try:
    time.sleep(5)
    print('Connect to wopr database')
    cnx = mysql.connector.connect(
         host="127.0.0.1", # your host, usually localhost
         port=3306,
         user="hjvveluw_mtossain", # your username
         passwd=PasswordMysql, # your password
         database="hjvveluw_wopr") # name of the data base
    cursor = cnx.cursor()

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
            if colnum == 4:
                Wind = int(int(col)/10*3.6) # Convert from 0.1m/s to km/h
            if colnum == 7:
                Temp = float(col)/10
            if colnum == 11:
                UVIndex = float(col)/60 # Estimate from calibration with others
            if colnum == 13:
                Rain = int(int(col)/10)
                if Rain == -0.1:
                    Rain = 0
            if colnum == 14:
                Baro = int(int(col)/10)
            if colnum == 17:
                Humid = int(col)
            colnum += 1       
    
        # Find from angle the wind direction name
        WindDirStr = ["N","NEN","NE","NEE","E","SEE","SE","ESS","S","SWS","SW","SWW","W","NWW","NW","NWN","N"] # At 350 still has to go
        condition = np.abs(np.arange(0.0,361.0,22.5) - WindDirAngle)<11.25
        WindDir = np.extract(condition, WindDirStr)
 
        RainRate = 0 # TBD
        SunPower = 0 # TBD
        
        # Correct for KNMI flaw of hour 24
        Min=00
        if (Hour==24):
			Hour=23
			Min =59
        DateTimeNow = Date[0:4] + "-" + Date[4:6] + "-" + Date[6:8] + ' '+ str(Hour).zfill(2)  + ":"+str(Min).zfill(2)+":00"
        print('Upload datetime: '+DateTimeNow)
                                   
        # Update the row to the database
        if variable == 0:
			fieldname = 'WindSpeed'
			valuesens = Wind
        if variable == 1:
			fieldname = 'WindDirection'
			valuesens = WindDirAngle
        if variable == 2:
			fieldname = 'Pressure'
			valuesens = Baro
        if variable == 3:
			fieldname = 'Humidity'
			valuesens = Humid
        if variable == 4:
			fieldname = 'UVIndex'
			valuesens = UVIndex
        if variable == 5:
			fieldname = 'Rainfall'
			valuesens = Rain
        sql_statement = "UPDATE AcuRiteSensor SET "+fieldname+"="+str(valuesens)+" WHERE SensorDateTime BETWEEN DATE_SUB('"+DateTimeNow+"', INTERVAL 1 HOUR) AND '"+DateTimeNow+"'"
        cursor.execute(sql_statement)
        print('Updated '+fieldname+' to: '+str(valuesens)+' on: '+str(cursor.rowcount)+' rows.' )   
        cnx.commit()
    
    cnx.close()        

except mysql.connector.Error as err:
    print("Could not connect to database [NOK]")
    print (err)
