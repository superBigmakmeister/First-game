import random
import sys
import pygame as pg
from pygame.locals import *
from math import sin, cos, pi
#font = pg.font.Font(None, 10)

color_blue = (0, 0, 255)
color_red = (255, 0, 0)
color_green = (0, 255, 0)
color_yellow = (255, 255, 0)
color_pink = (255, 150, 150)
color_white = (255, 255, 255)


class Circle:
    def __init__(self, x, y, color):
        self.left = True
        self.right = True
        self.down = True
        self.up = True
        self.x = x
        self.y = y
        self.color = color

    def draw(self, surface):
        pg.draw.circle(surface, self.color, (self.x, self.y), 3, 2)

    def coll_wall(self, walls):
        self.left = True
        self.right = True
        self.down = True
        self.up = True
        for i in range(10):
            for j in range(10):
                if walls.data[i][j] == 1:
                    left_side = j * 30
                    right_side = j * 30 + 30
                    up_side = i * 30
                    down_side = i * 30 + 30
                    if right_side == self.x and (down_side > self.y > up_side or (i != 9 and walls.data[i + 1][j] == 1
                                                                                  and down_side == self.y)):
                        self.left = False
                    if left_side == self.x and (down_side > self.y > up_side or (i != 9 and walls.data[i + 1][j] == 1
                                                                                  and down_side == self.y)):
                        self.right = False
                    if down_side == self.y and (left_side < self.x < right_side or (j != 9 and walls.data[i][j + 1] == 1
                                                                                    and right_side == self.x)):
                        self.up = False
                    if up_side == self.y and (left_side < self.x < right_side or (j != 9 and walls.data[i][j + 1] == 1
                                                                                    and right_side == self.x)):
                        self.down = False

    def move(self, walls):
        pressed_keys = pg.key.get_pressed()
        self.coll_wall(walls)
        if pressed_keys[K_LEFT] and self.x != 0 and self.left:
            self.x -= 5
        elif pressed_keys[K_RIGHT] and self.x != 300 and self.right:
            self.x += 5
        elif pressed_keys[K_UP] and self.y != 0 and self.up:
            self.y -= 5
        elif pressed_keys[K_DOWN] and self.y != 300 and self.down:
            self.y += 5


    def coll_portal(self, portal):
        if self.x == portal.x and self.y == portal.y:
            self.x = portal.to_x
            self.y = portal.to_y + 5
        if self.x == portal.to_x and self.y == portal.to_y:
            self.x = portal.x
            self.y = portal.y + 5

    def to_center(self):
        self.x = 45
        self.y = 75

    def win(self, win_cir):
        return self.x == win_cir.x and self.y == win_cir.y

    def lose(self, enemies):
        lose = False
        for enemy in enemies:
            lose = (lose or (self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2 < 10 ** 2)
        return lose

    def collect(self, stars, points):
        for star in stars.data:
            if not star.collected and abs(self.x - star.x) <= 5 and abs(self.y - star.y) <= 5:
                star.collected = True
                points.p += 10000

    def copy(self, other):

        self.left = True
        self.right = True
        self.down = True
        self.up = True
        self.x = other.x
        self.y = other.y
        self.color = other.color




class Portal:
    def __init__(self, x, y, color, to_x=45, to_y=45):
        self.x = x
        self.y = y
        self.color = color
        self.to_x = to_x
        self.to_y = to_y

    def draw(self, surface):
        pg.draw.circle(surface, self.color, (self.x, self.y), 10, 5)
        pg.draw.circle(surface, self.color, (self.to_x, self.to_y), 10, 5)


class WinCircle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, surface):
        pg.draw.circle(surface, self.color, (self.x, self.y), 10, 5)


class Lifes:
    def __init__(self, color):
        self.color = color
        self.lifes = [(255, 10), (270, 10), (285, 10)]

    def draw(self, surface):
        for life in self.lifes:
            pg.draw.circle(surface, self.color, (life[0], life[1]), 5, 5)

    def death(self):
        self.lifes = self.lifes[:-1]


class Walls:
    def __init__(self, data, walls_pic):
        self.data = data
        self.walls_pic = walls_pic

    def draw(self, surface):
        for i in range(10):
            for j in range(10):
                if self.data[i][j] == 1:
                    # pg.draw.rect(surface, self.color, (j * 30, i * 30, 30, 30))
                    surface.blit(self.walls_pic, self.walls_pic.get_rect(center=(j * 30 + 15, i * 30 + 15)))


class Stars:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False

    def draw(self, surface):
        if not self.collected:
            pg.draw.polygon(surface, color_yellow, [(self.x + 2, self.y), (self.x + round(cos(36 * 2 * pi / 360) * 5), self.y + round(sin(36 * 2 * pi / 360) * 5)),
                            (self.x + round(cos(72 * 2 * pi / 360) * 2), self.y + round(sin(72 * 2 * pi / 360) * 2)),
                            (self.x + round(cos(108 * 2 * pi / 360) * 5), self.y + round(sin(108 * 2 * pi / 360) * 5)),
                            (self.x + round(cos(144 * 2 * pi / 360) * 2), self.y + round(sin(144 * 2 * pi / 360) * 2)),
                            (self.x + round(cos(180 * 2 * pi / 360) * 5), self.y + round(sin(180 * 2 * pi / 360) * 5)),
                            (self.x + round(cos(216 * 2 * pi / 360) * 2), self.y + round(sin(216 * 2 * pi / 360) * 2)),
                            (self.x + round(cos(252 * 2 * pi / 360) * 5), self.y + round(sin(252 * 2 * pi / 360) * 5)),
                            (self.x + round(cos(288 * 2 * pi / 360) * 2), self.y + round(sin(288 * 2 * pi / 360) * 2)),
                            (self.x + round(cos(324 * 2 * pi / 360) * 5), self.y + round(sin(324 * 2 * pi / 360) * 5))])

    def copy(self, other):

        self.x = other.x
        self.y = other.y
        self.collected = False

class Points:
    def __init__(self, font):
        self.p = 0
        self.font = font


    def draw(self, surface):
        text = self.font.render(str(self.p), True, color_white)
        text_x = 240 + 60 // 2 - text.get_rect().width // 2
        surface.blit(text, (text_x, 20))
