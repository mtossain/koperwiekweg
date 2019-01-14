#!/bin/bash
#new comment
sudo echo 'none   /ramtmp2   tmpfs   size=40M,noatime   00' >> /etc/fstab
sudo mkdir /ramtmp2
sudo mount -a
