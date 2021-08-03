import cv2
import numpy as np

template = cv2.imread("template_axe.png", cv2.IMREAD_GRAYSCALE)
height, width = template.shape


def get_axe_location(image_gray):
    """Apply template matching to gray image and return axe location"""
    result = cv2.matchTemplate(image_gray, template, cv2.TM_CCOEFF_NORMED)

    location = np.where(result >= 0.85)
    return location


def draw_contours(image, image_gray, color=(150, 100, 200)):
    """Draws contours of the axe found in image"""
    try:
        for point in zip(*get_axe_location(image_gray)[::-1]):
            # Get the location of the axe, invert the list, draw each points
            cv2.rectangle(image, (point[0] - 2, point[1] - 2),
                          (point[0] + width + 2, point[1] + height + 2), color, 2)
    except:
        print("draw_contours: Could not find the axe")


def get_axe_minimap(image, image_gray):
    """Get the posiion of the axe found in image"""
    result = []

    try:
        for point in zip(*get_axe_location(image_gray)[::-1]):
            # Get the location of the axe, invert the list, draw each points
            result.append((point[0] + width // 2, point[1] + height // 2))
        return result
    except:
        print("get_axe_minimap: Could not find the axe")
