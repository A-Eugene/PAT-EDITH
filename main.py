# boot.py -- run on boot-up
"""

  This is the main file that is executed on startup by the Raspberry PI.
  The folder "src" is used as a package, then this script runs src/main.py
  by importing it, so ./src/main.py can run on startup while that and other 
  scripts remain organized in ./src instead of floating all over the root
  folder.

  Edit src/main.py instead of this file.
  
"""

import sys

sys.path.append('src')

from src import App