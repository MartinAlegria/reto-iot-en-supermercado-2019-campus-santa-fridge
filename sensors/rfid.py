#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import sys
sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def read_rfid():
    id, text=reader.read()
    print(id)
    return id
    #print(text)

def write_rfid():
    text = input("Write your input here")
    id, text=reader.write(text)
    print("recorded")
    print(id)
    print(text)

def admin_actions():
    while True:
        try:
            try:
                choice=int(input('1 to read RFID, 0 to write'))
                if choice ==1:
                    print("Si")
                    while True:
                        smth = read_rfid()
                        if smth:
                            break
                    print("Reading Succesful")
                elif choice == 0:
                    while True:
                        write_rfid()
                #else:
                  #  print("Not a valid choice, try again")
            except ValueError as error:
                print(error)
        finally:
            GPIO.cleanup()