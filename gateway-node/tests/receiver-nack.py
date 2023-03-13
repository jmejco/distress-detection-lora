
import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm9x
from datetime import datetime
import os


# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 868.0)
rfm9x.tx_power = 23
prev_packet = None
ack = bytes("ACK","utf-8")


while True:
    packet = None
 
    # check for packet rx
    packet = rfm9x.receive()    

    if packet is not None:
        rfm9x.send(ack)
        if prev_packet is None:
            print('start reception')
            t0 = time.time()
        prev_packet = packet
        packet_text = str(prev_packet, "utf-8")
        print('foo')

    if packet is None and prev_packet is not None:
        rssi_ = rfm9x.rssi
        t1 = time.time()
        total = t1-t0
        #send_email(packet_text,total,rssi_)
        print('packet_text')
        prev_packet = None