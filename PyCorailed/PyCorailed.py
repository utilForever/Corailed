import cv2
import time

from capture import window

ESC_KEY = 27
FRAME_RATE = 10
SLEEP_TIME = 1 / FRAME_RATE

capture = window.WindowCapture("Unrailed!", FRAME_RATE)

while True:
    start = time.time()

    frame = capture.screenshot()
    cv2.imshow("Unrailed! Clone", frame)

    delta = time.time() - start
    if delta < SLEEP_TIME:
        time.sleep(SLEEP_TIME - delta)

    key = cv2.waitKey(1) & 0xFF
    if key == ESC_KEY:
        break
