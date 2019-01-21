import shelve
import datetime
import os
import time
import json
import subprocess
import rpyc

CRED   ='\033[91m'
CGREEN ='\033[92m'
CEND = '\033[0m'

ram_drive            = '/ramtmp/'
json_rain_sensor     = ram_drive+'rain.json'
shelve_rain          = ram_drive+'rain'
scale_factor         = 0.7
#d = shelve.open(shelve_rain) # Save the data to file
WeatherService = rpyc.connect("localhost", 18861)

def nowStr():
    return( datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))

def getRainTicks():
    ticks = 0
    temperature=0
    os.system('rm -Rf '+json_rain_sensor)
    time.sleep(0.5)
    #cmd = ['rtl_433','-R','37','-E','-F','json:'+json_rain_sensor]
    #cmd = "rtl_433 -R 37 -E -F json:"+json_rain_sensor
    #try:
    #    subprocess.call(cmd,timeout=60, shell=True)
    #except:
    #    print(CRED+'[NOK] rtl_433 timed out'+CEND)
    os.system("rtl_433 -R 37 -E -F json:"+json_rain_sensor)
    time.sleep(0.5)
    with open(json_rain_sensor) as f:
        data = json.loads(f.readline())
    if "temperature_C" in data:
        temperature = float(data["temperature_C"])
    if "rain" in data:
        ticks = int(data["rain"])
    print(CGREEN+'[OK] ' + nowStr() + ' T:'+str(temperature)+' [degC] R:'+str(ticks)+' [ticks]'+CEND)
    return ticks, temperature
    

first_tick,temperature = getRainTicks() # get the first tick
print(CGREEN+'[OK] First tick: '+str(first_tick)+' [ticks]'+CEND)
last_hour = datetime.datetime.now().hour

# Main loop
while(1):
    tick, temperature = getRainTicks()
    hour = datetime.datetime.now().hour
    if (hour==0) and (hour!=last_hour):
        first_tick = tick
        print(CGREEN+'[OK] First tick: '+str(first_tick)+' [ticks]'+CEND)
    rain = (tick-first_tick)*scale_factor
    try:
        WeatherService.root.update_sensor_rain(rain,0)
        print(CGREEN+'[OK] ' + nowStr() + ' Rain today:'+str(rain)+' [mm]'+CEND)
    except:
        print(CRED+'[NOK] Could not update weather service...'+CEND)
    time.sleep(1)
    last_hour = hour
