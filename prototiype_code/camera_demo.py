import RPi.GPIO as GPIO
import time
import subprocess
from datetime import datetime
import requests
from pprint import pprint
import sys
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#PONER CHANNEL AC
channel = 40
ccccc


def callbackCamera(channel):
    if GPIO.input(channel) == GPIO.HIGH:
        #sound detected
        print("sound detected")
        subprocess.call(['fswebcam -r 640x480 --no-banner /home/pi/Desktop/image2.jpg', '-1'],shell =True)
        analyze()

def analyze():
    #AZURE
    face_uri = "https://raspberrycp.cognitiveservices.azure.com/vision/v1.0/analyze?visualFeatures=Faces&language=en"
    pathToFileInDisk = r'/home/pi/Desktop/image2.jpg'
    with open( pathToFileInDisk, 'rb' ) as f:
        data = f.read()

    headers = { "Content-Type": "application/octet-stream" ,'Ocp-Apim-Subscription-Key': '7e9cfbb244204fb994babd6111235269'}
    response = requests.post(face_uri, headers=headers, data=data)
    faces = response.json()
    pprint(faces)


GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime = 300)
GPIO.add_event_callback(channel,callbackCamera)