
import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm9x
from datetime import datetime
from functions import *

#Create the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)


#Set LoRa radio parameters
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm95 = adafruit_rfm9x.RFM9x(spi, CS, RESET, 868.0)
rfm95.tx_power = 23

#Initialize previous packet for saving data
prev_packet = None

#Initialize ACK
ack = bytes("ACK","utf-8")

while True:
    packet = None
 
    #check for packet reception
    packet = rfm95.receive()    

    if packet is not None:

        #Send acknowledgement back to local node on reception of data
        rfm95.send(ack)
        if prev_packet is None:

            #Capture timestamp at the start of reception
            timestamp = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")

        #Save data to packet    
        prev_packet = packet

        #Reconstruct the received data packet
        signal = reconstruct(prev_packet)

    if packet is None and prev_packet is not None:
        
        #Send email using reconstructed data
        send_email(signal,timestamp)
        
        #Reset previous packet to continue listening
        prev_packet = None
        time.sleep(1.0)