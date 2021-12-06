import cv2
import numpy as np

# Dark yellow in BGR : [33 148 163]
# Dark yellow in HSV : [54 80 64] in percentage
# Dark yellow in HSV : [54 200 163] in values

# Light yellow in BGR : [52 235 255]
# Light yellow in HSV : [54 80 100] in percentage
# Light yellow in HSV : [54 200 255] in values
"""
HSV_MIN_THRESH = np.array([24, 190, 150])
HSV_MAX_THRESH = np.array([31, 210, 255])
"""

# Dark red in BGR : [35 48 161]
# Dark red in HSV : [6 78 63] in percentage
# Dark red in HSV : [6 199 160] in values

# Light red in BGR : [56 76 255]
# Light red in HSV : [6 78 100] in percentage
# Light red in HSV : [6 199 255] in values
"""
HSV_MIN_THRESH = np.array([0, 190, 140])
HSV_MAX_THRESH = np.array([10, 210, 255])
"""

# Dark blue in BGR : [95 115 49]
# Dark blue in HSV : [162 57 45] in percentage
# Dark blue in HSV : [162 145 114] in values
"""
HSV_MIN_THRESH = np.array([0, 190, 140])
HSV_MAX_THRESH = np.array([10, 210, 255])
"""

# Magic values for the player
'''
HSV_MIN_THRESH = np.array([1, 180, 150])
HSV_MAX_THRESH = np.array([5, 220, 255])
'''

#new values for orange dinosaur
'''
HSV_MAX_THRESH = np.array([38,255,255])
HSV_MIN_THRESH = np.array([13, 219, 163])
'''

#new values for red hair player
HSV_MIN_THRESH = np.array([161,0,0])
HSV_MAX_THRESH = np.array([177,255,255])
def draw_contours(image, hsv_image, color=(0, 100, 255)):
    """Draws contours of the player found in image"""
    # Remove last value because we don't need the channels
    h, w = image.shape[:-1]

    # Create the mask with the treshold values on the hsv image and not BGR
    bin_image = cv2.inRange(hsv_image, HSV_MIN_THRESH, HSV_MAX_THRESH)

    # Get the locations of the player then remove rest pixels
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(
        bin_image, 8, cv2.CV_32S)

    dilated_bin_image = cv2.dilate(bin_image,
                                   np.ones((3, 3), np.uint8),
                                   iterations=2)

    result = cv2.bitwise_and(image, image, mask=dilated_bin_image)

    contours, hierarchy = cv2.findContours(dilated_bin_image,
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, contours, -1, color, 3)

    return result


def get_bin(image, hsv_image, color=(0, 100, 255)):
    """Get binary of the player found in image"""
    # Remove last value because we don't need the channels
    h, w = image.shape[:-1]

    # Create the mask with the treshold values on the hsv image and not BGR
    bin_image = cv2.inRange(hsv_image, HSV_MIN_THRESH, HSV_MAX_THRESH)

    # Get the locations of the player then remove rest pixels
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(
        bin_image, 8, cv2.CV_32S)

    dilated_bin_image = cv2.dilate(bin_image, np.ones((3, 3), np.uint8))

    result = cv2.bitwise_and(image, image, mask=dilated_bin_image)

    return result
