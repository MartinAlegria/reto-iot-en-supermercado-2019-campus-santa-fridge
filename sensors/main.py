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
from rfid import read_rfid
from db_query import query_product
from temp_sensor import temperatura


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

def sound_buzzer():
    GPIO.output(buzzer_pin,GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(buzzer_pin,GPIO.LOW)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

transaction = read_transaction()

#SETUP PARA PUERTA
door_pin = 40
buzzer_pin = 38

GPIO.setup(door_pin, GPIO.IN,pull_up_down = GPIO.PUD_UP)
GPIO.setup(buzzer_pin, GPIO.OUT)

#counter
i = 0
photo = True

#SYSTEM LOOP
while(True):

    #ANADIR ACCIONES DE ADMINISTRADOR

    #LA PUERTA ESTA ABIERTA
    if GPIO.input(door_pin) == True:
        #print("ABIERTO")
        t = temperatura()
        if t != 0 and t >25:
            sound_buzzer()

        #PROCESO QUE MANDA DATOS DE CARA A AZURE COG.SER. Y LOS SUBE A GCP
        if photo:
            faces_data =camera_module.snap_photo()
            transaction +=1
            upload_face_data.upload_data(transaction,faces_data)
            write_transaction(transaction)
            photo = False

        print("Scanning.....")
        id = read_rfid()
        print("Found")
        sound_buzzer()

        product_data = query_product(id)
        product_data.append(transaction)

        #ES UN PRODUCTO VALIDO/EN LA DB
        if product_data[0] != '':
            print(product_data)
            print("VALIDO")
        else:
            print("PRODUCTO NO VALIDO")

        """
        if i >= 5: #SEÑAL DE PUERTA ABIERA CUANDO ES MAYOR A UN TIEMPO DETERMINADO
           GPIO.output(18,GPIO.HIGH)
        time.sleep(0.5)
        i += 1"""

    #EL SENSOR ESTA CERRADO
    else:
        t = temperatura()
        if t != 0 and t >25:
            sound_buzzer()

        #print("CERRADO")
        i = 0
        photo = True
        #GPIO.output(18,GPIO.LOW)
        time.sleep(1)