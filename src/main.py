from machine import Pin
from time import sleep

pin = Pin(1, Pin.OUT)

while True:
    pin.toggle()
    sleep(1)