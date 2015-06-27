# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 14:48:53 2015

@author: Michel Tossaint
"""
Password = open('/home/pi/AuthBhostedFTP.txt','r').read().split('\n')[0]

import time
import ftplib
import vstarcam
import os
   
IP = "192.168.178.25" #IP Camera ip or series NO
Port = 81 #IP Camera port
User = "admin" #IP Camera account
Pwd = "888888" #IP Camera password
UpdateRate = 300 #Refresh rate pictures

#vstarcam.Setting(IP,Port,User,Pwd,0,1) # Main stream resolution: 720px
#vstarcam.Setting(IP,Port,User,Pwd,5,0) # Rotation: original

NumberPics = 8
RotationTime = 30 #Seconds
FirstRotationTime = 100 #Seconds
while True:
    
    #Completely turned to left
	convertstr = ""
    for x in range(1,NumberPics+1):
        FileName = 'KoperWiekCam_'+str(x)+'.jpg'
		FileNameUp = 'KoperWiekCam_'+str(x+NumberPics)+'.jpg'
		vstarcam.PTZ(IP,Port,User,Pwd,"CallPreset"+str(x))
        if x==1:
            time.sleep(FirstRotationTime) #Pause
        else:
            time.sleep(RotationTime) #Pause
        vstarcam.Snapshot(IP,Port,User,Pwd,FileName)
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        print(now +' Taking snapshot '+str(x)+' [OK]')
		vstarcam.PTZ(IP,Port,User,Pwd,'Up')
        time.sleep(3) #Pause 3s
		vstarcam.PTZ(IP,Port,User,Pwd,'UpStop')
		vstarcam.Snapshot(IP,Port,User,Pwd,FileNameUp)
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        print(now +' Taking snapshot '+str(x+NumberPics)+' [OK]')

        os.system("convert "+FileName+" "+FileNameUp+" -append f"+str(x)+".jpg") # flip upside down
        os.system("convert f"+str(x)+".jpg -flip f"+str(x)+".jpg") # flip upside down
		convertstr += " f"+str(x)+".jpg" 
		
    #Convert to panorama
    os.system("convert"+convertstr+" +append all.jpg") # append in one row
	os.system("convert all.jpg -matte -virtual-pixel white -distort arc '360 45' dome.jpg") # make polar plot
	os.system("convert dome.jpg -resize 1024x1024 dome.png") # resize and convert in png
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    print(now + ' Generated panorama [OK]')

    #Upload to FTP server
    try:
        session = ftplib.FTP('server2.bhosted.nl','hjvveluw',Password)
        session.cwd('www/www.koperwiekweg.nl')
        for x in range(1,NumberPics+1):
	        FileName = 'KoperWiekCam_'+str(x)+'.jpg'
            file = open(FileName,'rb') # file to send
	        session.storbinary('STOR '+FileName, file) # send the file
	        file.close() # close file and FTP
	        now = time.strftime("%Y-%m-%d %H:%M:%S")
	        print(now +' Uploaded panorama '+FileName+' to FTP [OK]')
        FileName = 'dome.png'
        file = open(FileName,'rb') # file to send
        session.storbinary('STOR '+FileName, file) # send the file
	    file.close() # close file and FTP
        session.quit()
    except ftplib.all_errors:
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        print(now +' Could not upload panorama '+FileName+' to FTP [NOK]')

    time.sleep(UpdateRate)
