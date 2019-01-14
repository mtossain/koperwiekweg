import socket
import time
import ftplib
import os
import requests
import subprocess as sub
import threading
from requests.auth import HTTPBasicAuth

class RunCmd(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout

    def run(self):
        self.p = sub.Popen(self.cmd)
        self.p.wait()

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.terminate()      #use self.p.kill() if process needs a kill -9
            self.join()

avail = 0 # which camera(s) is/are available 
# 0  -both Fisheye
# 1  -Fisheye1 only
# 2  -Fisheye2 only
RtspFisheye1 = 'rtsp://admin:admin@192.168.178.168:554/0/'
RtspFisheye2 = 'rtsp://admin:123456@192.168.178.254:554/mpeg4'
dirstick = "/ramtmp2/" # where to put the snapshot pictures for archive
#dirstick = "/home/pi/" # where to put the snapshot pictures for archive
UpdateRate = 90 # in s how often to make the snapshots
Password = open('/home/pi/AuthBhostedFTP.txt','r').read().split('\n')[0] # password bhosted not stored in this script

while True:
    
    if (avail==0 or avail==1):
        
        print('*** 0 - Set the camera in the right mode ***\n\n')
        try:
            r = requests.get('http://192.168.178.168/vb.htm?title=IP-Camera&videocodec=0&localdisplay=1&mirctrl=0&videocodeccombo=4&setvideoencbitratelevel=5&iframeinterval=30&codelevel=0', auth=HTTPBasicAuth('admin', 'admin'),timeout=15)
        except (requests.ConnectionError, requests.Timeout, socket.timeout) as e:
            print (e)
            print(' Could not update camera settings [NOK]')
        #with urllib.request.urlopen('http://vb.htm?title=IP-Camera&videocodec=0&localdisplay=1&mirctrl=0&videocodeccombo=4&setvideoencbitratelevel=5&iframeinterval=30&codelevel=0') as response:
        #    print(response.read())
        time.sleep(3)
		
        print('*** 1 - Make the first snapshot ***\n\n')
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        snapshot = dirstick+"snapshot"+time.strftime("_%Y%m%d_%H%M%S")+".jpeg"
        RunCmd(["./avconvv1.sh", "test"], 20).Run()
        time.sleep(20)
        #os.system("avconv -r 6  -rtsp_transport tcp -y -i "+RtspFisheye1+" -f mp4 -an -vcodec copy -t 1 movie.mp4")
        os.system("sudo avconv -ss 00:00:00.5 -t 1 -y -i "+dirstick+"movie.mp4 -f mjpeg "+snapshot)
        os.system("rm -f movie.mp4")
        print(now + ' Snapshot taken [OK]')
		
        print('*** 2 - Convert the snapshot\n\n')
        os.system("convert "+snapshot+" -crop 2070x1920+285+0 "+dirstick+"dome1.png")
        os.system("convert -size 2070x1920 xc:none -fill "+dirstick+"dome1.png -draw 'circle 1035,1010,2065,1010' "+dirstick+"dome2.png")
        os.system("convert "+dirstick+"dome2.png -resize 1024x1024 -flip "+dirstick+"dome3.png")
        os.system("convert -size 1024x1024 xc:none "+dirstick+"dome3.png -geometry +0+60 -composite "+dirstick+"dome4.png")
        now = time.strftime("%Y-%m-%d %H:%M:%S")

    if (avail==0 or avail==2):
	
        print('*** 3 - Make the second snapshot ***\n\n')
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        snapshot = dirstick+"snapshot"+time.strftime("_%Y%m%d_%H%M%S")+".jpeg"
        RunCmd(["./avconvv2.sh", "test"], 20).Run()
        time.sleep(20)
        #os.system("avconv -r 6  -rtsp_transport tcp -y -i "+RtspFisheye2+" -f mp4 -an -vcodec copy -t 1 movie.mp4")
        os.system("sudo avconv -ss 00:00:00.5 -t 1 -y -i "+dirstick+"movie.mp4 -f mjpeg "+snapshot)
        os.system("rm -f movie.mp4")
        print(now + ' Snapshot taken [OK]')
		
        print('*** 4 - Convert the second snapshot ***\n\n')
        os.system("convert -size 1280x960 xc:none -fill "+snapshot+" -draw 'circle 640,480,1,480' "+dirstick+"back1.png")
        os.system("convert "+dirstick+"back1.png -resize 1024x1024 "+dirstick+"back2.png")
        os.system("convert -size 1024x1024 xc:none "+dirstick+"back2.png -geometry +0+128 -composite "+dirstick+"back3.png")
        os.system("convert -size 1024x1024 xc:none "+dirstick+"back3.png -rotate '-90' -composite "+dirstick+"back4.png")
        #os.system("convert "+dirstick+"back4.png +level-colors navy,lemonchiffon "+dirstick+"back5.png") # blueish filter...
        now = time.strftime("%Y-%m-%d %H:%M:%S")

    print('*** 5 - Merge the pictures together\n\n')
    if (avail==0):
        os.system("composite -gravity center "+dirstick+"dome4.png "+dirstick+"back4.png "+dirstick+"dome.png")
    if (avail==1):
        # Make an overlay of the same rotated image, to fake the second camera
        os.system("convert -size 1024x1024 xc:none "+dirstick+"dome4.png -rotate '90' -composite "+dirstick+"back4.png")            
        os.system("composite -gravity center "+dirstick+"dome4.png "+dirstick+"back4.png "+dirstick+"dome.png")
        #os.system("mv "+dirstick+"dome4.png "+dirstick+"dome.png")
    if (avail==2):
        os.system("mv "+dirstick+"back4.png "+dirstick+"dome.png")

    print('*** 6 - Move fisheye to FTP server')
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

    print('*** 7 - Copy image on server to avoid partly images on website when FTP ongoing')
    try:
        r = requests.get('http://www.koperwiekweg.nl/copy_dome.php',timeout=15)
    except (requests.ConnectionError, requests.Timeout, socket.timeout) as e:
        print (e)
        print(now +' Could not copy dome.png on server [NOK]')
    
    os.system("rm -Rf "+dirstick+"*.jpeg")
    os.system("rm -Rf "+dirstick+"*.png")

    time.sleep(UpdateRate)
