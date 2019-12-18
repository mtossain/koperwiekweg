import mysql.connector
from datetime import datetime
import httplib, urllib
import datetime

deltaTimeSeconds = 5*60

def nowStr():
    return( datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))

# Get the last record from pushover
cnx = mysql.connector.connect(
host='127.0.0.1',
port=3306,
user='hjvveluw_mtossain',
passwd='vR6Fakwg7JmVWQ',
database='hjvveluw_wopr')
cursor = cnx.cursor()
cursor.execute("SELECT * FROM AcuRiteSensor ORDER BY SensorDateTime DESC")
myrecord = cursor.fetchone()
print(myrecord)

# Time difference
print("Now: "+nowStr())
print("Last record: "+str(myrecord[1]))
duration = datetime.datetime.now()-myrecord[1]
print("Time since last record: "+str(duration))
message_po = "Last update: "+str(myrecord[1])

# Update Pushover
if duration.total_seconds()>deltaTimeSeconds:

    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.urlencode({
      "token": "ajvhd2b75zyuoy6ijpaxabriggxbf9",
      "user": "ujkruc8ojd9av86fgv2hkbd4pbv7xp",
      "title": "KWW Update ERROR...",
      "message": message_po,
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
