# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 14:48:53 2015

@author: Michel Tossaint
"""
file = open('~/AuthBhostedFTP.txt', 'r')
Password = file.readline():
file.close()

import time
import ftplib
import vstarcam
   
IP = "192.168.2.28" #IP Camera ip or series NO
Port = 81 #IP Camera port
User = "admin" #IP Camera account
Pwd = "888888" #IP Camera password
UpdateRate = 300 #Refresh rate pictures

#vstarcam.Setting(IP,Port,User,Pwd,0,1) # Main stream resolution: 720px
#vstarcam.Setting(IP,Port,User,Pwd,5,0) # Rotation: original

NumberPics = 5
RotationTime = 15 #Seconds
while True:
    
    #Completely turned to left
    for x in range(1,NumberPics):
        vstarcam.PTZ(IP,Port,User,Pwd,"CallPreset"+str(x))
        time.sleep(RotationTime) #Pause
        vstarcam.Snapshot(IP,Port,User,Pwd,"KoperWiekCam_"+str(x)+".jpg")
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        print(now +' Taking snapshot '+str(x)+' [OK]')
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    print(now +' Taking snapshots [OK]')

    #Convert to panorama
    #result = subprocess.call("generatepanorama.bat")
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    print(now + ' Generated panorama [OK]')

    #Upload to FTP server
    try:
        session = ftplib.FTP('server2.bhosted.nl','hjvveluw',Password)
        session.cwd('www/www.koperwiekweg.nl')
        for x in range(1,NumberPics):
	        FileName = 'KoperWiekCam_'+str(x)+'.jpg'
            file = open(FileName,'rb') # file to send
	        session.storbinary('STOR '+FileName, file) # send the file
	        file.close() # close file and FTP
	        now = time.strftime("%Y-%m-%d %H:%M:%S")
	        print(now +' Uploaded panorama '+FileName+' to FTP [OK]')
        session.quit()
    except ftplib.all_errors:
        now = time.strftime("%Y-%m-%d %H:%M:%S")
	    print(now +' Could not upload panorama '+FileName+' to FTP [NOK]')

    time.sleep(UpdateRate)

