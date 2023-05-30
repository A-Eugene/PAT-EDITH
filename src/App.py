from machine import Pin, SoftI2C, Timer

from Libraries.ssd1306 import SSD1306_I2C
from Libraries.ESP32BLE import ESP32_BLE
from Libraries.BLEJSONInstruction import BLEInstructionParser
from Displays.SecondaryDisplays import SecondaryDisplays

""" BEGIN CONFIGURATION """

# GPIO Pins
SDA_PIN = 21  # Gray
SCL_PIN = 22  # Green

# Display Information
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
MIRRORED = False

""" END CONFIGURATION """

display = SSD1306_I2C(
    width=DISPLAY_WIDTH,
    height=DISPLAY_HEIGHT,
    i2c=SoftI2C(
        sda=Pin(SDA_PIN),
        scl=Pin(SCL_PIN)
    )
)

# Possible values: Startup, WaitingConnection, Ready
currentDisplay = 'Startup'
secondaryDisplays = SecondaryDisplays(display)

bluetooth = ESP32_BLE(name='EDITH', blinkLED=False)
instructionParser = BLEInstructionParser(bluetooth)

def on_bluetooth_connected():
    global currentDisplay
    currentDisplay = 'Ready'
    secondaryDisplays.showReady()

def on_bluetooth_disconnected():
    global currentDisplay
    currentDisplay = 'WaitingConnection'
    secondaryDisplays.waitForConnection()

def on_bluetooth_instruction(instruction):
    print(instruction)
    instructionParser.sendMessage('Created InstructionParser.py; Since Bluetooth Low Energy is limited to 20 bytes (characters) per message, it is a challenge to send large amount of instructional data. InstructionParser.py is a library that decodes array of strings into a JSON instruction for easier use.')

bluetooth.on('connected', on_bluetooth_connected)
bluetooth.on('disconnected', on_bluetooth_disconnected)
bluetooth.on('message', instructionParser.feedChunk)

instructionParser.on_instruction(on_bluetooth_instruction)

def main():
    if MIRRORED:
        display.write_cmd(0xA0)

    secondaryDisplays.startup()
    secondaryDisplays.waitForConnection()


main()
