from machine import Pin
import time
import ssd1306

# Using GP1 for VCC, breadboard limitation
VCC = Pin(1, Pin.OUT)
VCC.on()

def main():
  while True:
    VCC.toggle()
    time.sleep(1)

main()