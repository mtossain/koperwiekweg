import time
import sys
from subprocess import PIPE, Popen, STDOUT
from threading  import Thread
import json
import datetime
import rpyc
from easyprocess import Proc
import os
import urllib2
import numpy as np

CRED = '\033[91m'
CGREEN = '\033[92m'
CEND = '\033[0m'

ram_drive            = '/ramtmp/'
json_rain_sensor     = ram_drive+'rain.json'
WeatherService       = rpyc.connect("localhost", 18861)
scale_factor         = 0.7 # For rain ticks to mm

class Smooth:

    # Smooth class with outlier removal

    # Length: Length of the smoothing window
    # Threshold: number STD above which to take out outliers

    def __init__(self, length,threshold):
        self.num_added = 0
        self.length = length
        self.threshold = threshold
        self.data = np.array(np.zeros(length))

    def add(self,number):

       # Adds a number if it is not an outlier
       # Returns the mean of the window

        if self.num_added < self.length: # array still not full
            self.data = np.insert(self.data,0,number)
            self.data = np.delete(self.data,self.length)
            self.num_added += 1
            return (self.data[0:self.num_added].mean())
        else:
            if self.data.std()>0.1:
                self.data = np.insert(self.data,0,number)
                zscore = (self.data - self.data.mean())/self.data.std()
                absolute_normalized = np.abs(zscore)
                test_idx = absolute_normalized > self.threshold
                if test_idx[0] == True:
                    self.data = np.delete(self.data,0)
                else:
                    self.data = np.delete(self.data,self.length) # cannot be done at once
                self.num_added += 1
                return (self.data.mean())
            else: # all the same, std = 0 -> reset
                self.data = np.zeros(self.length)
                self.num_added = 0
                return number

def deg2compass(deg):
     arr = ['NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N']
     return arr[int(abs((deg - 11.25) % 360)/ 22.5)]
def nowStr():
    return( datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))
def hpa_to_inches(pressure_in_hpa):
    pressure_in_inches_of_m = pressure_in_hpa * 0.02953
    return pressure_in_inches_of_m
def mm_to_inches(rainfall_in_mm):
    rainfall_in_inches = rainfall_in_mm * 0.0393701
    return rainfall_in_inches
def degc_to_degf(temperature_in_c):
    temperature_in_f = (temperature_in_c * (9/5.0)) + 32
    return temperature_in_f
def degf_to_degc(temperature_in_f):
    temperature_in_c = (temperature_in_f-32)*5.0/9.0
    return temperature_in_c
def kmh_to_mph(speed_in_kmh):
    speed_in_mph = speed_in_kmh * 0.621371
    return speed_in_mph

#   We're using a queue to capture output as it occurs
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x
ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(src, out, queue):
    for line in iter(out.readline, b''):
        queue.put(( src, line))
    out.close()

###############################################################################
# Get the first rain ticks
def nowStr():
    return( datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))

ticks = 0
temperature=0

def getRainTicks():
    global ticks
    global temperature
    os.system('rm -Rf '+json_rain_sensor)
    time.sleep(0.5)
    cmd = "rtl_433 -R 37 -E -F json:"+json_rain_sensor
    try:
        print(CGREEN+'[OK] Getting first rain data...'+CEND)
        stdout=Proc(cmd).call(timeout=60).stdout
        time.sleep(0.5)
        with open(json_rain_sensor) as f:
            data = json.loads(f.readline())
        if "temperature_C" in data:
            temperature = float(data["temperature_C"])
        if "rain" in data:
            ticks = int(data["rain"])
        print(CGREEN+'[OK] ' + nowStr() + ' T:'+str(temperature)+' [degC] R:'+str(ticks)+' [ticks]'+CEND)
    except:
        print(CRED+'[NOK] rtl_433 timed out'+CEND)
    return ticks, temperature


first_tick,temperature = getRainTicks() # get the first tick
print(CGREEN+'[OK] First tick: '+str(first_tick)+' [ticks]'+CEND)
last_hour = datetime.datetime.now().hour

###############################################################################
cmd = ['rtl_433','-R','37','-R','40','-F','json']
p = Popen( cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, close_fds=ON_POSIX)
q = Queue()
t = Thread(target=enqueue_output, args=('stdout', p.stdout, q))
t.daemon = True # thread dies with the program
t.start()

record = {}
pulse = 0
temperature_s = Smooth(25,4)

while True:

    try:
        src, line = q.get(timeout = 1) # get the queue output
    except Empty:
        pulse += 1
    else: # got line
        pulse -= 1
        #   See if the data is something we need to act on...
        if (line.find( '"A"') != -1) or (line.find('Inovalley')!=-1):

            data = json.loads( line)

            for item in data:
                record[ item] = data[ item]

            # we have processed two rows & now have a complete record...
            if ( ( 'humidity' in record) and ( 'rain' in record) and ('wind_dir_deg' in record)):
                try:
                    f = urllib2.urlopen('http://api.wunderground.com/api/c76852885ada6b8a/conditions/q/pws:IIJSSELS27.json')
                    parsed_json = json.loads(f.read())
                    pressure = int(float(parsed_json['current_observation']['pressure_mb']))
                except:
                    pressure = 0

                humidity=round(float(record['humidity']),1)
                wind_speed=round(float(record['wind_speed_kph']),1)
                wind_dir_angle=round(float(record['wind_dir_deg']),1)
                print(round(degf_to_degc(record['temperature_F']),1))
                temperature = round(temperature_s.add(degf_to_degc(record['temperature_F'])),1)
                print(temperature_s.data)
                wind_dir_str = deg2compass(wind_dir_angle)

                hour = datetime.datetime.now().hour
                ticks=int(record['rain'])
                if (hour==0) and (hour!=last_hour):
                    first_tick = ticks
                    print(CGREEN+'[OK] First tick: '+str(first_tick)+' [ticks]'+CEND)
                rain = (ticks-first_tick)*scale_factor

                sys.stdout.write(CGREEN+nowStr() + ' - W_vel: ' + str(wind_speed) + \
                ', W_dir: ' + str(wind_dir_angle) + ', T: ' + str(temperature) + \
                ', P: '+str(pressure)+', H: ' + str(humidity) + ', R: ' + str(rain)+CEND+ '\n')

                try: # Upload data to the master server
                    WeatherService.root.update_sensor_rain(rain,0)
                    WeatherService.root.update_sensor_2018(temperature,pressure,humidity,0,0)
                    WeatherService.root.update_sensor_wind(wind_speed,wind_dir_str,wind_dir_angle)
                except:
                    print(CRED+'[NOK] Could not update weather service...'+CEND)
                time.sleep(1)
                last_hour = hour

                record = {} # Empty the record for next time
        else:
            False
            #sys.stdout.write( nowStr() + ' - stderr: ' + line)
            if (( line.find( 'Failed') != -1) or ( line.find( 'No supported devices') != -1)):
                sys.stdout.write( '   >>>---> ERROR, exiting...\n\n')
                exit( 1)

    sys.stdout.flush()
