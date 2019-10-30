#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import subprocess
from datetime import datetime
import requests
from pprint import pprint
import sys
import signal
import time

class camera_module():

    def snap_photo():
        subprocess.call(['fswebcam -r 640x480 --no-banner /home/pi/Desktop/image.jpg', '-1'],shell =True)
        try:
            #AZURE
            face_uri = "https://raspberrycp.cognitiveservices.azure.com/vision/v1.0/analyze?visualFeatures=Faces&language=en"
            pathToFileInDisk = r'/home/pi/Desktop/image.jpg'
            with open( pathToFileInDisk, 'rb' ) as f:
                data = f.read()

            headers = { "Content-Type": "application/octet-stream" ,'Ocp-Apim-Subscription-Key': '7e9cfbb244204fb994babd6111235269'}
            response = requests.post(face_uri, headers=headers, data=data)
            faces = response.json()
            #pprint(faces)
            """
            faces[] = lista de diccionarios de rasgos
            f[0]['age'] -> Edad
            """
            f=faces['faces']
            #print(f)

            #DATOS A SUBIR
            #print("\n Age: ",f[0]['age'])
            #print("Gender: ",f[0]['gender'])

            return f

        except IndexError as error:
            # Error handling para cuando no encuentra ninguna cara
            print(error)