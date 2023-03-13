
#########################################################################################################################

#Import opencv and numpy
import cv2, numpy as np


#Initialize classes on which the mobilenet SSD was trained on
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat","bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

#Construct ignore list to exclude unwanted classes
IGNORE = ["bottle", "chair", "diningtable", "pottedplant", "sheep", "sofa", "tvmonitor"]

#Initialize the path of the pre-trained classification network

PROTOTXT = "/home/pi/code/ssd.prototxt"
CAFFEMODEL = "/home/pi/code/ssd.caffemodel"

def classify(image):

    #Load caffemodel and prototxt
    model = cv2.dnn.readNetFromCaffe(PROTOTXT, CAFFEMODEL)

    #Extract the frame size
    (h, w) = image.shape[:2]

    #Compute 300x300px blob from the image
    #The function parameters are specific to the mobilenet ssd used
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

    #Set blob as input and compute labels by passing it through the network
    model.setInput(blob)
    labels = model.forward()
    
    #Initialize payload for LoRa
    payload=""

    #Loop through all labels
    for i in np.arange(0, labels.shape[2]):
        
        #extract confidence levels
        confidence = labels[0, 0, i, 2]

        #Set minimum threshold for confidence
        if confidence > 0.2:
            #Extract class labels
            idx = int(labels[0, 0, i, 1])

            #Ignore unwanted classes
            if CLASSES[idx] in IGNORE:
                continue
            
            #Construct LoRa payload
            label = f"{idx}:{(confidence * 100):.2f} "
            payload += label

            #Return payload if person is identified
            if idx == 15:
                return payload


###################################################################################################

#Import python libraried for the LoRa bonnet

import busio, board, adafruit_rfm9x
from digitalio import DigitalInOut

def send_lora(data):
 
    #Initialize the I2C interface
    i2c = busio.I2C(board.SCL, board.SDA)
 
    # Configure LoRa Radio
    CS = DigitalInOut(board.CE1)
    RESET = DigitalInOut(board.D25)
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

    #Setting frequency as 868Mhz to conform with EU Radio Regulations
    rfm95 = adafruit_rfm9x.RFM9x(spi, CS, RESET, 868.0)

    #Maximum transmission power
    rfm95.tx_power = 23

    #Initialize previous packet as none for saving
    prev_packet = None

    #Convert payload to bytes array for transmission
    lora_payload = bytes(data,"utf-8")

    while True:

        #Sending packet
        rfm95.send(lora_payload)

        #Setting current packet as none to keep receiving
        packet = None
        packet = rfm95.receive()

        if packet is not None:

            #Save previous packet upon reception of ACK from gateway
            prev_packet = packet
            packet_text = str(prev_packet, "utf-8")

            #Confirming ACK
            if packet_text == "ACK":
                break
        else:
            #Continuing reception until ACK is received
            continue
