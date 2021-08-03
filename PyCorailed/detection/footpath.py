import cv2
import numpy as np

# Magic values for the footpath
HSV_MIN_THRESH_GRASS = np.array([40, 110, 80])
HSV_MAX_THRESH_GRASS = np.array([73, 176, 255])

HSV_MIN_THRESH_EMPTY_TREE = np.array([0, 50, 50])
HSV_MAX_THRESH_EMPTY_TREE = np.array([10, 255, 255])

HSV_MIN_THRESH_BRIDGE = np.array([16, 130, 100])
HSV_MAX_THRESH_BRIDGE = np.array([16, 140, 150])

HSV_MIN_THRESH_EMPTY_ROCK = np.array([16, 0, 0])
HSV_MAX_THRESH_EMPTY_ROCK = np.array([16, 255, 255])


def _remove_all_from_bin_image(bin_image, nb_components, stats, w, h):
    """Sets everything but the footpath to 0 in binary image"""
    for i in range(nb_components):
        if stats[i][2] < w // 50:
            for y in range(stats[i][1], stats[i][1] + stats[i][3] + 1):
                for x in range(stats[i][0], stats[i][0] + stats[i][2] + 1):
                    if y >= 0 and x >= 0 and y < h and x < w:
                        bin_image[y][x] = 0


def draw_contours(image, hsv_image, color=(255, 255, 255)):
    """Draws contours of the footpath found in image"""
    # Remove last value because we don't need the channels
    h, w = image.shape[:-1]

    # Create the bin_image with the treshold values on the hsv image and not BGR
    bin_image = cv2.inRange(
        hsv_image, HSV_MIN_THRESH_GRASS, HSV_MAX_THRESH_GRASS)
    bin_image += cv2.inRange(hsv_image,
                             HSV_MIN_THRESH_EMPTY_TREE, HSV_MAX_THRESH_EMPTY_TREE)
    bin_image += cv2.inRange(hsv_image,
                             HSV_MIN_THRESH_BRIDGE, HSV_MAX_THRESH_BRIDGE)
    bin_image += cv2.inRange(hsv_image,
                             HSV_MIN_THRESH_EMPTY_ROCK, HSV_MAX_THRESH_EMPTY_ROCK)

    # Get the locations of the footpath then remove rest pixels
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(
        bin_image, 8, cv2.CV_32S)
    _remove_all_from_bin_image(bin_image, nb_components, stats, w, h)

    dilated_bin_image = cv2.dilate(bin_image,
                                   np.ones((3, 3), np.uint8),
                                   iterations=2)

    result = cv2.bitwise_and(image, image, mask=dilated_bin_image)

    contours, hierarchy = cv2.findContours(dilated_bin_image,
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, contours, -1, color, 3)

    return result


def get_bin(image, hsv_image, color=(255, 255, 255)):
    """Get binary of the footpath found in image"""
    # Remove last value because we don't need the channels
    h, w = image.shape[:-1]

    # Create the bin_image with the treshold values on the hsv image and not BGR
    bin_image = cv2.inRange(
        hsv_image, HSV_MIN_THRESH_GRASS, HSV_MAX_THRESH_GRASS)
    bin_image += cv2.inRange(hsv_image,
                             HSV_MIN_THRESH_EMPTY_TREE, HSV_MAX_THRESH_EMPTY_TREE)
    bin_image += cv2.inRange(hsv_image,
                             HSV_MIN_THRESH_BRIDGE, HSV_MAX_THRESH_BRIDGE)
    bin_image += cv2.inRange(hsv_image,
                             HSV_MIN_THRESH_EMPTY_ROCK, HSV_MAX_THRESH_EMPTY_ROCK)

    # Get the locations of the footpath then remove rest pixels
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(
        bin_image, 8, cv2.CV_32S)
    _remove_all_from_bin_image(bin_image, nb_components, stats, w, h)

    dilated_bin_image = cv2.dilate(bin_image, np.ones((3, 3), np.uint8))

    result = cv2.bitwise_and(image, image, mask=dilated_bin_image)

    return result
