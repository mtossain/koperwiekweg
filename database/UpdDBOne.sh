#!/bin/bash

ssh -Ng -L 3306:127.0.0.1:3306 hjvveluw@s14.servitnow.nl &
echo 'Opened SSH tunnel [OK]'
PID=$!
echo mlu | sudo python insertone.py
echo mlu | sudo kill -9 $PID
echo 'Closed SSH tunnel [OK]'

