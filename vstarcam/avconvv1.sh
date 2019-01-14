#!/bin/sh
avconv -rtsp_transport tcp -y -i rtsp://admin:123456@192.168.178.168:554/0 -threads 0 -an -vcodec copy -t 2 /ramtmp2/movie.mp4
