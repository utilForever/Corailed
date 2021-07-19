import cv2
import time

from capture import window
from game import map

import functions

ESC_KEY = 27
FRAME_RATE = 10
SLEEP_TIME = 1 / FRAME_RATE

capture = window.WindowCapture("Unrailed!", FRAME_RATE)

# Create map
game_map = map.Map(20, 36, 22, 16, 10)
game_map.init_matrix()

while True:
    game_map.draw_matrix()
    im = game_map.draw_image()
    cv2.imshow("Unrailed! Game Map", im)

    game_map.init_matrix()

    start = time.time()

    frame = capture.screenshot()
    im2 = functions.cut(frame)

    functions.test(im2, game_map)

    functions.draw(im2)
    functions.grid(im2) 

    cv2.imshow("Unrailed! Clone", im2)

    delta = time.time() - start
    if delta < SLEEP_TIME:
        time.sleep(SLEEP_TIME - delta)

    key = cv2.waitKey(1) & 0xFF
    if key == ESC_KEY:
        break
