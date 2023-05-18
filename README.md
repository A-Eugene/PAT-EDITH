# Raspberry PI Pico W Smart Glasses
A device used as a proof of concept for future developed AR glasses which combines the vision from reality and augmented reality.

![Raspberry PI Pico W GPIO Mapping](https://i0.wp.com/peppe8o.com/wp-content/uploads/2023/03/raspberry-pi-pico-pinout.jpg?resize=910%2C607&ssl=1)

## GPIO Mapping
| Port   | Description |
| ----------- | ----------- |
| GP1      | SCL      |
| GP2   | SDA     |

## Build Log
- **18 May 2023**
  - Initialized the project using Pico-W-Go 2.18 VScode Extension (later versions seems to have problem initializing vREPL terminal to Pico)
  - Initialized the project to github
  - Added ./main.py which adds ./src folder as a package and runs ./src/main.py by importing it on startup, so ./src/main.py can run on startup while that and other scripts remain organized in ./src instead of floating all over the root folder.