#!/bin/sh


#Install the necessary linux system packages

sudo apt-get install build-essential cmake unzip pkg-config libjpeg-dev libpng-dev libtiff-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libcanberra-gtk* libatlas-base-dev gfortran python3-dev python-picamera python3-picamera

#Download the source code for OpenCV 4.0

cd /home/pi
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.0.0.zip
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.0.0.zip
unzip opencv.zip
unzip opencv_contrib.zip
mv opencv-4.0.0 opencv
mv opencv_contrib-4.0.0 opencv_contrib

#Install Numpy which is a requirement for opencv
sudo pip3 install numpy


#Set build directory
mkdir /home/pi/opencv/build
cd /home/pi/opencv/build

#Optimised OpenCV install paraemeters
 cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
-D ENABLE_NEON=ON \
-D ENABLE_VFPV3=ON \
-D BUILD_TESTS=OFF \
-D OPENCV_ENABLE_NONFREE=ON \
-D INSTALL_PYTHON_EXAMPLES=OFF \
-D BUILD_EXAMPLES=OFF ..

#Increase swap size so that build doesn't hang
sudo sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=2048/' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start


#Build opencv from source
make -j4
sudo make install
sudo ldconfig

#Link cv2 to enable python imports
ln -s /usr/local/python/cv2/python-3.7/cv2.cpython-37m-arm-linux-gnueabihf.so /home/pi/.local/lib/python3.7/site-packages/cv2.so

#Install imutils which needs opencv
sudo pip3 install imutils

#Clean up
cd /home/pi
rm -rf opencv opencv_contrib opencv.zip opencv_contrib.zip