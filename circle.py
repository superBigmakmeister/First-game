import sys
import pygame as pg
from pygame.locals import *
pg.init()
font = pg.font.Font(None, 36)
fps = 30
FramePerSec = pg.time.Clock()
DISPLAYSURF = pg.display.set_mode((300, 300))
color_blue = (0, 0, 255)
color_red = (255, 0, 0)
color_green = (0, 255, 0)
color_yellow = (255, 255, 0)
color_pink = (255, 150, 150)
color_white = (255, 255, 255)
pg.display.set_caption('circles')


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
                    if right_side == self.x and down_side >= self.y >= up_side:
                        self.left = False
                    if left_side == self.x and down_side >= self.y >= up_side:
                        self.right = False
                    if down_side == self.y and left_side <= self.x <= right_side:
                        self.up = False
                    if up_side == self.y and left_side <= self.x <= right_side:
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
        if (self.x - portal.x) ** 2 + (self.y - portal.y) ** 2 < 13 ** 2:
            self.color = color_blue
        if self.x == portal.x and self.y == portal.y:
            self.x = portal.to_x
            self.y = portal.to_y
            self.color = color_white

    def to_center(self):
        self.x = 150
        self.y = 150

    def win(self, win_cir):
        return self.x == win_cir.x and self.y == win_cir.y

    def lose(self, enemy):
        return (self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2 < 10 ** 2




class Enemy:
    def __init__(self, color):
        self.color = color
        self.x = 200
        self.y = 0
        self.dest = 1

    def draw(self, surface):
        pg.draw.circle(surface, self.color, (self.x, self.y), 16, 2)

    def move(self):
        if self.y == 300:
            self.dest = -1
        elif self.y == 0:
            self.dest = 1
        self.y += 5 * self.dest


class Portal:
    def __init__(self, x, y, color, to_x=150, to_y=150):
        self.x = x
        self.y = y
        self.color = color
        self.to_x = to_x
        self.to_y = to_y

    def draw(self, surface):
        pg.draw.circle(surface, self.color, (self.x, self.y), 10, 5)


class WinCircle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, surface):
        pg.draw.circle(surface, self.color, (250, 100), 10, 5)


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
    def __init__(self, data, color):
        self.data = data
        self.color = color

    def draw(self, surface):
        for i in range(10):
            for j in range(10):
                if self.data[i][j] == 1:
                    pg.draw.rect(surface, self.color, (j * 30, i * 30, 30, 30))




data = [[1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]]
portals = []
lifes = Lifes(color_red)
walls = Walls(data, color_pink)
w = WinCircle(250, 100, color_red)
c = Circle(150, 150, color_white)
e = Enemy(color_green)

portals.append(Portal(200, 200, color_white))
portals.append(Portal(100, 200, color_yellow))
game_over = False
win_game = False

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
    if pg.key.get_pressed()[K_SPACE] and win_game:
        win_game = False
        c.to_center()
    DISPLAYSURF.fill((0, 0, 0))
    if not game_over and not win_game:
        walls.draw(DISPLAYSURF)
        c.move(walls)
        e.move()
        e.draw(DISPLAYSURF)
        lifes.draw(DISPLAYSURF)
        for portal in portals:
            portal.draw(DISPLAYSURF)
            c.coll_portal(portal)
        c.draw(DISPLAYSURF)
        w.draw(DISPLAYSURF)
        win_game = c.win(w)
        if c.lose(e):
            lifes.death()
            c.to_center()
            game_over = (len(lifes.lifes) == 0)
    elif game_over:
        text = font.render('GAME OVER ', True, color_red)
        text_rect = text.get_rect()
        text_x = 150 - text_rect.width // 2
        text_y = 150 - text_rect.height // 2
        DISPLAYSURF.blit(text, (text_x, text_y))
    else:
        text = font.render('YOU WIN ', True, color_blue)
        text_rect = text.get_rect()
        text_x = 150 - text_rect.width // 2
        text_y = 150 - text_rect.height // 2
        DISPLAYSURF.blit(text, (text_x, text_y))

    pg.display.update()
    FramePerSec.tick(fps)
