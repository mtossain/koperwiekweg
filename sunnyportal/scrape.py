import os
import time
import requests
import serial
import mysql.connector
import subprocess
import shelve
from datetime import datetime
import math
import json
import urllib2
from dateutil.parser import *
import datetime as dt

PasswordAculink = open("/home/pi/AuthAculinkWebsite.txt",'r').read().split('\n')[0]
PasswordMysql = open("/home/pi/AuthBhostedMysql.txt",'r').read().split('\n')[0]

shelve = shelve.open("config.db")

Temp=shelve['Temp']
Baro=shelve['Baro']
Humid=shelve['Humid']
Rain=shelve['Rain']
RainRate=0
Wind=shelve['Wind']
WindDir=shelve['WindDir']
WindDirAngle=shelve['WindDirAngle']
UVIndex=shelve['UVIndex']
TransmitPower=0
SunPower=shelve['SunPower']
LightningDist=999999

HumidReadings = [] # For moving average
max_samples = 4
def mean(nums):
    return float(sum(nums)) / max(len(nums), 1)

#Get the sun power data value
#command = ["scrapy", "crawl", "sunnyportal"]    
#with open(os.devnull, "w") as fnull:
    #result = subprocess.call(command, stderr = fnull, stdout = fnull)
#time.sleep(10)
#with open ("FixedPages", "r") as myfile:
    #data = myfile.read()
#print(data)
#time.sleep(1000)
#test = data.find('<span id="CurrentPlantPowerValue">')
#if test > 0:
#    text2 = data[test:]
#    test2 = text2.find('</span>')
#    if test2 > 0:
#        SunPower = int(float(text2[34:test2])/12)
#        print('Found solar power from SunnyPortal.com [OK]')
#        shelve['SunPower'] = SunPower
#    else:
#        print('Could not get the Sunnyportal webpage [NOK]')
#        SunPower=shelve['SunPower']
#else:
#    print('Could not get the Sunnyportal webpage [NOK]')        
#    SunPower=shelve['SunPower']

# now get the data from Aculink

try:
    #r = requests.get('https://acu-link.com/login', auth=('h.j.van.veluw@gmail.com', PasswordAculink),timeout=6)

    #FindTemp = r.text.find("<div class=\"sensor-widget-label\">Temperature</div>")
    #if FindTemp>0:
        #test = r.text[FindTemp:]
        #test2 = test[test.find('<div class=\"reading\">'):]
        #Temp = float(test2[21:24])
        #dummy =test.find("<div class=\"sensor-decimal\">")
        #if dummy > 0:
            #test2 = test[dummy:]
            #Temp = Temp + float(test2[30:45])
            #print('Found temperature from Aculink.com [OK]')
            #shelve['Temp']=Temp
        #else:
            #Temp=shelve['Temp']


    #FindBaro = r.text.find("<div class=\"sensor-widget-label\">Barometric Pressure</div>")
    #if FindBaro>0:
        #test = r.text[FindBaro:]
        #test2 = test[test.find('<div class=\"reading\">'):]
        #Baro = int(test2[21:25])
        #print('Found pressure fromform Aculink.com [OK]')
        #shelve['Baro']=Baro
    #else:
        #Baro=shelve['Baro']
        
    #FindHumid = r.text.find("<div class=\"sensor-widget-label\">Humidity</div>")
    #if FindHumid>0:
        #test = r.text[FindHumid:]
        #test2 = test[test.find('<div class=\"reading\">'):]
        #Humid = int(test2[21:24])
        #print('Found humidity from Aculink.com [OK]')
        #shelve['Humid']=Humid
    #else:
        #Humid=shelve['Humid']

    #FindRain = r.text.find("<div class=\"sensor-widget-label\">Rainfall</div>")
    #if FindRain>0:
        #test = r.text[FindRain:]
        #test2 = test[test.find('<div class=\"reading\">'):]
        #Rain = float(test2[21:25])
        #print('Found rainfall from Aculink.com [OK]')
        #shelve['Rain']=Rain
    #else:
        #Rain=shelve['Rain']

    #FindWind = r.text.find("<div class=\"wind-speed-label\">Wind Speed</div>")
    #if FindWind>0:
        #test = r.text[FindWind:]
        #test2 = test[test.find('<div class=\"wind-speed-reading\">'):]
        #test3 = test2.find("</div>")
        #Wind = float(test2[32:test3])
        #print('Found windspeed from Aculink.com [OK]')
        #shelve['Wind']=Wind
    #else:
        #Wind=shelve['Wind']

    #FindWindDir = r.text.find("100x_winddirect_")
    #if FindWindDir>0:
        #test = r.text[FindWindDir+5:]
        #FindWindDir = test.find("100x_winddirect_")
        #if FindWindDir>0:
            #test = test[FindWindDir:]
            #test4 = test.find('.png')
            #WindDir = test[16:test4]
            #if WindDir == 'N':
                #WindDirAngle = 0
            #if WindDir== "NEN" or WindDir=="ENN" or WindDir=="NNE":
                #WindDirAngle = 22.5
            #if WindDir== "NE":
                #WindDirAngle = 45
            #if WindDir== "NEE" or WindDir=="ENE" or WindDir=="EEN":
                #WindDirAngle = 67.5
            #if WindDir== "E":
                #WindDirAngle = 90
            #if WindDir== "SEE" or WindDir=="ESE" or WindDir=="EES":
                #WindDirAngle = 112.5
            #if WindDir== "SE":
                #WindDirAngle = 135
            #if WindDir== "ESS" or WindDir=="SES" or WindDir=="SSE":
                #WindDirAngle = 157.5
            #if WindDir== "S":
                #WindDirAngle = 180
            #if WindDir== "SWS" or WindDir=="WSS" or WindDir=="SSW":
                #WindDirAngle = 202.5
            #if WindDir== "SW":
                #WindDirAngle = 225
            #if WindDir== "SWW" or WindDir=="WSW" or WindDir=="WWS":
                #WindDirAngle = 247.5
            #if WindDir== "W":
                #WindDirAngle = 270
            #if WindDir== "NWW" or WindDir=="WNW" or WindDir=="WWN":
                #WindDirAngle = 292.5
            #if WindDir== "NW":
                #WindDirAngle = 315
            #if WindDir== "NWN" or WindDir=="WNN" or WindDir=="NNW":
                #WindDirAngle = 337.5
            #print('Found winddirection from Aculink.com [OK]')
            #shelve['WindDirAngle']=WindDirAngle
    #else:
        #WindDirAngle=shelve['WindDirAngle']

    f = urllib2.urlopen('http://api.wunderground.com/api/c76852885ada6b8a/conditions/q/pws:IIJSSELS30.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)
    station_time = parse(parsed_json['current_observation']['observation_time_rfc822']).replace(tzinfo=None)
    now = dt.datetime.now()
    seconds = (now-station_time).total_seconds()
    if seconds > 5*60:
        print('Station IIJSELS30 is not updated since: '+str(int(seconds/60))+'min, taking Ijsselstein [NOK]')
        f = urllib2.urlopen('http://api.wunderground.com/api/c76852885ada6b8a/conditions/q/Ijsselstein.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
    #print(json.dumps(parsed_json, sort_keys=True,indent=4, separators=(',', ': ')))
    Baro = int(float(parsed_json['current_observation']['pressure_mb']))
    Temp = float(parsed_json['current_observation']['temp_c'])
    
    Wind = int(float(parsed_json['current_observation']['wind_kph']))
    WindDir = parsed_json['current_observation']['wind_dir']
    WindDirAngle = int(float(parsed_json['current_observation']['wind_degrees']))
    
    try:
        Rain = int(float(parsed_json['current_observation']['precip_today_metric']))
    except:
        Rain = shelve['Rain']

    humidity_str = parsed_json['current_observation']['relative_humidity']
    Humid = int(float(humidity_str[:-1]))
    HumidReadings.append(Humid)
    Humid = mean(HumidReadings)
    if len(HumidReadings) == max_samples:
        HumidReadings.pop(0)

    if Temp<-50 or Temp>50:
        Temp = shelve['Temp']
    if Baro<750 or Baro>1250:
        Baro = shelve['Baro']
    if Wind<0 or Wind>1000:
        Wind = shelve['Wind']
    if Humid<0 or Humid>100:
        Humid = shelve['Humid']
    if Rain<0 or Rain>100:
        Rain = shelve['Rain']

    shelve['Temp']=Temp
    shelve['Baro']=Baro
    shelve['Humid']=Humid
    shelve['Rain']=Rain
    shelve['Wind']=Wind
    shelve['WindDir']=WindDir
    shelve['WindDirAngle']=WindDirAngle
    print('Found data from wunderground.com [OK]')
    
except requests.exceptions.RequestException as e:
    print('Could not get the Aculink webpage [NOK]')
    Temp=shelve['Temp']
    Baro=shelve['Baro']
    Humid=shelve['Humid']
    Rain=shelve['Rain']
    Wind=shelve['Wind']
    WindDir=shelve['WindDir']
    WindDirAngle=shelve['WindDirAngle']

# Get the UV Index Sensor data     
try:
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    test=str(ser.readline())
    test+=str(ser.readline())
    test+=str(ser.readline())
    start= test.find('<uvIntensity>')
    stop= test.find('</uvIntensity>')
    if start>0 and stop>0 and stop>start:
        try:
            UVIndex = float(test[start+13:stop])
            UVIndex = float(int(UVIndex*10))/10*2
            print('Found UV data from sensor [OK]')
            shelve['UVIndex']=UVIndex
        except ValueError:
            print(test[start:])
            print('Error: did not convert to float... [NOK]')
except serial.SerialException, e:
    print("Could not find data from UV Sensor [NOK]")
    UVIndex=shelve['UVIndex']


# Get the lightning sensor data
try:
    fname = '/var/log/lightning.log' 
    with open(fname, 'rb') as fh:
    	for line in fh:
            pass
        print('Found Lightning Sensor data [OK]')
        now = datetime.now()
        LightningDate = datetime.strptime(line[:19], '%Y-%m-%d %H:%M:%S') # date object
        minutes  = (now - LightningDate).total_seconds() / 60
        if minutes < 30:
            LightningDist = float(line[-2:])
            if LightningDist ==1 or LightningDist==5:
                LightningDist = 99.0
        else:
            LightningDist = 99.0
except IOError: #handle other exceptions such as attribute errors
    print("Could not find Lightning Sensor data [NOK]")

now = time.strftime("%Y-%m-%d %H:%M:%S")
print(now + ' T:'+str(Temp)+ ' P:'+str(Baro)+' H:'+str(Humid)+' R:'+str(Rain)+' W:'+str(Wind)+' WD:'+WindDir+' WDA:'+str(WindDirAngle)+' UVI:'+str(UVIndex)+' LD:'+str(LightningDist))     

# Get the RF Sensor data     
#os.system('rtl_power -f 87.5M:108M:10k -1 rflog.csv')
#ifile  = open('rflog.csv', "rb")
#reader = csv.reader(ifile)
#rownum = 0
#Freq=[]
#Power=[]
#for row in reader:
	#colnum = 0
	#for col in row:
		#if colnum == 2:
			#StartFreq = float(col)
		#if colnum == 3:
			#StopFreq = float(col)
		#if colnum == 4:
			#StepFreq = float(col)
		#if colnum > 5:
		    #if col<>'nan':
			    #Freq.append(StartFreq + StepFreq*(colnum-6))
			    #Power.append(float(col))
		#colnum += 1       
	#rownum += 1
#ifile.close()
#PowerMax = max(Power)
#PowerMin = min(Power)
#FreqMax = Freq[Power.index(PowerMax)]
#FreqMin = Freq[Power.index(PowerMin)]
#TransmitPower = PowerMax - PowerMin
#print("Max Power: "+str(PowerMax) + " Min Power: " + str(PowerMin))
#print("Max Freq: "+str(FreqMax/1e6) + "[MHz] Min Freq: " + str(FreqMin/1e6)+"[MHz]")
#print('Found RF Power from sensor [OK]')
# Upload it to the database

try:
    cnx = mysql.connector.connect(
         host="127.0.0.1", # your host, usually localhost
         port=3307,
         user="mtossain", # your username
         passwd=PasswordMysql, # your password
         database="wopr") # name of the data base

    # Use all the SQL you like
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO AcuRiteSensor (SensorDateTime, Temperature, Pressure, Humidity, WindSpeed, WindDirection, WindDirectionAngle, Rainfall, RainfallRate, UVIndex,TransmitPowerkW, SunPower, LightningDist) " +
                                   "VALUES ('" + now + "','" + str(Temp)+ "','" + str(Baro)+ "','" + str(Humid)+ "','" + str(Wind)+ "','" + WindDir+ "','" + str(WindDirAngle)+ "','" + str(Rain)+ "','" + str(RainRate)+ "','" + str(UVIndex)+ "','" + str(TransmitPower)+ "','" + str(SunPower) + "','" + str(LightningDist) + "')")
    cnx.commit()
    cursor.close()
    cnx.close()

    print('Data uploaded to database [OK]')
    
except mysql.connector.Error as err:
    print("Could not connect to database [NOK]")
    print(err)

shelve.close()
 
