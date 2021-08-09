from threading import Thread

import time
import keyboard


class Printer:
    def __init__(self, updateHZ):
        self._thread_name = "Capture"
        self.wait_time = 1 / updateHZ
        self.should_stop = False
        self.last_key_press = ''

    def start(self):
        self._thread = Thread(target=self.update,
                              name=self._thread_name, args=())
        self._thread.daemon = True
        self._thread.start()

        return self

    def update(self):
        while not self.should_stop:
            start = time.time()

            if keyboard.is_pressed('F1'):
                self.last_key_press = 'F1'

            if keyboard.is_pressed('F2'):
                self.last_key_press = 'F2'

            if keyboard.is_pressed('P'):
                self.last_key_press = 'P'

            if keyboard.is_pressed('K'):
                self.last_key_press = 'K'

            if keyboard.is_pressed('C'):
                self.last_key_press = 'C'

            if keyboard.is_pressed('O'):
                self.last_key_press = 'O'

            if keyboard.is_pressed('L'):
                self.last_key_press = 'L'

            delta = time.time() - start
            if delta < self.wait_time:
                time.sleep(self.wait_time - delta)

    def key(self):
        the_key = self.last_key_press
        self.last_key_press = ''
        return the_key
