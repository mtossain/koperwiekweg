import socket
import time
import ftplib
import os
import requests
import subprocess as sub

dirstick = "/ramtmp/" # where to put the snapshot pictures for archive
UpdateRate = 90 # in s how often to make the snapshots
Password = open('/home/pi/AuthBhostedFTP.txt','r').read().split('\n')[0] # password bhosted not stored in this script

while True:

        print('*** 1 - Convert the snapshot ***\n\n')
        os.system("convert -size 1280x960 xc:none -fill cam.jpg -draw 'circle 640,480,1,480' "+dirstick+"back1.png")
        os.system("convert "+dirstick+"back1.png -resize 1024x1024 "+dirstick+"back2.png")
        os.system("convert -size 1024x1024 xc:none "+dirstick+"back2.png -geometry +0+128 -composite "+dirstick+"back3.png")
        os.system("convert -size 1024x1024 xc:none "+dirstick+"back3.png -rotate '-90' -composite "+dirstick+"dome.png")
        now = time.strftime("%Y-%m-%d %H:%M:%S")

    print('*** 2 - Move fisheye to FTP server')
    try:
        time.sleep(2)
        FileName = dirstick+"dome.png"
        file = open(FileName,'rb') # file to send
        session = ftplib.FTP('s14.servitnow.nl','hjvveluw',Password,timeout=30)
        session.cwd('/domains/koperwiekweg.nl/public_html')
        session.storbinary('STOR dome.png', file) # send the file
        file.close() # close file and FTP
        session.quit()
        print(now +' Uploaded fisheye '+FileName+' to FTP [OK]')
    except (socket.error, ftplib.all_errors) as e:
        print (e)
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        print(now + ' Could not upload fisheye '+FileName+' to FTP [NOK]')

    print('*** 3 - Copy image on server to avoid partly images on website when FTP ongoing')
    try:
        r = requests.get('http://www.koperwiekweg.nl/copy_dome.php',timeout=15)
    except (requests.ConnectionError, requests.Timeout, socket.timeout) as e:
        print (e)
        print(now +' Could not copy dome.png on server [NOK]')

    os.system("rm -Rf "+dirstick+"*.jpeg")
    os.system("rm -Rf "+dirstick+"*.png")

    time.sleep(UpdateRate)
