import cv2
import time

from colorama import Fore

from agent import simple_agent
from capture import window
from game import map

import functions
import printer

ESC_KEY = 27
FRAME_RATE = 10
SLEEP_TIME = 1 / FRAME_RATE

run = True
mode = "tree"

# Initialize the window
capture = window.WindowCapture("Unrailed!", FRAME_RATE)

# Initialize printer
prn = printer.Printer(40)

# Initialize agent
agent = simple_agent.SimpleAgent()

# Print information
print(Fore.WHITE +
      f"""> Corailed Project with Jeonbuk Science High School!
    F1: Quit
    F2: Pause Bot  
    C: Change Mode
    K: Positive Confirmation
    L: Negative Confirmation
    P: Randomize movements
    O: Emergency drop Item
    """)

# Create map
game_map = map.Map(20, 36, 22, 16, 10)
game_map.init_matrix()

# Pick the axe and move out of the train station
agent.input_key('space', 0.1)
time.sleep(0.3)
agent.input_key('s', 0.5)

# Start printer thread
prn.start()

# Variables for the main loop
tried = 0
change = False
random = False

# Last object
last = []
for i in range(15):
    last.append((0, 0))

while True:
    key = prn.key()

    if key == 'F1':
        print(
            Fore.WHITE +
            "> Corailed Project with Jeonbuk Science High School!")
        break
    elif key == 'F2':
        if run:
            print(Fore.YELLOW + "> I'M WAITING!")
            run = False
        else:
            print(Fore.YELLOW + "> I'M STARTING!")
            run = True
    elif key == 'C':
        print(Fore.MAGENTA + "> I'M CHANGING TARGET")
        change = True
    elif key == 'K':
        change = False
        print(Fore.GREEN + "> Thanks for the confirmation")
        agent.input_key("space", 0.3)

        if mode == "tree":
            mode = "rock"
        else:
            mode = "tree"

        tried = 0
    elif key == 'O':
        change = False
        print(Fore.RED + "> EMERGENCY DROP")
        agent.input_key("space", 0.3)
        print(Fore.RED + "> WAITING FOR YOUR CALL")
        run = False
    elif key == 'L':
        change = False
        tried = 0

        if mode == "tree":
            print(Fore.BLUE + "> I'M SORRY, BACK TO CHOPPING")
        else:
            print(Fore.BLUE + "> I'M SORRY, BACK TO MINING")
    elif key == 'P':
        random = True
        change = False

        print(Fore.YELLOW + "> WANT SOME RANDOM ? :)")

    if run:
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
        if tried != -1:
            tried, last = functions.test(im2, agent, game_map, last, mode, change,
                                         tried, random)

        random = False

        if tried >= 15:
            change = False
            if mode == "tree":
                print("> I'M SORRY, BACK TO CHOPPING")
            else:
                print("> I'M SORRY, BACK TO MINING")
            tried = 0        

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
    else:
        time.sleep(1)
