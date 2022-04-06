import random
import sys
import pygame as pg
from pygame.locals import *


class EzEnemy:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.dest = 1

    def draw(self, surface):
        pg.draw.circle(surface, self.color, (self.x, self.y), 15, 3)

    def move(self, walls):
        if walls.data[(self.y + 5 * self.dest + 15 * self.dest) // 30][self.x // 30] == 1:
            self.dest *= -1
        self.y += 5 * self.dest


class LineEnemy:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.dest = 1

    def draw(self, surface):
        pg.draw.circle(surface, self.color, (self.x, self.y), 15, 3)

    def move(self, walls):
        if walls.data[self.y // 30][(self.x + 5 * self.dest + 15 * self.dest) // 30] == 1:
            self.dest *= -1
        self.x += 5 * self.dest


class HardEnemy:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.x_dest = 1
        self.y_dest = 0

    def draw(self, surface):
        pg.draw.circle(surface, self.color, (self.x, self.y), 15, 3)

    def move(self, walls):
        self.x_dest = (random.randint(0, 100) % 3) - 1
        if abs(self.x_dest) == 0:
            self.y_dest = (random.randint(0, 100) % 3) - 1
        new_x = (self.x + 5 * self.x_dest + 15 * self.x_dest) // 30
        new_y = (self.y + 5 * self.y_dest + 15 * self.y_dest) // 30
        if abs(self.x_dest) == 1 and (new_x < 0 or new_x > 9 or walls.data[self.y // 30][new_x] == 1 or walls.data[self.y // 30][new_x] == 2):
            self.x_dest *= -1
        if abs(self.y_dest) == 1 and (new_y < 0 or new_y > 9 or walls.data[new_y][self.x // 30] == 1 or walls.data[new_y][self.x // 30] == 2):
            self.y_dest *= -1
        self.x += 5 * self.x_dest
        self.y += 5 * self.y_dest


class SuperEnemy:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.x_dest = 1
        self.y_dest = 0

    def draw(self, surface):
        pg.draw.circle(surface, self.color, (self.x, self.y), 15, 3)

    def move(self, walls):
        if self.x % 30 == 15 and self.y % 30 == 15:
            j = self.x // 30
            i = self.y // 30
            move_to = []
            if walls.data[i - 1][j] == 0:
                move_to.append((0, -1))
            if walls.data[i + 1][j] == 0:
                move_to.append((0, 1))
            if walls.data[i][j - 1] == 0:
                move_to.append((-1, 0))
            if walls.data[i][j + 1] == 0:
                move_to.append((1, 0))
            if len(move_to) > 0:
                dest = move_to[random.randint(0, len(move_to) - 1)]
                self.x_dest = dest[0]
                self.y_dest = dest[1]
        self.x += 3 * self.x_dest
        self.y += 3 * self.y_dest
