import numpy as np
from sys import platform

if platform == "win32":
    import cv2
    import win32gui
    import pyautogui
elif platform == "darwin":
    import Quartz.CoreGraphics as CG


class WindowCapture:
    def __init__(self, window_name, capture_rate):
        self.window_name = window_name
        self.wait_time = 1 / capture_rate

    def take_screenshot(self):
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
            windows = CG.CGWindowListCopyWindowInfo(
                CG.kCGWindowListOptionAll, CG.kCGNullWindowID)
            found = False

            for window in windows:
                if window.get('kCGWindowName', u'Unknown') == self.window_name:
                    found = True
                    unrailed_window = window
                    break

            if not found:
                raise Exception('Window not found: ' + self.window_name)

            # TODO: How get titlebar height or content rect?
            image = CG.CGWindowListCreateImage(
                CG.CGRectNull,
                CG.CG.kCGWindowListOptionIncludingWindow,
                unrailed_window['kCGWindowNumber'],
                CG.kCGWindowImageBoundsIgnoreFraming | CG.kCGWindowImageBestResolution)

            width = CG.CGImageGetWidth(image)
            height = CG.CGImageGetHeight(image)
            bytes_per_row = CG.CGImageGetBytesPerRow(image)

            pixel_data = CG.CGDataProviderCopyData(
                CG.CGImageGetDataProvider(image))
            image = np.frombuffer(pixel_data, dtype=np.uint8)
            image = image.reshape((height, bytes_per_row // 4, 4))
            image = image[:, :width, :]

            return image
