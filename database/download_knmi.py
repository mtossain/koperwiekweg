###############################################################################
# Get KNMI uurgegevens file from a station
#
# Input arguments:
#         start_date    YYYYMMDD
#         stop_date     YYYYMMDD
#
# From: Michel Tossaint 2018
###############################################################################

import argparse
import os
import csv
from dateutil.parser import parse
from datetime import datetime
CRED = '\033[91m'
CGREEN = '\033[92m'
CEND = '\033[0m'

# URL of the site where the data is taken
url = 'http://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/uurgegevens/'

# Parse the input date start and stop
parser = argparse.ArgumentParser()
parser.add_argument("start_date")
parser.add_argument("stop_date")
args = parser.parse_args()

startDatetime = datetime.strptime(args.start_date, '%Y%m%d')
stopDatetime = datetime.strptime(args.stop_date, '%Y%m%d')

# Define the filename
try:
    yearNeeded = int(args.start_date[0:4])
    if yearNeeded <= 2020:
        filename = 'uurgeg_348_2011-2020.zip'
    else:
        filename = 'uurgeg_348_2021-2030.zip'

    # Get the file and unzip
    os.system('rm -Rf uurgeg*')
    os.system('wget '+url+filename)
    os.system('unzip -o '+filename)

    print(CGREEN+'[OK] Downloaded the knmi file')
except:
    print(CRED+'[NOK] Could not get the knmi file from the web'+CEND)


# Open the file and get the lines needed
try:
    fOut = open('knmi.txt', 'w')
    print(CGREEN+'[OK] Selected the following lines:'+CEND)
    with open(filename[:-3]+'txt') as f:
        for line in f:
            if (line[0:5]=='  348'): # if it is a valid date line
                if (parse(line[6:14])>=startDatetime and parse(line[6:14])<=stopDatetime): # Found the last header lines
                    fOut.write(line)
                    print(line)
    fOut.close()
except:
    print(CRED+'[NOK] Could not parse the knmi file'+CEND)

print(CGREEN+'[OK] Finished parsing knmi file...'+CEND)
