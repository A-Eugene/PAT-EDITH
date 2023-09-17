from machine import Timer
from Libraries.ssd1306 import SSD1306_I2C

class Stopwatch:
    timer = Timer(91)
    time = {
        'm': 0,
        's': 0,
        'ms': 0
    }

    def __init__(self, display: SSD1306_I2C):
        self.display = display

    def showDefault(self):
        self.display.fill(0)
        self.display.rect(0, 0, 128, 64, 1)
        self.display.text('00:00.00', 32, 28)
        self.display.show()

    def tick(self):
        if self.time['ms'] + 10 > 99:
            if self.time['s'] + 1 > 59:
                if self.time['m'] + 1 > 99:
                    self.stop()
                else:
                    self.time['m'] += 1

                self.time['s'] = 0
            else:
                self.time['s'] += 1

            self.time['ms'] = 0
        else:
            self.time['ms'] += 10 

        self.display.fill(0)
        self.display.text(f'{"{:02}".format(self.time["m"])}:{"{:02}".format(self.time["s"])}.{"{:02}".format(self.time["ms"])}', 32, 28)
        self.display.show() 
 
    def start(self):
        self.time = {
            'm': 0,
            's': 0,
            'ms': 0
        }

        self.timer.init(
            period = 100,
            mode = Timer.PERIODIC,
            callback = lambda t: self.tick()
        )

    def stop(self):
        self.timer.deinit()
        self.display.rect(0, 0, 128, 64, 1)
        self.display.show()
