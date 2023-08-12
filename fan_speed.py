import RPi.GPIO as GPIO
import time
import subprocess as sp
from temp_config import Temperature
from types import SimpleNamespace

Fan = 8
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Fan, GPIO.OUT)

p = GPIO.PWM(Fan, 50)
p.start(0)

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

def change_fan(state):
    if state == State.Normal:
        p.ChangeDutyCycle(0)
    elif state == State.Medium:
        p.ChangeDutyCycle(100)
        #time.sleep(0.1)
    elif state == State.High:
        p.ChangeDutyCycle(100)
    elif state == State.Nightmare:
        p.ChanngeDutyCycle(100)
        #time.sleep(0.1)

try:
    prev_state = -1
    while True:
        temp = sp.getoutput("vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'")
        state = calc_state(temp)
        if (state != prev_state):
            change_fan(state)
        prev_state = state
        time.sleep(8)

except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()
