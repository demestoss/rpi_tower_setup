import RPi.GPIO as GPIO
import time
import subprocess as sp
from temp_config import Temperature

Fan = 8
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Fan, GPIO.OUT)

p = GPIO.PWM(Fan, 50)
p.start(0)

try:
    while True:
        temp = sp.getoutput("vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'")
    # print(temp)
        if float(temp) < Temperature.Normal:
            p.ChangeDutyCycle(0)
        elif float(temp) >= Temperature.Normal and float(temp) < Temperature.Medium:
            p.ChangeDutyCycle(100)
            time.sleep(0.1)
        elif float(temp) >= Temperature.Medium and float(temp) < Temperature.High:
            p.ChangeDutyCycle(100)
        elif float(time) >= Temperature.High:
            p.ChanngeDutyCycle(100)
            time.sleep(0.1)
        time.sleep(4)

except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()
