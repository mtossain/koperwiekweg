Password = open('/home/pi/AuthBhostedFTP.txt','r').read().split('\n')[0]
PasswordMysql = open("/home/pi/AuthBhostedMysql.txt",'r').read().split('\n')[0]

import socket
import time
import ftplib
import os
import requests
import mysql.connector

dirstick = "/media/DRAAKJE/"
UpdateRate = 45

while True:
    
    # Make the snapshot
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    snapshot = dirstick+"snapshot"+time.strftime("_%Y%m%d_%H%M%S")
    os.system("avconv -rtsp_transport tcp -y -i rtsp://admin:123456@192.168.178.254:554/mpeg4 -vcodec copy -t 1 movie.mp4")
    os.system("avconv -ss 00:00:00.5 -t 1 -y -i movie.mp4 -f mjpeg "+snapshot+".jpeg")
    os.system("rm -f movie.mp4")
    print(now + ' Snapshot taken [OK]')
	
    #Convert to proper size and apply circle mask
    os.system("convert -size 1280x960 xc:none -fill "+snapshot+".jpeg -draw 'circle 640,480,1,480' "+dirstick+"domeflat.png")
    os.system("convert "+dirstick+"domeflat.png -resize 1024x1024 "+dirstick+"domeflatter.png")
    os.system("convert -size 1024x1024 xc:none "+dirstick+"domeflatter.png -geometry +0+128 -composite "+dirstick+"dome.png")
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    print(now + ' Generated panorama [OK]')

    # Move snapshot to directory
    dailydir = dirstick+time.strftime("%Y%m%d")
    os.system("mkdir "+dailydir)
    os.system("mv "+snapshot+".jpeg "+dailydir)

    #Upload to FTP server
    try:
        time.sleep(2)
        session = ftplib.FTP('server2.bhosted.nl','hjvveluw',Password,timeout=30)
        session.cwd('www/www.koperwiekweg.nl')
        FileName = dirstick+"dome.png"
        file = open(FileName,'rb') # file to send
        session.storbinary('STOR dome.png', file) # send the file
        file.close() # close file and FTP
        session.quit()
        print(now +' Uploaded panorama '+FileName+' to FTP [OK]')
    except (socket.error, ftplib.all_errors) as e:
        print e
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        print(now + ' Could not upload panorama '+FileName+' to FTP [NOK]')

    # Copy on the server, to avoid partly images on site when FTP ongoing
    try:
        r = requests.get('http://www.koperwiekweg.nl/copy_dome.php',timeout=15)
    except (requests.ConnectionError, requests.Timeout, socket.timeout) as e:
        print e
        print(now +' Could not copy dome.jpg on server [NOK]')


    # Upload time to the database
    #try:
    #    cnx = mysql.connector.connect(
    #         host="127.0.0.1", # your host, usually localhost
    #         port=3307,
    #         user="mtossain", # your username
    #         passwd=PasswordMysql, # your password
    #         database="wopr") # name of the data base
    #    # Use all the SQL you like
    #    cursor = cnx.cursor()
    #    cursor.execute("INSERT INTO Camera (CameraDateTime) VALUES ('" + now + "')")
    #    cnx.commit()
    #    cursor.close()
    #    cnx.close()
    #    print('Data uploaded to database [OK]')
    #except mysql.connector.Error as err:
    #    print("Could not connect to database [NOK]")
    
    time.sleep(UpdateRate)
