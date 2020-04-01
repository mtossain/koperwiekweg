import shelve
import datetime
import os
import time
import json
import subprocess
import rpyc
from easyprocess import Proc

CRED   ='\033[91m'
CGREEN ='\033[92m'
CEND = '\033[0m'

ram_drive            = '/dev/shm/'
json_rain_sensor     = ram_drive+'rain.json'
shelve_rain          = ram_drive+'rain'
scale_factor         = 0.7
WeatherService = rpyc.connect("localhost", 18861)

def nowStr():
    return( datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))

ticks = 0
temperature=0

def getRainTicks():
    global ticks
    global temperature
    os.system('rm -Rf '+json_rain_sensor)
    time.sleep(0.5)
    cmd = "sudo rtl_433 -R 37 -F json:"+json_rain_sensor+' -E'
    try:
        stdout=Proc(cmd).call(timeout=120).stdout
        time.sleep(0.5)
        with open(json_rain_sensor) as f:
            data = json.loads(f.readline())
        if "temperature_C" in data:
            temperature = float(data["temperature_C"])
        if "rain" in data:
            ticks = int(data["rain"])
    except:
        print(CRED+'[NOK] rtl_433 timed out'+CEND)
        from easyprocess import EasyProcess
        s=EasyProcess("lsusb").call().stdout
        for line in s.splitlines():
            if line.find('Realtek')!=-1:
                cmd = "sudo usb_reset /dev/bus/usb/"+line[4:7]+"/"+line[15:18]
                stdout=Proc(cmd).call().stdout
                print(cmd + ' ' +stdout)
    return ticks, temperature


first_tick,temperature = getRainTicks() # get the first tick
print(CGREEN+'[OK] First tick: '+str(first_tick)+' [ticks]'+CEND)
last_hour = datetime.datetime.now().hour

# Main loop
while(1):
    ticks, temperature = getRainTicks()
    hour = datetime.datetime.now().hour
    if (hour==0) and (hour!=last_hour):
        first_tick = ticks
        print(CGREEN+'[OK] First tick: '+str(first_tick)+' [ticks]'+CEND)
    rain = (ticks-first_tick)*scale_factor
    try:
        WeatherService.root.update_sensor_rain(rain,0)
        print(CGREEN+'[OK] ' + nowStr() + ' T:'+str(temperature)+' [degC] R:'+str(ticks)+' [ticks] '+str(rain)+' [mm]'+CEND)
    except:
        print(CRED+'[NOK] Could not update weather service...'+CEND)
    time.sleep(1)
    last_hour = hour
