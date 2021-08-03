import cv2
import numpy as np

# Dark brown in BGR : [68 87 105]
# Dark brown in HSV : [144 56 11] in percentage
# Dark brown in HSV : [144 142 28] in values

# light brown in BGR : [118 150 182]
# light brown in HSV : [142 56 41] in percentage
# light brown in HSV : [142 142 104] in values

# Magic values for the rock
HSV_MIN_THRESH = np.array([14, 80, 100])
HSV_MAX_THRESH = np.array([16, 100, 200])

HSV_MIN_THRESH_SUB = np.array([16, 0, 0])
HSV_MAX_THRESH_SUB = np.array([16, 255, 255])


def _remove_all_from_bin_image(bin_image, nb_components, stats, w, h):
    """Sets everything but the rock to 0 in binary image"""
    for i in range(nb_components):
        if stats[i][2] < w//15:
            for y in range(stats[i][1], stats[i][1]+stats[i][3]+1):
                for x in range(stats[i][0], stats[i][0]+stats[i][2]+1):
                    if y >= 0 and x >= 0 and y < h and x < w:
                        bin_image[y][x] = 0


def draw_contours(image, hsv_image, color=(255, 0, 150)):
    """Draws contours of the rock found in image"""
    # Remove last value because we don't need the channels
    h, w = image.shape[:-1]

    # Create the mask with the treshold values on the hsv image and not BGR
    bin_image = cv2.inRange(hsv_image, HSV_MIN_THRESH, HSV_MAX_THRESH)
    bin_image2 = cv2.inRange(hsv_image, HSV_MIN_THRESH_SUB, HSV_MAX_THRESH_SUB)

    # Get the locations of the the rock then remove rest pixels
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(
        bin_image, 8, cv2.CV_32S)
    _remove_all_from_bin_image(bin_image, nb_components, stats, w, h)

    dilated_bin_image = cv2.dilate(
        bin_image, np.ones((3, 3), np.uint8), iterations=0)
    dilated_bin_image2 = cv2.dilate(
        bin_image2, np.ones((3, 3), np.uint8), iterations=0)

    result = cv2.bitwise_and(image, image, mask=dilated_bin_image)
    result2 = cv2.bitwise_and(image, image, mask=dilated_bin_image2)

    result2 = cv2.bitwise_not(result2)
    result = cv2.bitwise_and(result, result2)

    contours, hierarchy = cv2.findContours(
        dilated_bin_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, contours, -1, color, 3)

    return result


def get_bin(image, hsv_image, color=(255, 0, 150)):
    """Get binary of the rock found in image"""
    # Remove last value because we don't need the channels
    h, w = image.shape[:-1]
    
    # Create the mask with the treshold values on the hsv image and not BGR
    bin_image = cv2.inRange(hsv_image, HSV_MIN_THRESH, HSV_MAX_THRESH)
    bin_image2 = cv2.inRange(hsv_image, HSV_MIN_THRESH_SUB, HSV_MAX_THRESH_SUB)

    # Get the locations of the the rock then remove rest pixels
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(
        bin_image, 8, cv2.CV_32S)
    _remove_all_from_bin_image(bin_image, nb_components, stats, w, h)

    dilated_bin_image = cv2.dilate(
        bin_image, np.ones((3, 3), np.uint8), iterations=0)
    dilated_bin_image2 = cv2.dilate(
        bin_image2, np.ones((3, 3), np.uint8), iterations=0)

    result = cv2.bitwise_and(image, image, mask=dilated_bin_image)
    result2 = cv2.bitwise_and(image, image, mask=dilated_bin_image2)

    result2 = cv2.bitwise_not(result2)
    result = cv2.bitwise_and(result, result2)

    return result
