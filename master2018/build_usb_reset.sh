gcc usb_reset.c -o usb_reset
sudo mv usb_reset /usr/local/sbin/
sudo chown root:root /usr/local/sbin/usb_reset
sudo chmod 0755 /usr/local/sbin/usb_reset
lsusb | cat
sudo usb_reset /dev/bus/usb/001/009
