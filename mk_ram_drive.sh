#!/bin/bash
#new comment
sudo echo 'none   /ramtmp   tmpfs   size=40M,noatime   00' >> /etc/fstab
sudo mkdir /ramtmp
sudo mount -a
