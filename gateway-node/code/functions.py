import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import *

def send_email(message,time):
    email = SENDER_EMAIL
    password = PASSWORD
    send_to_email = RECEIVER_EMAIL
    subject = 'Distress Signal' 
    body = f"""Distress detected on: {time}
Detections : {message}"""

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    #Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string() # You now need to convert the MIMEMultipart object to a string to send
    server.sendmail(email, send_to_email, text)
    server.quit()



CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat","bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


def reconstruct(data):
    #Convert received bytes into string and split into classes 
    tmp = str(data, "utf-8").split()
    classes=[]
    for i in tmp:
        tmp.append(i.split(':'))
    #Derive class labels from indices and create dictionary
    output = {CLASSES[int(idx[0])]:idx[1] for idx in classes}
    return output