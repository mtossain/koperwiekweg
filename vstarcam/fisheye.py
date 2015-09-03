
Password = open('/home/pi/AuthBhostedFTP.txt','r').read().split('\n')[0]

import time
import ftplib
import os

UpdateRate = 60 # In seconds

while True:
    
	# Make the snapshot
    os.system("ffmpeg -y -i rtsp://admin:123456@192.168.178.254:554/mpeg4 -r 1 -vframes 1 -f image2 snapshot.jpeg")
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    print(now + ' Snapshot taken [OK]')
	
    #Convert to proper size and apply circle mask
    os.system("convert -size 1280x960 xc:none -fill snapshot.jpeg -draw "circle 640,480,1,480" domeflat.png")
    os.system("convert domeflat.png -resize 1024x1024 domeflatter.png")
    os.system("convert -size 1024x1024 xc:none domeflatter.png  -geometry  +0+128  -composite dome.png")
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    print(now + ' Generated panorama [OK]')

    #Upload to FTP server
    try:
        session = ftplib.FTP('server2.bhosted.nl','hjvveluw',Password)
        session.cwd('www/www.koperwiekweg.nl')
        FileName = 'dome.png'
        file = open(FileName,'rb') # file to send
        session.storbinary('STOR '+FileName, file) # send the file
        file.close() # close file and FTP
        session.quit()
    except ftplib.all_errors:
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        print(now +' Could not upload panorama '+FileName+' to FTP [NOK]')
		
    time.sleep(UpdateRate)
