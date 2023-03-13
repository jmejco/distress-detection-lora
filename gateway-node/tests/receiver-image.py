
import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm9x
from datetime import datetime
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


def send_email(message,time,signal):
    subject = "Distress Signal"
    body = f"""Distress detected on {message}
Transmission Time : {time} 
RSSI  : {signal}"""
    sender_email = "insert-email"
    receiver_email = "insert-email"
    password = "<insert-password>"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "./output.jpg"  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 868.0)
rfm9x.tx_power = 23
prev_packet = None


while True:
    packet = None
 
    # check for packet rx
    packet = rfm9x.receive(timeout=2)    

    if packet is not None:
        # # Display the packet text and rssi
        if prev_packet is None:
            # print('start reception')
            t0 = time.time()
            timestamp = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
            tmp = open('tmp.txt', 'wb+')
        prev_packet = packet
        tmp.write(prev_packet)
        print('receiving')

    if packet is None and prev_packet is not None:
        rssi_ = rfm9x.rssi
        t2 = time.time()
        total = t2-t0
        print('received')
        tmp.close()
        read_tmp = open('tmp.txt', 'rb')

        # Create the jpg file
        with open('./output.jpg', 'wb') as image_file:
            for f in read_tmp:
                image_file.write(f)

        #send_email(timestamp,total,rssi_)
        print('done')
        print(rssi_)
        print(total)
        os.remove("./tmp.txt")
        os.remove("./output.jpg")
        prev_packet = None