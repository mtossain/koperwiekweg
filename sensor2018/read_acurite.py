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

cmd = [ '/usr/local/bin/rtl_433', '-F', 'json', '-R', '10', '-R', '40']
shelve_name = "data_acurite.db"

def nowStr():
    return( datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))

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
        if ( line.find( 'wind') != -1):
            #   Sample data for our two message formats...
            #   wind speed: 3 kph, wind direction: 180.0[degree], rain gauge: 0.00 in.
            #   wind speed: 4 kph, temp: 52.5[degree] F, humidity: 51% RH

            #   Remove the [degree] character as well as Unit Of Measure indicators...
            line = stripped( line)
            line = line.replace( ' F', '')
            line = line.replace( '% RH', '')
            line = line.replace( ' kph', '')
            line = line.replace( ' in.', '')

            #   Add a timestamp & tweak the formatting a bit so we have valid JSON...
            line = 'timestamp: ' + nowStr() + ', ' + line
            line = '{"' + line + '"}'
            line = line.replace( ', ', '","')
            line = line.replace( ': ', '":"')

            # Although data comes in as two rows I wanted to store it as a
            # single row in the DB. As a result we need to piece it together
            # to get a single record before we process it further...

            # At this point our data is a JSON string...
            # Convert our JSON string to a Python object,
            # then move the data into a dictionary as we get each row...
            data = json.loads( line)

            for item in data:
                record[ item] = data[ item]

            # When we have "rain gauge" and "temp" in our dictionary we know
            # we have processed two rows & now have a complete record...
            if (( 'rain gauge' in record) and ( 'temp' in record)):
                #   sys.stdout.write( nowStr() + ' - record: ' + urllib.urlencode( record) + '\n')
                sys.stdout.write( nowStr() + ' - Wind Speed: ' + record[ 'wind speed'] + \
                ', Wind Dir: "' + record[ 'wind direction'] + '", Temp: ' + record[ 'temp'] + \
                ', Humidity: ' + record[ 'humidity'] + ', Rain: ' + record[ 'rain gauge']+ '\n')

                shelve = shelve.open(shelve_name) # Save the data to file
                shelve['temperature']=record[ 'temp']
                shelve['rain']record[ 'rain gauge']
                shelve['humidity']=record[ 'humidity']
                shelve['wind_speed']=record['wind speed']
                shelve['wind_dir_str']=record['wind direction']
                shelve.close()

                record = {} # Empty the record for next time
        else:
            False
            sys.stdout.write( nowStr() + ' - stderr: ' + line)
            if (( line.find( 'Failed') != -1) or ( line.find( 'No supported devices') != -1)):
                sys.stdout.write( '   >>>---> ERROR, exiting...\n\n')
                exit( 1)

    sys.stdout.flush()
