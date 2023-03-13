import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm9x
from datetime import datetime

# Maximum chunk size that can be sent
CHUNK_SIZE = 250

# Location of source image
image_file = './test.jpg'

# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
 
# 128x32 OLED Display
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height
 
# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 868.0)
rfm9x.tx_power = 23

prev_packet = None
 
while True:
 

    if not btnA.value:
        with open(image_file, 'rb') as infile:
            while True:
                # Read 250byte chunks of the image
                chunk = infile.read(CHUNK_SIZE)
                if not chunk: 
                    break
                rfm9x.send(chunk, timeout=2.0)


    elif not btnB.value:
        # Send Button B
        display.fill(0)
        timestamp = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
        payload = bytes(timestamp,"utf-8")
        while True:
            rfm9x.send(payload)
            print('sent')
            display.text('Sent Button B!', 25, 15, 1)
            display.show()
            packet = None
            packet = rfm9x.receive()

            if packet is not None:
                prev_packet = packet
                packet_text = str(prev_packet, "utf-8")

                if packet_text == "ACK":
                    print('ack received')
                    display.fill(0)
                    display.text('RasPi ACK', 35, 0, 1)
                    display.show()
                    time.sleep(1.0)
                    break

            else:
                print('no ack')
                display.fill(0)
                display.text('RasPi NACK', 35, 0, 1)
                display.show()
                time.sleep(1.0)
                continue
        
        display.fill(0)
    display.show()
    time.sleep(0.1)