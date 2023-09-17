from Libraries.ssd1306 import SSD1306_I2C
from machine import Timer
import time

# def Teleprompter(display: SSD1306_I2C, script: str, speed):
#     scriptLines = []

#     for i in range(0, len(script), 15):
#         scriptLines.append(script[i:i+15])

#     display.fill(0)

#     for i in range(2 * 128):
#         display.fill(0)

#         for index, scriptLine in enumerate(scriptLines):
#             display.text(scriptLine, 0, 63 + index * 12 - i)

#         display.show()
#         time.sleep(1 / speed) 

class Teleprompter:
    script = ""
    speed = 10

    textRows = []
    scrollTimer = Timer(69)
    running = False
    dy = 0
    dyTo = 0

    def __init__(self, display: SSD1306_I2C):
        self.display = display

    def formatScript(self):
        self.textRows = []

        # Break the script into left aligned rows with wordBreak and wordWrap property
        for lineBreak in self.script.split('\n'):
            line = ""
            scriptWords = lineBreak.split(' ')
            firstWord = True

            for scriptWord in scriptWords:
                if firstWord:
                    if len(scriptWord) <= 15:
                        line += scriptWord
                    else: # If wordbreak is necessary
                        for i in range(0, len(scriptWord), 15):
                            brokenWord = scriptWord[i : i + 15]

                            # If brokenWord fills up the whole row 
                            if len(brokenWord) == 15:
                                self.textRows.append(brokenWord)
                                line = ""
                            else:
                                line = brokenWord

                    firstWord = False
                    continue

                if len(line + ' ' + scriptWord) <= 15:
                    line += ' ' + scriptWord
                elif len(scriptWord) <= 15: # If word can be moved into the next row
                    self.textRows.append(line)
                    line = scriptWord
                else: # If wordbreak is necessary
                    self.textRows.append(line)
                    line = ""

                    for i in range(0, len(scriptWord), 15):
                        brokenWord = scriptWord[i : i + 15]

                        # If brokenWord fills up the whole row 
                        if len(brokenWord) == 15:
                            self.textRows.append(brokenWord)
                            line = ""
                        else:
                            line = brokenWord

            self.textRows.append(line)

    def showDefault(self):
        self.display.fill(0)
        self.display.rect(0, 0, 128, 64, 1)
        self.display.text('Teleprompter', 16, 28)
        self.display.show()

    def redrawText(self):
        self.display.fill(0) 

        for index, scriptRow in enumerate(self.textRows):
            y = 63 + index * 12 - self.dy

            # Only draw text that are inside the display
            if -8 < y < 64:
                self.display.text(scriptRow, 0, y)

        self.display.show()

        if self.dy + 1 == self.dyTo:
            self.stop()
        else:
            self.dy += 1 

    def start(self):
        self.formatScript()
        self.display.fill(0) 
        self.running = True

        self.dy = 0
        self.dyTo = 64 + len(self.textRows) * 12

        self.scrollTimer.init(
            period = int(1000 / self.speed),
            mode = Timer.PERIODIC,
            callback = lambda t: self.redrawText()
        )
        # for i in range(self.dyTo):
        #     if not self.running:
        #         break

        #     self.dy = i
        #     self.redrawText()
        #     time.sleep(1 / self.speed)

        # self.textRows = []
        # self.display.fill(0)
        # self.showDefault()

    def stop(self):
        # self.running = False 
        self.scrollTimer.deinit()
        self.textRows = []

        self.display.fill(0)
        self.display.show()

        time.sleep(1)
        self.showDefault()
    