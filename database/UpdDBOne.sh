#!/bin/bash

ssh -Ng -L 3307:127.0.0.1:3307 hjvveluw@server2.bhosted.nl &
echo 'Opened SSH tunnel [OK]'
PID=$!
echo mlu | sudo python insertone.py
echo mlu | sudo kill -9 $PID
echo 'Closed SSH tunnel [OK]'
