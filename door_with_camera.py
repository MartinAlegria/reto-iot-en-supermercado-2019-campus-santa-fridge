import RPi.GPIO as GPIO
import time
import subprocess
from datetime import datetime
import requests
from pprint import pprint
import sys
import signal
import time

def snap_photo():
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



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#SETUP PARA PUERTA
door_pin = 14
buzzer_pin = 18
GPIO.setup(door_pin, GPIO.IN,pull_up_down = GPIO.PUD_UP)
GPIO.setup(buzzer_pin, GPIO.OUT)

#counter
i = 0
photo = True
while(True):
    #EL SENSOR ESTA ABIERTO
    if GPIO.input(14) == True:
        print("ABIERTO")
        if photo:
            snap_photo()
            photo = False
        if i >= 5: #SEÑAL DE PUERTA ABIERA CUANDO ES MAYOR A UN TIEMPO DETERMINADO
            GPIO.output(18,GPIO.HIGH)
        time.sleep(1)
        i += 1
    #EL SENSOR ESTA CERRADO
    else:
        print("CERRADO")
        i = 0
        photo = True
        GPIO.output(18,GPIO.LOW)
        time.sleep(1)



