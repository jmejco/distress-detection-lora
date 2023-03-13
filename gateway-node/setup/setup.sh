#!/bin/sh

#Update package lists and upgrade packages
sudo apt-get update
sudo apt-get upgrade -y

#Clean redundant files
sudo apt-get clean
sudo apt-get autoremove -y

#Set python3.7 as default
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2

#Install pip for python3
sudo apt-get install python3-pip
pip3 install --upgrade pip

#Install python libraries for LoRa bonnet
sudo pip3 install RPI.GPIO
sudo pip3 install adafruit-blinka
sudo pip3 install adafruit-circuitpython-ssd1306
sudo pip3 install adafruit-circuitpython-framebuf
sudo pip3 install adafruit-circuitpython-rfm9x