# -------------------------------------------------------------------------------
#
#   rtl_433_wrapper.py
#
#   Wrapper script for executing "rtl_433" and processing the output as it occurs
#   in realtime.
#   As currently written it works with the "Aculink 5n1" weather station.
#
#   >>>---> Changes to handle other makes/models will likely be necessary, possibly
#            to the rtl_433 source as well because ouputting data
#           as JSON hasn't been implemented in  all of the protocol handlers :-/
#
#   The goal is to be able to use "rtl_433" unmodified so that is easy to stay
#   current as support for additional devices/protocols are added.
#   Note: To make this "real" some refactoring of the rtl_433 source will be
#   needed to add consistent support for JSON across the various protocol handlers.
#
# ------------------------------------------------------------------------------
import sys
from subprocess import PIPE, Popen, STDOUT
from threading  import Thread
import json
import datetime
import shelve
CRED = '\033[91m'
CGREEN = '\033[92m'
CEND = '\033[0m'

cmd = [ '/usr/local/bin/rtl_433', '-F', 'json', '-R', '40']
shelve_name = "/ramtmp/data_acurite.db"
shelve = shelve.open(shelve_name) # Save the data to file

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

stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)

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

# Create our sub-process...
# Note that we need to either ignore output from STDERR or merge it with STDOUT
# due to a limitation/bug somewhere under the covers of "subprocess"
# > this took awhile to figure out a reliable approach for handling it...
p = Popen( cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, close_fds=ON_POSIX)
q = Queue()
t = Thread(target=enqueue_output, args=('stdout', p.stdout, q))
t.daemon = True # thread dies with the program
t.start()

# ------------------------------------------------------------------------------
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
        if ( line.find( '"B"') != -1):
            #   Sample data for our two message formats...
            #   wind speed: 3 kph, wind direction: 180.0[degree], rain gauge: 0.00 in.
            #   wind speed: 4 kph, temp: 52.5[degree] F, humidity: 51% RH

            # Although data comes in as two rows I wanted to store it as a
            # single row in the DB. As a result we need to piece it together
            # to get a single record before we process it further...

            # At this point our data is a JSON string...
            # Convert our JSON string to a Python object,
            # then move the data into a dictionary as we get each row...
            data = json.loads( line)

            for item in data:
                record[ item] = data[ item]

            # we have processed two rows & now have a complete record...
            if ( ( 'humidity' in record) and ( 'rain_inch' in record)):
                #   sys.stdout.write( nowStr() + ' - record: ' + urllib.urlencode( record) + '\n')
                sys.stdout.write(CGREEN+nowStr() + ' - Wind Speed: ' + str(record[ 'wind_speed_kph']) + \
                ', Wind Dir: ' + str(record[ 'wind_dir_deg']) + ', Temp_C: ' + str(degf_to_degc(record['temperature_F'])) + \
                ', Humidity: ' + str(record[ 'humidity']) + ', Rain: ' + str(record[ 'rain_inch'])+CEND+ '\n')

                shelve['temperature']=degf_to_degc(float(record['temperature_F']))
                shelve['pressure']=1000
                shelve['rain']=float(record['rain_inch'])*25.6
                shelve['humidity']=float(record['humidity'])
                shelve['wind_speed']=float(record['wind_speed_kph'])
                shelve['wind_dir_angle']=float(record['wind_dir_deg'])
                shelve['wind_dir_str']=deg2compass(float(record['wind_dir_deg']))
                shelve['uv_index']=0
                shelve['light_intensity']=0

                record = {} # Empty the record for next time
        else:
            False
            sys.stdout.write( nowStr() + ' - stderr: ' + line)
            if (( line.find( 'Failed') != -1) or ( line.find( 'No supported devices') != -1)):
                sys.stdout.write( '   >>>---> ERROR, exiting...\n\n')
                exit( 1)

    sys.stdout.flush()
