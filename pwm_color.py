import board
import time
import neopixel
import subprocess as sp
from temp_config import Temperature

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

def apocalypce_mode():
    np[0] = (255, 0, 0)
    np[1] = (255, 0, 0)
    np[2] = (204, 0, 0)
    np[3] = (204, 0, 0)

try:
    while True:
        temp = sp.getoutput("vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'")
       # print(temp)
        if float(temp) < Temperature.Normal:
            normal_mode()
        elif float(temp) >= Temperature.Normal and float(temp) < Temperature.Medium:
            warning_mode()
            time.sleep(0.1)
        elif float(temp) >= Temperature.Medium and float(temp) < Temperature.High:
            hardcore_mode()
        elif float(time) >= Temperature.High:
            apocalypce_mode()
            time.sleep(0.1)
        time.sleep(4)

except KeyboardInterrupt:
    pass
np.fill((0,0,0))
