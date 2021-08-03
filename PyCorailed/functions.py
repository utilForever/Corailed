import cv2
import numpy as np

from detection import axe, pickaxe, tree, player, rock, black_rock, river, footpath, empty_space


def recognize_objects(im, game_map):
    """Recognize objects in the game"""
    im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    # Get binary from image
    bin_player = player.get_bin(im, im_hsv)
    bin_tree = tree.get_bin(im, im_hsv)
    bin_rock = rock.get_bin(im, im_hsv)
    bin_black_rock = black_rock.get_bin(im, im_hsv)
    bin_river = river.get_bin(im, im_hsv)
    bin_footpath = footpath.get_bin(im, im_hsv)
    bin_empty_space = empty_space.get_bin(im, im_hsv)

    # Get object from binary
    arr_player = get_object(game_map, bin_player, bin_player, 3)
    arr_tree = get_object(game_map, bin_tree, bin_tree, 3)
    arr_rock = get_object(game_map, bin_rock, bin_rock, 5)
    arr_black_rock = get_object(game_map, bin_black_rock, bin_black_rock, 3)
    arr_river = get_object(game_map, bin_river, bin_river, 3)
    arr_footpath = get_object(game_map, bin_footpath, bin_footpath, 3)
    arr_empty_space = get_object(game_map, bin_empty_space, bin_empty_space, 6)

    # Get the position of axe and pickaxe
    axe_pos = axe.get_axe_minimap(im, cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
    pickaxe_pos = pickaxe.get_pickaxe_minimap(
        im, cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))

    # Unpack array to unique letter
    unpack_array(arr_player, 'P', game_map, (0, -1))
    unpack_array(arr_tree, 'T', game_map)
    unpack_array(arr_rock, 'K', game_map)
    unpack_array(arr_black_rock, 'B', game_map)
    unpack_array(arr_river, 'R', game_map)
    unpack_array(arr_footpath, 'M', game_map)
    unpack_array(arr_empty_space, '0', game_map)

    if axe_pos != None:
        for i in range(len(axe_pos)):
            axe_pos[i] = (axe_pos[i][0] // 22, axe_pos[i][1] // 16)
            unpack_array(axe_pos, 'A', game_map, (0, -1))

    if pickaxe_pos != None:
        for i in range(len(pickaxe_pos)):
            pickaxe_pos[i] = (pickaxe_pos[i][0] // 22, pickaxe_pos[i][1] // 16)
            unpack_array(pickaxe_pos, 'I', game_map, (0, -1))

    # Add extra empty space to game map
    for i in range(2):
        for j in range(20):
            game_map.add_matrix(i, j, '0')

    for i in range(20):
        game_map.add_matrix(35, i, '0')


def get_object(game, bin, im, nb):
    """Get object from the image using the color in pixel"""
    result = []

    for x in range(22, 810, 22):
        for y in range(0, 320, 16):
            # Get the color from some pixels
            arr0 = get_pixel_color(bin, x - 10, y)
            arr1 = get_pixel_color(bin, x - 5, y)
            arr2 = get_pixel_color(bin, x + 0, y)

            arr3 = get_pixel_color(bin, x - 10, y + 12)
            arr4 = get_pixel_color(bin, x - 5, y + 12)
            arr5 = get_pixel_color(bin, x + 0, y + 12)

            arr6 = get_pixel_color(bin, x - 10, y + 7)
            arr7 = get_pixel_color(bin, x - 5, y + 7)
            arr8 = get_pixel_color(bin, x + 0, y + 7)

            arr = [arr0, arr1, arr2, arr3, arr4, arr5, arr6, arr7, arr8]
            num_color_pixel = 0

            for i in range(len(arr)):
                num_color_pixel += (arr[i][0] != 0 and arr[i]
                                    [1] != 0 and arr[i][2] != 0)

            # If the number of pixel that contains the color \
            # greater than or equal to threshold, append to result
            if num_color_pixel >= nb:
                result.append([x // 22 - 1, y // 16])

    return result


def unpack_array(arr, vall, game, offset=(0, 0)):
    for elem in arr:
        # Check boundary
        if elem[0] - offset[0] > 0 and elem[0] - offset[0] < len(game.matrix[0]) and \
            elem[1] - offset[1] > 0 and elem[1] - offset[1] < len(game.matrix):
            game.add_matrix(elem[0] - offset[0], elem[1] - offset[1], vall)


def draw_object_contours(im):
    """Draw contours of the object"""
    im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    # Draw object contours
    player.draw_contours(im, im_hsv)
    axe.draw_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
    pickaxe.draw_contours(im, cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
    tree.draw_contours(im, im_hsv)
    rock.draw_contours(im, im_hsv)
    black_rock.draw_contours(im, im_hsv)
    river.draw_contours(im, im_hsv)
    footpath.draw_contours(im, im_hsv)
    empty_space.draw_contours(im, im_hsv)


def draw_grid(im):
    """Draw grid to the image"""
    # Draw a line along the x-axis
    for x in range(5, 900, 22):
        for y in range(0, 400):
            im = set_pixel_color(im, x, y, (100, 0, 100))

    # Draw a line along the y-axis
    for y in range(0, 400, 16):
        for x in range(0, 900):
            im = set_pixel_color(im, x, y, (100, 0, 100))


def cut_image(im):
    """Cut the image"""
    im = rotate(im, -8)
    x, y = 0, 125
    h, w = 320, 800
    im = im[y:y + h, x:x + w]

    rows, cols = im.shape[:-1]

    a, b, c = [382, 52], [500, 50], [400, 200]
    offsetx = 20
    d, e, f = [382 + offsetx, 52], [500 + offsetx, 50], [400, 200]

    pts1 = np.float32([a, b, c])
    pts2 = np.float32([d, e, f])

    dst = im

    M = cv2.getAffineTransform(pts1, pts2)
    dst = cv2.warpAffine(im, M, (cols, rows))

    return dst


def rotate(im, angle):
    """Rotate the image"""
    image_center = tuple(np.array(im.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(
        im, rot_mat, im.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def get_pixel_color(im, x, y):
    """Get the pixel color"""
    rows, cols = im.shape[:-1]

    if x < 0 and y < 0:
        raise Exception("get_pixel_color: Coordinates need to be positive!")
    if x < cols and y < rows:
        return im[y, x]

    raise Exception("get_pixel_color: x and y out of range!")


def set_pixel_color(im, x, y, color):
    """Set the pixel color"""
    rows, cols = im.shape[:-1]

    if x < 0 and y < 0:
        raise Exception("set_pixel_color: Coordinates need to be positive!")
    if x < cols and y < rows:
        im[y, x] = color
        return im

    return im
