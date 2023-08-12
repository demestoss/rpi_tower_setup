import board
import neopixel
import time
from random import randint

pixels = neopixel.NeoPixel(board.D18, 4)

pixels[0] = (0, 0, 255)
pixels[1] = (51, 51, 255)
pixels[2] = (127, 0, 255)
pixels[3] = (153, 51, 255)
#pixels[4] = (0, 0, 0)

#pixels.fill((0,0,0)
#try:
 #   while True:
  #      for i in range(0, 255):
   #         pixels[1] = (randint(0,i), randint(i,255), randint(i,255))
    #        pixels[2] = (randint(0,i), randint(i,255), randint(0,i))
     #       pixels[3] = (randint(i,255), randint(0,i), randint(i,255))
      #      time.sleep(0.02)
       #     #pixels[4] = (0,0,0)
#
#except KeyboardInterrupt:
  #  pass
#pixels.fill((0,0,0))
