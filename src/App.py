from machine import Pin, SoftI2C, Timer
import gc
from micropython import mem_info, alloc_emergency_exception_buf

from Libraries.ssd1306 import SSD1306_I2C
from Libraries.ESP32BLE import ESP32_BLE
from Libraries.BLEJSONInstruction import BLEJSONInstruction
from Displays.SecondaryDisplays import SecondaryDisplays
from Displays.Teleprompter import Teleprompter
from Displays.Stopwatch import Stopwatch

""" BEGIN CONFIGURATION """

# GPIO Pins
SDA_PIN = 21  # Gray
SCL_PIN = 22  # Green

# Display Information
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
MIRRORED = True

""" END CONFIGURATION """

alloc_emergency_exception_buf(320)

display = SSD1306_I2C(
    width=DISPLAY_WIDTH,
    height=DISPLAY_HEIGHT,
    i2c=SoftI2C(
        sda=Pin(SDA_PIN),
        scl=Pin(SCL_PIN)
    )
)

bluetooth = ESP32_BLE(name='EDITH', blinkLED=False) 
BLEInstruction = BLEJSONInstruction(bluetooth)

# Load features
secondaryDisplays = SecondaryDisplays(display)
teleprompter = Teleprompter(display)
stopwatch = Stopwatch(display)

# Bluetooth Event Handler
def on_bluetooth_connected():
    secondaryDisplays.showHome()

def on_bluetooth_disconnected():
    secondaryDisplays.waitForConnection()

def on_bluetooth_message(message):
    # print(message)
    BLEInstruction.feedChunk(message)

def on_bluetooth_instruction(instruction):
    try:
        print(instruction)
        # {"feature": "Home"} 
        if instruction['feature'] == 'Home':
            secondaryDisplays.showHome()
            return
        
        if instruction['feature'] == 'Teleprompter':
            if 'action' in instruction:
                if instruction['action'] == 'Start':
                    if 'script' in instruction.keys() and 'speed' in instruction.keys():
                        teleprompter.script = instruction['script']
                        teleprompter.speed = instruction['speed']
                        
                        teleprompter.start()
                elif instruction['action'] == 'Stop': 
                    teleprompter.stop()
            else: 
                teleprompter.showDefault()

        if instruction['feature'] == 'Stopwatch':
            if 'action' in instruction:
                if instruction['action'] == 'Start':
                    stopwatch.start()
                elif instruction['action'] == 'Stop':
                    stopwatch.stop()
            else:
                stopwatch.showDefault()

    except Exception as e:
        print('Error:', e) #
        
# Bluetooth Events
bluetooth.on('connected', on_bluetooth_connected)
bluetooth.on('disconnected', on_bluetooth_disconnected)
bluetooth.on('message', on_bluetooth_message)

BLEInstruction.on_instruction(on_bluetooth_instruction) 

def main():
    if MIRRORED:
        display.write_cmd(0xA0)

    secondaryDisplays.startup()
    secondaryDisplays.waitForConnection()

    e = Timer(10) 
    e.init(
        period=1000,
        mode=Timer.PERIODIC,
        callback=lambda t: gc.collect()
    )

main() 