import time
import framebuf

from Libraries.ssd1306 import SSD1306_I2C

from Displays.Images import LogoMDC

"""
    Character size: 8x8 pixels
    y distance per line: 12 pixels
"""

class SecondaryDisplays():
    def __init__(self, display: SSD1306_I2C):
        self.display = display
        
    def showReady(self):
        self.display.fill(0)
        self.display.rect(0, 0, 128, 64, 1)
        self.display.text('Device', 40, 22)
        self.display.text('Ready!', 40, 34)
        self.display.show()
        
    def waitForConnection(self):
        self.display.fill(0)
        self.display.rect(0, 0, 128, 64, 1)
        self.display.text('Waiting', 36, 16)
        self.display.text('for', 52, 28)
        self.display.text('Connection', 24, 40)
        self.display.show()

    def startup(self):
        self.display.fill(0)

        fb = framebuf.FrameBuffer(LogoMDC, 64, 64, framebuf.MONO_HLSB)
        self.display.blit(fb, 32, 0)
        self.display.show()

        for x in range(0, 128, 2):
            self.display.pixel(x, 0, 1)
            self.display.pixel(x + 1, 0, 1)
            self.display.pixel(127 - x, 63, 1)
            self.display.pixel(127 - x - 1, 63, 1)

            self.display.show()
            time.sleep_ms(10)

        for y in range(0, 64, 2):
            self.display.pixel(0, 63 - y, 1)
            self.display.pixel(0, 63 - y - 1, 1)
            self.display.pixel(127, y, 1)
            self.display.pixel(127, y + 1, 1)
            self.display.show()
            time.sleep_ms(10)

        time.sleep_ms(500)
