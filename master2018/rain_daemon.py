import shelve
import datetime
import os
import random
import time
import json
CRED = '\033[92m'
CEND = '\033[0m'

# DR        = Duur van de neerslag (in 0.1 uur) per uurvak
# RH        = Uursom van de neerslag (in 0.1 mm) (-1 voor <0.05 mm)

ram_drive            = '/ramtmp/'
json_rain_sensor     = ram_drive+'rain.json'
shelve_rain          = ram_drive+'rain.db'
scale_factor         = 0.7

def nowStr():
    return( datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))

def getRainTicks():
    os.system('rm -Rf '+json_rain_sensor)
    time.sleep(0.5)
    os.system("rtl_433 -R 37 -E -F json:"+json_rain_sensor)
    with open(json_rain_sensor) as json_data:
        data = json.load(json_data)
        if "temperature_C" in data:
            temperature = float(data["temperature_C"])
        if "rain" in data:
            ticks = int(data["rain"])
            print(CRED+'[OK] ' + nowStr() + ' T:'+str(temperature)+' [degC] R:'+str(ticks)+' [ticks]'+CEND)
    return ticks
    

first_tick = getRainTicks() # get the first tick
print(CRED+'[OK] First tick: '+str(first_tick)+' [ticks]'+CEND)
last_hour = datetime.datetime.now().hour

# Main loop
while(1):
    tick = getRainTicks()
    hour = datetime.datetime.now().hour
    if (hour==0) and (hour!=last_hour):
        first_tick = tick
        print(CRED+'[OK] First tick: '+str(first_tick)+' [ticks]'+CEND)
    rain = (tick-first_tick)*scale_factor
    d = shelve.open(shelve_rain) # Save the data to file
    d['rain']=rain
    print(CRED+'[OK] ' + nowStr() + ' Rain today:'+str(rain)+' [mm]'+CEND)
    d.close()
    last_hour = hour