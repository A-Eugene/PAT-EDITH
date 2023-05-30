from machine import Pin
import time

led = Pin(26, Pin.OUT)
led.on()
time.sleep(1)
led.off()