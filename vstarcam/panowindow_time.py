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

NumberPics = 9
RotationTimeRight = 3.5 #Seconds
RotationTimeUp = 4 #Seconds
FirstRotationTime = 45 #Seconds

# Make the other pictures
while True:
    
    #Completely turned to left
    convertstr = ""

    # Go completely to the left and make the first pictures
    x=1
    FileName = 'KoperWiekCam_'+str(x)+'.jpg'
    FileNameUp = 'KoperWiekCam_'+str(x+NumberPics)+'.jpg'
    vstarcam.PTZ(IP,Port,User,Pwd,"Left")
    time.sleep(FirstRotationTime) #Pause
    vstarcam.PTZ(IP,Port,User,Pwd,"LeftStop")
    time.sleep(1) #Pause
    vstarcam.PTZ(IP,Port,User,Pwd,"Down")
    time.sleep(RotationTimeUp+1) #Pause
    vstarcam.PTZ(IP,Port,User,Pwd,"DownStop")
    time.sleep(1) #Pause
    vstarcam.Snapshot(IP,Port,User,Pwd,FileName)
    time.sleep(1) #Pause
    vstarcam.PTZ(IP,Port,User,Pwd,"Up")
    time.sleep(RotationTimeUp) 
    vstarcam.PTZ(IP,Port,User,Pwd,"UpStop")
    time.sleep(1) #Pause
    vstarcam.Snapshot(IP,Port,User,Pwd,FileNameUp)
    time.sleep(1) #Pause
    vstarcam.PTZ(IP,Port,User,Pwd,"Down")
    time.sleep(RotationTimeUp+1) #Pause
    os.system("convert "+FileNameUp+" "+FileName+" -append f"+str(x)+".jpg") # flip upside down
    os.system("convert f"+str(x)+".jpg -flip f"+str(x)+".jpg") # flip upside down
    convertstr += " f"+str(x)+".jpg" 

    for x in range(2,NumberPics+1):
        FileName = 'KoperWiekCam_'+str(x)+'.jpg'
        FileNameUp = 'KoperWiekCam_'+str(x+NumberPics)+'.jpg'
        vstarcam.PTZ(IP,Port,User,Pwd,"Right")
        time.sleep(RotationTimeRight) #Pause
        vstarcam.PTZ(IP,Port,User,Pwd,"RightStop")
        time.sleep(1) #Pause
        vstarcam.Snapshot(IP,Port,User,Pwd,FileName)
        time.sleep(1) #Pause
        vstarcam.PTZ(IP,Port,User,Pwd,"Up")
        time.sleep(RotationTimeUp) 
        vstarcam.PTZ(IP,Port,User,Pwd,"UpStop")
        time.sleep(1) #Pause
        vstarcam.Snapshot(IP,Port,User,Pwd,FileNameUp)
        time.sleep(1) #Pause
        vstarcam.PTZ(IP,Port,User,Pwd,"Down")
        time.sleep(RotationTimeUp+1) #Pause
        os.system("convert "+FileNameUp+" "+FileName+" -append f"+str(x)+".jpg") # flip upside down
        os.system("convert f"+str(x)+".jpg -flip f"+str(x)+".jpg") # flip upside down
        convertstr += " f"+str(x)+".jpg" 
		
    #Convert to panorama
    os.system("convert"+convertstr+" +append all.jpg") # append in one row
    os.system("convert all.jpg -matte -virtual-pixel white -distort arc '360 40' dome.jpg") # make polar plot
    os.system("convert dome.jpg -resize 1024x1024 dome.png") # resize and convert in png
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
