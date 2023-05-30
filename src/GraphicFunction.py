from machine import Pin, SoftI2C
import Libraries.ssd1306 as ssd1306
import time
import math

# GPIO Pins
SDA_PIN = 26 # Gray
SCL_PIN = 27 # Green

# Display Information
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64

# using SoftI2C
i2c = SoftI2C(sda=Pin(SDA_PIN), scl=Pin(SCL_PIN))
display = ssd1306.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c)

def absXPos(x: float):
    return round(x + 64)

def absYPos(y: float):
    return round(32 - y)

def f(x):
    result = 10 * math.cos(x)
    return result

def main():
    display.fill(0)

    # Sumbu X
    display.line(0, 32, 128, 32, 1)

    # Sumbu Y
    display.line(64, 0, 64, 64, 1)

    x = -64

    while x < 64:
        try:
            y = f(x)

            display.pixel(absXPos(x), absYPos(y), 1)
        except:
            pass

        # Incremental accuracy
        x += 0.05

    display.show()
main()