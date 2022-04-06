import random
import sys
import pygame as pg
from pygame.locals import *
from enemies import EzEnemy, LineEnemy, HardEnemy, SuperEnemy
from classes import Circle, Portal, WinCircle, Walls, Stars, Points
walls_pic = pg.image.load("walls.jpg")
walls_pic = pg.transform.scale(walls_pic, (30, 30))
color_blue = (0, 0, 255)
color_red = (255, 0, 0)
color_green = (0, 255, 0)
color_yellow = (255, 255, 0)
color_pink = (255, 150, 150)
color_white = (255, 255, 255)


class Sstars:
    def __init__(self, data):
        self.data = data

    def copy(self, other):
        self.data = []
        for star in other.data:
            self.data.append(Stars(0, 0))
            self.data[-1].copy(star)


class Level:
    def __init__(self, enemies=0, walls=0, circle=Circle(0, 0, color_red), portals=0, win_circle=0, stars=Sstars([]), points=0):
        self.enemies = enemies
        self.walls = walls
        self.circle = circle
        self.portals = portals
        self.win_circle = win_circle
        self.stars = stars
        self.points = points

    def add_points(self, points):
        self.points = points

    def copy(self, other):

        self.enemies = other.enemies
        self.walls = other.walls
        self.circle.copy(other.circle)
        self.portals = other.portals
        self.win_circle = other.win_circle
        self.stars.copy(other.stars)
        self.points = other.points




data_1 = [[1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 2, 1, 0, 1, 1, 0, 0, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 1, 0, 0, 1],
        [1, 1, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
enemies_1 = []
portals_1 = []
stars_1 = []
walls_1 = Walls(data_1, walls_pic)
win_circle_1 = WinCircle(260, 260, color_green)
enemies_1.append(SuperEnemy(color_red, 195, 105))
circle_1 = Circle(45, 75, color_white)
enemies_1.append(LineEnemy(color_red, 90, 45))
enemies_1.append(LineEnemy(color_red, 105, 105))
enemies_1.append(HardEnemy(color_red, 265, 265))
portals_1.append(Portal(45, 220, color_yellow, 165, 195))
stars_1.append(Stars(45, 45))
stars_1 = Sstars(stars_1)
level_1 = Level(enemies_1, walls_1, circle_1, portals_1, win_circle_1, stars_1, 0)



data_2 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [0, 0, 0, 0, 1, 1, 0, 1, 1, 1],
         [1, 0, 1, 0, 1, 1, 0, 0, 1, 1],
         [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
         [1, 0, 0, 0, 1, 1, 1, 0, 1, 1],
         [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
         [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
enemies_2 = []
portals_2 = []
walls_2 = Walls(data_2, walls_pic)
win_circle_2 = WinCircle(160, 255, color_green)
enemies_2.append(SuperEnemy(color_red, 75, 255))
enemies_2.append(EzEnemy(color_red, 45, 255))
circle_2 = Circle(15, 45, color_white)
enemies_2.append(LineEnemy(color_red, 255, 105))
enemies_2.append(HardEnemy(color_red, 175, 105))
level_2 = Level(enemies_2, walls_2, circle_2, portals_2, win_circle_2, stars_1, 0)

