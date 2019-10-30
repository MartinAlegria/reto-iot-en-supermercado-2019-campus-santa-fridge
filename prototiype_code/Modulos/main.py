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
from camera_module import camera_module
import upload_face_data
import rfid

def write_transaction(t):
    t = str(t)
    text_file = open("/home/pi/Desktop/SantaFridge/Modulos/transaction.txt", "w")
    text_file.write(t)
    text_file.close()

def read_transaction():
    transaction = open("/home/pi/Desktop/SantaFridge/Modulos/transaction.txt", "r")
    t = transaction.read(1)
    t = int(t)
    transaction.close()
    return t

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

transaction = read_transaction()

#SETUP PARA PUERTA
door_pin = 21
buzzer_pin = 18
GPIO.setup(door_pin, GPIO.IN,pull_up_down = GPIO.PUD_UP)
#GPIO.setup(buzzer_pin, GPIO.OUT)

#counter
i = 0
photo = True

#SYSTEM LOOP
while(True):

    #LA PUERTA ESTA ABIERTA
    if GPIO.input(door_pin) == True:
        #print("ABIERTO")

        #PROCESO QUE MANDA DATOS DE CARA A AZURE COG.SER. Y LOS SUBE A GCP
        if photo:
            faces_data =camera_module.snap_photo()
            transaction +=1
            upload_face_data.upload_data(transaction,faces_data)
            write_transaction(transaction)
            photo = False


        #if i >= 5: #SEÑAL DE PUERTA ABIERA CUANDO ES MAYOR A UN TIEMPO DETERMINADO
           # GPIO.output(18,GPIO.HIGH)
        time.sleep(0.8)
        i += 1



    #EL SENSOR ESTA CERRADO
    else:
        #print("CERRADO")
        i = 0
        photo = True
        #GPIO.output(18,GPIO.LOW)
        time.sleep(1)

