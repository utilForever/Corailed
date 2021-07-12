import cv2
import numpy as np
import win32gui
import pyautogui


class WindowCapture:
    def __init__(self, window_name, capture_rate):
        self.window_name = window_name
        self.wait_time = 1 / capture_rate

    def screenshot(self):
        hwnd = win32gui.FindWindow(None, self.window_name)
        if not hwnd:
            raise Exception('Window not found: ' + self.window_name)

        left, top, right, bot = win32gui.GetClientRect(hwnd)
        x, y = win32gui.ClientToScreen(hwnd, (left, top))

        return cv2.cvtColor(
            np.asarray(
                pyautogui.screenshot(
                    region=(x, y,
                            *win32gui.ClientToScreen(hwnd, (right - x, bot - y))))),
            cv2.COLOR_RGB2BGR)
