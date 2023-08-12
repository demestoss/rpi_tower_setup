import board
import time
import neopixel
import subprocess as sp
from temp_config import Temperature
from types import SimpleNamespace

stateDict = { "Normal": 0, "Medium": 1, "High": 2, "Nightmare": 3 }
State = SimpleNamespace(**stateDict)

def calc_state(temp):
    v = float(temp)
    if v < Temperature.Normal:
        return State.Normal
    elif v >= Temperature.Normal and v < Temperature.Medium:
        return State.Medium
    elif v >= Temperature.Medium and v < Temperature.High:
        return State.High
    elif v >= Temperature.High:
        return State.Nightmare

np = neopixel.NeoPixel(board.D18, 4)

# https://rapidtables.com/web/color/RGB_Color.html

def normal_mode():
    np[0] = (0, 0, 204)
    np[1] = (0, 0, 255)
    np[2] = (102, 0, 204)
    np[3] = (127, 0, 255)

def warning_mode():
    np[0] = (255, 128, 0)
    np[1] = (255, 153, 51)
    np[2] = (255, 255, 0)
    np[3] = (255, 255, 51)

def hardcore_mode():
    np[0] = (255, 0, 0)
    np[1] = (255, 51, 51)
    np[2] = (255, 0, 127)
    np[3] = (255, 51, 153)

def nightmare_mode():
    np[0] = (255, 0, 0)
    np[1] = (255, 0, 0)
    np[2] = (204, 0, 0)
    np[3] = (204, 0, 0)

def change_color(state):
    if state == State.Normal:
        normal_mode() 
    elif state == State.Medium:
        warning_mode() 
    elif state == State.High:
        hardcore_mode() 
    elif state == State.Nightmare:
        nightmare_mode()

try:
    prev_state = -1
    while True:
        temp = sp.getoutput("vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'")
        state = calc_state(temp)
        if (state != prev_state):
            change_color(state)
        prev_state = state
        time.sleep(8)

except KeyboardInterrupt:
    pass
np.fill((0,0,0))
