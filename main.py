#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import subprocess
import sys
import signal
import time
sys.path.append('/home/pi/Desktop/SantaFridge/Modulos/sensors')
sys.path.append('/home/pi/Desktop/SantaFridge/Modulos/backend')
from camera_module import snap_photo
import upload_face_data as upload_face_data
from rfid import read_rfid
from db_query import query_product
from temp_sensor import temperatura
import upload_products as upload_products


def write_transaction(t):
    t = str(t)
    text_file = open("/home/pi/Desktop/SantaFridge/Modulos/datasets/transaction.txt", "w")
    text_file.write(t)
    text_file.close()

def read_transaction():
    transaction = open("/home/pi/Desktop/SantaFridge/Modulos/datasets/transaction.txt", "r")
    t = transaction.read()
    line = list(t)
    number = ""
    for thing in line:
        number += str(thing)
    transaction.close()
    return int(number)

def sound_buzzer():
    GPIO.output(buzzer_pin,GPIO.HIGH)
    time.sleep(0.25)
    GPIO.output(buzzer_pin,GPIO.LOW)

def led_on():
    GPIO.output(led_pin,GPIO.HIGH)

def led_off():
    GPIO.output(led_pin,GPIO.LOW)


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)



#SETUP PARA PUERTA
door_pin = 40
buzzer_pin = 38
led_pin = 12

GPIO.setup(door_pin, GPIO.IN,pull_up_down = GPIO.PUD_UP)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(led_pin, GPIO.OUT)

#counter
i = 0
photo = True

#SYSTEM LOOP
while(True):
    #ANADIR ACCIONES DE ADMINISTRADOR
    #LA PUERTA ESTA ABIERTA
    transaction = read_transaction()
    print("Transaction: ", transaction)

    if GPIO.input(door_pin) == True:
        print("PUERTA ABIERTA")
        #print("ABIERTO")
        t = temperatura()
        if t != 0 and t >25:
            sound_buzzer()
        #PROCESO QUE MANDA DATOS DE CARA A AZURE COG.SER. Y LOS SUBE A GCP
        if photo:
            faces_data =snap_photo()
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
            time.sleep(0.5)
            print(product_data)
            print("VALIDO")
            upload_products.upload_data(transaction,product_data)
        else:
            time.sleep(0.5)
            print("PRODUCTO NO VALIDO")

        for i in range(1,5):
            #sound_buzzer()
            print(" ****** CIERRA LA PUERTA *******")
            led_on()
            sound_buzzer()
            time.sleep(0.5)
            led_off()
            time.sleep(0.5)

    #EL SENSOR ESTA CERRADO
    else:
        print("PUERTA CERRADA")
        t = temperatura()
        if t != 0 and t >25:
            sound_buzzer()
        i = 0
        photo = True
        time.sleep(1)