import pyautogui
import random
import time

from colorama import Fore

from pathfinding import astar

SPEED = 0.105
TIME_OFF = 0.15
BREAK_TIME = 1.8

LEFT_KEY = 'A'
RIGHT_KEY = 'D'
UP_KEY = 'W'
DOWN_KEY = 'S'

class SimpleAgent():
    def input_key(self, key, delta_time):
        pyautogui.keyDown(key)
        time.sleep(delta_time)
        pyautogui.keyUp(key)
    
    def input_move_key(self, key):
        self.input_key(key, SPEED)
        time.sleep(TIME_OFF)

    def get_path(self, start, obj, game, last):
        map = game.get_binary_matrix()

        if obj == "axe":
            axe = map.get_pos('A')
            print(axe)
            return astar.run(map, start, axe, game, last)
        elif obj == "pickaxe":
            pickaxe = map.get_pos('I')
            print(pickaxe)
            return astar.run(map, start, pickaxe, game, last)
        elif obj == "tree":
            tree = map.get_pos('t')
            print(tree)
            return astar.run(map, start, tree, game, last)
        elif obj == "rock":
            rock = map.get_pos('k')
            print(rock)
            return astar.run(map, start, rock, game, last)
        else:
            raise Exception("get_path: Not a valid object")

    def move(self, obj, game, draw, player_pos, last):
        print("!!!")
        movement, last = self.get_path(player_pos, obj, game, last)

        if movement is not None:
            for vect in movement:
                delta_height = player_pos[0] - vect[0]
                delta_width = player_pos[1] - vect[1]
                player_pos = vect

                if delta_width > 0:
                    self.input_move_key(LEFT_KEY)
                elif delta_width < 0:
                    self.input_move_key(RIGHT_KEY)
                elif delta_height > 0:
                    self.input_move_key(UP_KEY)
                elif delta_height < 0:
                    self.input_move_key(DOWN_KEY)
                else:
                    print(Fore.GREEN + f"> I got a path to {obj}!")
        else:
            print(Fore.RED + "E: Movement is null!")

        return player_pos, last

    def process_input(self, obj, game, player_pos):
        game.matrix[player_pos[0]][player_pos[1]] = 'M'

        if player_pos[0] - 1 > 0 and game.matrix[player_pos[0] - 1][player_pos[1]] == obj:
            self.input_key(UP_KEY, BREAK_TIME)
            return (player_pos[0] - 1, player_pos[1])
        elif player_pos[0] + 1 < len(game.matrix) and game.matrix[player_pos[0] + 1][player_pos[1]] == obj:
            self.input_key(DOWN_KEY, BREAK_TIME)
            return (player_pos[0] + 1, player_pos[1])
        elif player_pos[1] - 1 > 0 and game.matrix[player_pos[0]][player_pos[1] - 1] == obj:
            self.input_key(LEFT_KEY, BREAK_TIME)
            return (player_pos[0], player_pos[1] - 1)
        elif player_pos[1] + 1 < len(game.matrix[0]) and game.matrix[player_pos[0]][player_pos[1] + 1] == obj:
            self.input_key(RIGHT_KEY, BREAK_TIME)
            return (player_pos[0], player_pos[1] + 1)

        print(Fore.RED + f"E: I can't reach {obj}")
        return None

    def rnd(self, r):
        for i in range(r):
            r = random.randrange(0, 4, 1)
            if r == 0:
                self.input_move_key(UP_KEY)
            elif r == 1:
                self.input_move_key(DOWN_KEY)
            elif r == 2:
                self.input_move_key(LEFT_KEY)
            elif r == 3:
                self.input_move_key(RIGHT_KEY)
