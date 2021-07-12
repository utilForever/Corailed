import cv2
import numpy as np
import pyautogui
from sys import platform

if platform == "win32":
    import win32gui
elif platform == "darwin":
    from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionAll


class WindowCapture:
    def __init__(self, window_name, capture_rate):
        self.window_name = window_name
        self.wait_time = 1 / capture_rate

    def screenshot(self):
        if platform == "win32":
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
        elif platform == "darwin":
            return cv2.cvtColor(np.asarray(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
