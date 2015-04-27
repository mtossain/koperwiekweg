# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 14:48:53 2015

@author: Michel Tossaint
"""

Password = open('/home/pi/AuthBhostedFTP.txt','r').read().split('\n')[0]

import time
import ftplib
import vstarcam
   
IP = "192.168.2.28" #IP Camera ip or series NO
Port = 81 #IP Camera port
User = "admin" #IP Camera account
Pwd = "888888" #IP Camera password
UpdateRate = 120	 #Refresh rate pictures

vstarcam.Setting(IP,Port,User,Pwd,0,0) # Main stream resolution: 720px
vstarcam.Setting(IP,Port,User,Pwd,5,0) # Rotation: original

# Goto start point 30deg elevation
vstarcam.PTZ(IP,Port,User,Pwd,'Down')
time.sleep(8)
#vstarcam.PTZ(IP,Port,User,Pwd,'Up')
#time.sleep(0.5)
now = time.strftime("%Y-%m-%d %H:%M:%S")
print(now+' Goto start point 30deg Elevation [OK]')

# Goto start point North
vstarcam.PTZ(IP,Port,User,Pwd,'Right')
now = time.strftime("%Y-%m-%d %H:%M:%S")
print(now+' Goto start point 00deg Azimuth [OK]')
time.sleep(35)
AtLeft = True

NumberPics = 13
RotationTime = 2.5 #Seconds
while True:
    
    if AtLeft:
        #Completely turned to left
        vstarcam.Snapshot(IP,Port,User,Pwd,"KoperWiekCam_1.jpg")
        for x in range(2, NumberPics):
            vstarcam.PTZ(IP,Port,User,Pwd,'Left')
            time.sleep(RotationTime) #Pause
            vstarcam.PTZ(IP,Port,User,Pwd,'LeftStop')
            time.sleep(0.5) #Pause
            vstarcam.Snapshot(IP,Port,User,Pwd,"KoperWiekCam_"+str(x)+".jpg")
            time.sleep(0.5) #Pause
        AtLeft = False
    else:
        #Completely turned to right
        vstarcam.Snapshot(IP,Port,User,Pwd,"KoperWiekCam_"+str(NumberPics-1)+".jpg")
        for x in range(NumberPics-1, 0, -1):
            vstarcam.PTZ(IP,Port,User,Pwd,'Right')
            time.sleep(RotationTime) #Pause
            vstarcam.PTZ(IP,Port,User,Pwd,'RightStop')
            time.sleep(0.5) #Pause
            vstarcam.Snapshot(IP,Port,User,Pwd,"KoperWiekCam_"+str(x-1)+".jpg")
            time.sleep(0.5) #Pause
        AtLeft=True
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
        for x in range(0,NumberPics):
	    FileName = 'KoperWiekCam_'+str(x)+'.jpg'
            file = open(FileName,'rb') # file to send
	    session.storbinary('STOR '+FileName, file) # send the file
	    file.close() # close file and FTP
	    now = time.strftime("%Y-%m-%d %H:%M:%S")
	    print(now +' Uploaded panorama '+FileName+' to FTP [OK]')
        session.quit()
    except ftblib.all_errors:
	print(now +' Could not upload panorama '+FileName+' to FTP [NOK]')

    time.sleep(UpdateRate)
