import shelve
import datetime
import os
import time
import json
import subprocess
import rpyc
import sys
from subprocess import PIPE, Popen, STDOUT
from threading  import Thread

CRED   ='\033[91m'
CGREEN ='\033[92m'
CEND = '\033[0m'

ram_drive            = '/ramtmp/'
json_rain_sensor     = ram_drive+'rain.json'
scale_factor         = 0.7
WeatherService = rpyc.connect("localhost", 18861)


try: #   We're using a queue to capture output as it occurs
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x
ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(src, out, queue):
    for line in iter(out.readline, b''):
        queue.put(( src, line))
    out.close()

def nowStr():
    return( datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))

# Get the first tick to reference to
os.system('rm -Rf '+json_rain_sensor)
os.system("rtl_433 -R 37 -E -F json:"+json_rain_sensor)
time.sleep(0.5)
with open(json_rain_sensor) as f:
    data = json.loads(f.readline())
if "rain" in data:
    first_tick = int(data["rain"])
print(CGREEN+'[OK] First tick: '+str(first_tick)+' [ticks]'+CEND)
last_hour = datetime.datetime.now().hour

# Create our rtl_433 sub-process...
cmd = ['rtl_433','-R','37','-F','json']
p = Popen( cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, close_fds=ON_POSIX)
q = Queue()
t = Thread(target=enqueue_output, args=('stdout', p.stdout, q))
t.daemon = True # thread dies with the program
t.start()

record = {}
pulse = 0
while True:
    try:
        src, line = q.get(timeout = 1) # get the queue output
    except Empty:
        pulse += 1
    else: # got line
        pulse -= 1
        #   See if the data is something we need to act on...
        if ( line.find( 'rain') != -1):

            data = json.loads(line)
            for item in data:
                record[ item] = data[ item]
            if "temperature_C" in record:
                temperature = float(record["temperature_C"])
            if "rain" in record:
                tick = int(record["rain"])
            print(CGREEN+'[OK] ' + nowStr() + ' T:'+str(temperature)+' [degC] R:'+str(tick)+' [ticks]'+CEND)

            hour = datetime.datetime.now().hour
            if (hour==0) and (hour!=last_hour): # on rollover
                first_tick = tick
                print(CGREEN+'[OK] First tick: '+str(first_tick)+' [ticks]'+CEND)

            rain = (tick-first_tick)*scale_factor

            try: # Upload data to the master server
                WeatherService.root.update_sensor_rain(rain,0)
                print(CGREEN+'[OK] ' + nowStr() + ' Rain today:'+str(rain)+' [mm]'+CEND)
            except:
                print(CRED+'[NOK] Could not update weather service...'+CEND)
            time.sleep(1)
            last_hour = hour

            record = {} # Empty the record for next time
        else:
            False
            sys.stdout.write( nowStr() + ' - stderr: ' + line)
            if (( line.find( 'Failed') != -1) or ( line.find( 'No supported devices') != -1)):
                sys.stdout.write( '   >>>---> ERROR, exiting...\n\n')
                exit( 1)

    sys.stdout.flush()
