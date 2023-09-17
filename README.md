# PAT - EDITH
It's some sort of smart display mounted on your glasses while projecting images or texts from a bluetooth low energy peer.

![Raspberry PI Pico W Pinout](https://www.raspberrypi-spy.co.uk/wp-content/uploads/2022/11/raspberry_pi_pico_w_pinout.png)

![ESP32 Wroom DevKit Pinout](https://www.mischianti.org/wp-content/uploads/2020/11/ESP32-DOIT-DEV-KIT-v1-pinout-mischianti.png)

## Female to Female Cable Mapping
| Port   | Color |
| ----------- | ----------- |
| 3V3      | Orange (ideally red, but the red one is not rigid)      |
| GND   | Black     |
| GP22      | Brown      |
| GP21   | White     |

## Breadboard Cable Mapping
| Port   | Color |
| ----------- | ----------- |
| 3V3      | Red     |
| GND   | Black     |
| GP22      | Green      |
| GP21   | Gray  |

## Build Log
- **18 May 2023**
  - Initialized the project using Pico-W-Go 2.18 VScode Extension (later versions seems to have problem initializing vREPL terminal to Pico)
  - Initialized the project to github
  - Added ./main.py which adds ./src folder as a package and runs ./src/main.py by importing it on startup, so ./src/main.py can run on startup while that and other scripts remain organized in ./src instead of floating all over the root folder.
  - Tested the OLED display and works
  - (TODO) Test something with internet connection and create the client
- **20 May 2023**
  - Met an error in which "Upload failed.Hashes do not match between computer and board. Hashes do not match between computer and board." As it suggests, this happens because of the mismatch of the source codes. Whether it's Pico's issue or the VSCode extension's issue is unknown, however a website mentioned that it's due to corrupted files inside Pico's storage. To fix this, simply move all the source codes temporarily into another folder and add a new source code, and then upload it to the Pico. Pico will then compare the files in the source code directory and it's storage and remove the so called corrupted files, and copies the healthy code into it. Move the original source code back into the working directory and you're good to go.
  - When source code just does not seem to get executed, purposefully create an error in one of the scripts, upload, and then remove the error. Sometimes it gets fixed. What the hell.
  - (TODO) Replace the usage of PYTHONPATH to importing absolute path for module imports. Example: src.Libraries.gfx, src.Routes.Intro.
  - (DONE) Added ./src to PYTHONPATH, created "Libraries" directory and probably other directories in the future to tidy things up. Since ./src is in PYTHONPATH, the import name has changed from having "src." prefix to none. Example: src.Libraries.gfx becomes Libraries.gfx
  - Found the way to mirror display. Simply add "display.write_cmd(0xA0)" after the display initialization and it gets flipped.
  - Correction to the first point: when this happens just turn off the Rasp PI for a while.
- **21 May 2023**
  - After 4 HOURS OF SEARCHING the correct SSD1306 driver which supports display.text, display.blit and everything else, turns out the one used as the standard is Stefan Lehmann's library, which is a fork of the original SSD1306 driver by Adafruit. In the original driver by Adafruit, .text(), .fill(), .pixel() and other methods are written directly on the class. In Stefan's version these methods are replaced by directly returning the Framebuffer methods which are WAY MORE COMPREHENSIVE than Adafruit's. This explains why .blit() method cannot be found anywhere. It is a Framebuffer method, not SSD1306_I2C's.
  - (DONE) Replaced Adafruit's SSD1306 driver with Stefan Lehmann's. Thank you so much Stefan.
- **27 May 2023**
  - Bought ESP32 Wroom Devkit V1. In order to communicate with it via Serial Port you need to install a driver from [Silicon Labs's official Driver](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=documentation) by unzipping the file, and right click install on silabs.inf.
  - To install Micropython on ESP32, you need to use esptool.py and use the command provided by the docs. The Micropython binary is downloaded from it's official site.
  - (UHHH) Both new and old display works, just when display decided not to work just unplug SDA cable, reset, plug the SDA cable back in, and reset. It MAY work, it has worked 3 times but still unclear whether it's just luck.
  - Maybe also try scanning the I2c, then initialize the display class, then send display.write_cmd(0xe4) using the REPL. 
  - Probably the display is a hardware issue. First, SDA is not meant to be plugged off without turning the power off. Second, it probably isn't entirely the data, probably something with SCL or VCC that got plugged in and out really quickly causing the display to die or something. display.write_cmd(0xe4) doesn't seem to do anything, yet.
  - Yes it's most likely the display's issue. After switching the display that just had an error with one that does not the code works instantly.
- **28 May 2023**
  - Display for connected and disconnected state works.
- **30 May 2023**
  - Modified bluetooth.py; now events are registered as callbacks to the instance of the class and you can add multiple callbacks
  - Created BLEJSONInstruction.py; Since Bluetooth Low Energy is limited to 20 bytes (characters) per message, it is a challenge to send large amount of instructional data. BLEJSONInstruction.py is a library that decodes array of strings into a JSON instruction for easier use. 
  - Found a different behaviour between Micropython's json module and regular Python's. Micropython's does not throw an error when it should. If you were to run
    ```py
        import json
        
        json.loads('{"th": ')
        # raises an Exception in regular Python
        # returns {} in Micropython
    ```
    the solution is to ignore empty dictionary instruction in Micropython. Whenever it encounters {} it will just clear self.message and return. 
- Found a some different game-changing behaviour on Micropython's json module, more explained in BLEJSONInstruction.py
- Okay, I think BLEJSONInstruction.py is ready, time to translate it to Typescript
- **3 June 2023**
  - Removed .strip() in _IRQ_GATTS_WRITE since it corrupts spaces in BLEJSONInstruction
  - Teleprompter seems to work fine EXCEPT ESP32 seems to crash after Stop is pressed. Out of RAM? The console said it was stackoverflow, probably need some optimization.
- **5 June 2023**
  - Stopwatch works, however tick's delay does not seem to be valid (too slow)
  - Stopwatch needs number formatting. Example: 00:01:53 instead of 0:1:53.