import RPi.GPIO as GPIO
import sys
import Adafruit_DHT
import time

sensor = Adafruit_DHT.DHT11
pin =23

GPIO.setmode(GPIO.BOARD)

def temperatura():
    print("asdasdas")
    humedad, temperatura = Adafruit_DHT.read(sensor,pin)
    if temperatura is None:
        print("NONE")
        return 0
    else:
        return temperatura