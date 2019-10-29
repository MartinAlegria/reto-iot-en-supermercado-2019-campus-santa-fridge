import RPi.GPIO as GPIO
import time
import subprocess
from datetime import datetime
import requests
from pprint import pprint
import sys
import signal
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#pin.DOOR_SENSOR_PIN = 14

GPIO.setup(14, GPIO.IN,pull_up_down = GPIO.PUD_UP)
GPIO.setup(18, GPIO.OUT)
i = 0

while(True):
    #EL SENSOR ESTA ABIERTO
    if GPIO.input(14) == True:
        print("ABIERTO")
        if i >= 5: #SEÑAL DE PUERTA ABIERA CUANDO ES MAYOR A UN TIEMPO DETERMINADO
            GPIO.output(18,GPIO.HIGH)
        time.sleep(1)
        i += 1
    #EL SENSOR ESTA CERRADO
    else:
        print("CERRADO")
        i = 0
        GPIO.output(18,GPIO.LOW)
        time.sleep(1)



