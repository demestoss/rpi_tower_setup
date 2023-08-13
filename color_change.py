import board
import time
import neopixel
import schedule
import subprocess as sp
from temp_config import Temperature
from types import SimpleNamespace

TICK_TIME=8

# State based on Temperature
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

# Mode settings
modeDict = { "Default": 0, "Simple": 1 }
Mode = SimpleNamespace(**modeDict)
current_mode = { "value": Mode.Default }

def set_simple_mode():
    current_mode["value"] = Mode.Simple

def set_default_mode():
    current_mode["value"] = Mode.Default

# Scheduler to change mode

schedule.every().day.at("00:00").do(set_simple_mode)
schedule.every().day.at("08:00").do(set_default_mode)

# Init NeoPixel
# https://rapidtables.com/web/color/RGB_Color.html

np = neopixel.NeoPixel(board.D18, 4)

def normal_color():
    np[0] = (0, 0, 204)
    np[1] = (0, 0, 255)
    np[2] = (102, 0, 204)
    np[3] = (127, 0, 255)

def normal_color_simple():
    np[0] = (0, 0, 204)
    np[1] = (0, 0, 0)
    np[2] = (0, 0, 0)
    np[3] = (0, 0, 0)

def warning_color():
    np[0] = (255, 128, 0)
    np[1] = (255, 153, 51)
    np[2] = (255, 255, 0)
    np[3] = (255, 255, 51)

def warning_color_simple():
    np[0] = (0, 0, 0)
    np[1] = (0, 0, 0)
    np[2] = (255, 255, 0)
    np[3] = (0, 0, 0)

def hardcore_color():
    np[0] = (255, 0, 0)
    np[1] = (255, 51, 51)
    np[2] = (255, 0, 127)
    np[3] = (255, 51, 153)

def hardcore_color_simple():
    np[0] = (255, 0, 0)
    np[1] = (0, 0, 0)
    np[2] = (0, 0, 0)
    np[3] = (0, 0, 0)

def nightmare_color():
    np[0] = (255, 0, 0)
    np[1] = (255, 0, 0)
    np[2] = (204, 0, 0)
    np[3] = (204, 0, 0)

def change_color_simple(state):
    if state == State.Normal:
        normal_color_simple() 
    elif state == State.Medium:
        warning_color_simple() 
    elif state == State.High:
        hardcore_color_simple() 
    elif state == State.Nightmare:
        nightmare_color()

def change_color(state):
    if state == State.Normal:
        normal_color() 
    elif state == State.Medium:
        warning_color() 
    elif state == State.High:
        hardcore_color() 
    elif state == State.Nightmare:
        nightmare_color()

def change_color_by_mode(state, mode):
    if mode == Mode.Default:
        change_color(state)
    else:
        change_color_simple(state)

try:
    prev_state = -1
    prev_mode = current_mode["value"]
    while True:
        schedule.run_pending()
        temp = sp.getoutput("vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'")
        state = calc_state(temp)
        if (state != prev_state or prev_mode != current_mode["value"]):
            change_color_by_mode(state, current_mode["value"])
        prev_state = state
        prev_mode = current_mode["value"]
        time.sleep(TICK_TIME)

except KeyboardInterrupt:
    pass
np.fill((0,0,0))
