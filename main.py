import sys
import pygame as pg
from pygame.locals import *
pg.init()
fps = 30
FramePerSec = pg.time.Clock()
DISPLAYSURF = pg.display.set_mode((300, 300))
color_blue = (0, 0, 255)
color_red = (255, 0, 0)
color_green = (0, 255, 0)
color_yellow = (255, 255, 0)
color_white = (255, 255, 255)
pg.display.set_caption('Red_Nose')


class Pupil:
    def __init__(self, coord):
        self.coord = coord

    def draw(self, surface, coord):
        pg.draw.circle(surface, color_white, coord, 3, 2)

    def left(self, surface):
        self.draw(surface, (self.coord[0] - 5, self.coord[1]))

    def right(self, surface):
        self.draw(surface, (self.coord[0] + 5, self.coord[1]))

    def up(self, surface):
        self.draw(surface, (self.coord[0], self.coord[1] - 5))

    def down(self, surface):
        pg.draw.line(surface, color_white, (self.coord[0] - 10, self.coord[1]), (self.coord[0] + 10, self.coord[1]))


p = Pupil((115, 140))
p_2 = Pupil((160, 140))


while True:
    DISPLAYSURF.fill((0, 0, 0))

    pg.draw.circle(DISPLAYSURF, color_blue, (150, 150), 70, 2)
    pg.draw.circle(DISPLAYSURF, color_blue, (115, 140), 10, 2)
    pg.draw.circle(DISPLAYSURF, color_blue, (160, 140), 10, 2)
    pg.draw.line(DISPLAYSURF, color_blue, (125, 140), (150, 140))
    pg.draw.rect(DISPLAYSURF, color_blue, (110, 175, 50, 2))
    pg.draw.polygon(DISPLAYSURF, color_red, [(120, 160), (130, 160), (130, 150)], 2)
    pressed_keys = pg.key.get_pressed()
    if pressed_keys[K_UP]:
        p.up(DISPLAYSURF)
        p_2.up(DISPLAYSURF)
    elif pressed_keys[K_LEFT] and not pressed_keys[K_RIGHT]:
        p.left(DISPLAYSURF)
        p_2.left(DISPLAYSURF)
    elif pressed_keys[K_DOWN]:
        p.down(DISPLAYSURF)
        p_2.down(DISPLAYSURF)
        pg.draw.circle(DISPLAYSURF, color_green, (115, 140), 10, 2)
        pg.draw.circle(DISPLAYSURF, color_green, (160, 140), 10, 2)
        pg.draw.line(DISPLAYSURF, color_green, (125, 140), (150, 140))
    elif pressed_keys[K_RIGHT] and not pressed_keys[K_LEFT]:
        p_2.right(DISPLAYSURF)
        p.right(DISPLAYSURF)
    elif pressed_keys[K_RIGHT] and pressed_keys[K_LEFT]:
        p.draw(DISPLAYSURF, p.coord)
        p_2.draw(DISPLAYSURF, p_2.coord)
    elif not pressed_keys[K_RIGHT] and not pressed_keys[K_LEFT]:
        p.draw(DISPLAYSURF, p.coord)
        p_2.draw(DISPLAYSURF, p_2.coord)

    pg.display.update()


    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
    FramePerSec.tick(fps)
