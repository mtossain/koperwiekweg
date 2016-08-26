#!/bin/sh
avconv -rtsp_transport tcp -y -i rtsp://admin:123456@192.168.178.254:554/mpeg4 -vcodec copy -t 2 /ramtmp/movie.mp4
