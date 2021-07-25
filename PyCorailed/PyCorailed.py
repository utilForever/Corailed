import cv2
import time

from capture import window
from game import map

import functions

ESC_KEY = 27
FRAME_RATE = 10
SLEEP_TIME = 1 / FRAME_RATE

# Initialize the window
capture = window.WindowCapture("Unrailed!", FRAME_RATE)

# Create map
game_map = map.Map(20, 36, 22, 16, 10)
game_map.init_matrix()

while True:
    # Draw matrix and image of game map
    game_map.draw_matrix()
    im = game_map.draw_image()

    # Show game map
    cv2.imshow("Unrailed! Game Map", im)

    # Initialize matrix
    game_map.init_matrix()

    start = time.time()

    # Take screenshot from window and cut it
    frame = capture.take_screenshot()
    im2 = functions.cut_image(frame)

    # Recognize objects on the image
    functions.recognize_objects(im2, game_map)

    # Draw contours of objects and grid
    functions.draw_object_contours(im2)
    functions.draw_grid(im2)

    # Show game clone
    cv2.imshow("Unrailed! Clone", im2)

    # Wait for ESC key
    delta = time.time() - start
    if delta < SLEEP_TIME:
        time.sleep(SLEEP_TIME - delta)

    # Process key events
    key = cv2.waitKey(1) & 0xFF
    if key == ESC_KEY:
        break
