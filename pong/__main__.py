import os
import sys
from pong import Pong

# if getattr(sys, 'frozen', False):
#     os.chdir(sys._MEIPASS)

if __name__ == "__main__":
    application = Pong()
    while True:
        application.application_state.loop()