
Password = open('/home/pi/AuthBhostedFTP.txt','r').read().split('\n')[0]

import time
import ftplib
import os
import requests

UpdateRate = 45 # In seconds

while True:
    
    # Make the snapshot
    os.system("ffmpeg -rtsp_transport tcp -y -i rtsp://admin:123456@192.168.178.254:554/mpeg4 -vcodec copy -t 3 snapshot.mp4")
    os.system("ffmpeg -ss 00:00:02 -t 1 -y -i snapshot.mp4 -f mjpeg snapshot.jpeg")
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    print(now + ' Snapshot taken [OK]')
	
    #Convert to proper size and apply circle mask
    os.system("convert -size 1280x960 xc:none -fill snapshot.jpeg -draw 'circle 640,480,1,480' domeflat.png")
    os.system("convert domeflat.png -flop -resize 1024x1024 domeflatter.png")
    os.system("convert -size 1024x1024 xc:none domeflatter.png -geometry +0+128 -composite dome.png")
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
        #file =open('snapshot.mp4','rb')
        #session.storbinary('STOR snapshot.mp4', file)
        #file.close()
        session.quit()
        print(now +' Uploaded panorama '+FileName+' to FTP [OK]')
    except ftplib.all_errors:
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        print(now +' Could not upload panorama '+FileName+' to FTP [NOK]')

    r = requests.get('http://www.koperwiekweg.nl/copy_dome.php')
		
    time.sleep(UpdateRate)
