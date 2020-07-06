#!/bin/bash
sudo apt-get install python3-pip -y
sudo apt-get install python3-dev -y
pip3 install pillow spidev google-api-python-client google-auth-httplib2 google-auth-oauthlib
sudo apt-get install python3-RPi.GPIO -y
sudo apt-get install libopenjp2-7 -y
sudo apt install libtiff5 -y

sudo cp /home/pi/EPaperDisplay/EPaper.service /etc/systemd/system/
sudo systemctl enable EPaper.service
sudo systemctl start EPaper.service