import random
import sys
import pygame as pg
from pygame.locals import *
from levels import level_1, level_2, Level
from classes import Points
from enemies import EzEnemy, LineEnemy, HardEnemy, SuperEnemy
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



class Button:
    def __init__(self, color, x, y, width, height, text, font):
        self.color = color
        self.x = x
        self.y = y
        self.font = font
        self.width = width
        self.height = height
        text = font.render(text, True, color_red)
        self.text = text
        self.text_rect = text.get_rect()
        self.text_x = self.x + self.width // 2 - self.text_rect.width // 2
        self.text_y = self.y + self.height // 2 - self.text_rect.height // 2


    def draw(self, surface):
        pg.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        pg.draw.rect(DISPLAYSURF, color_white, (self.text_x, self.text_y, self.text_rect.width, self.text_rect.height), 2)
        DISPLAYSURF.blit(self.text, (self.text_x, self.text_y))

    def touch(self, x, y):
        if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
            return True
        else:
            return False


class Lifes:
    def __init__(self, color):
        self.color = color
        self.lifes = [(255, 10), (270, 10), (285, 10)]

    def draw(self, surface):
        for life in self.lifes:
            pg.draw.circle(surface, self.color, (life[0], life[1]), 5, 5)

    def death(self):
        self.lifes = self.lifes[:-1]



b_2 = Button(color_white, 100, 100, 100, 50, 'LVL 2', font)
b_1 = Button(color_white, 100, 25, 100, 50, 'LVL 1', font)
exit = Button(color_white, 100, 175, 100, 50, "EXIT", font)
menu = Button(color_white, 100, 175, 100, 50, "MENU", font)
records = Button(color_white, 90, 250, 125, 50, "RECORDS", font)
points = Points(pg.font.Font(None, 15))
game_started = 0
game_over = False
win_game = False
records_show = False
lvl = 0
tr = 0
while True:
    mouse_pos = [-1, -1]
    for event in pg.event.get():
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
        if event.type == QUIT:
            pg.quit()
            sys.exit()
    DISPLAYSURF.fill((0, 0, 0))
    if not game_started:
        exit.draw(DISPLAYSURF)
        b_1.draw(DISPLAYSURF)
        b_2.draw(DISPLAYSURF)
        records.draw(DISPLAYSURF)
        if exit.touch(mouse_pos[0], mouse_pos[1]):
            pg.quit()
            sys.exit()
        if b_1.touch(mouse_pos[0], mouse_pos[1]):
            lifes = Lifes(color_red)
            level = Level()
            level.copy(level_1)
            points = Points(pg.font.Font(None, 15))
            level.add_points(points)mk
            lvl = 1
            game_started = True
        if b_2.touch(mouse_pos[0], mouse_pos[1]):
            level = Level()
            lifes = Lifes(color_red)
            lvl = 2
            level.copy(level_2)
            points = Points(pg.font.Font(None, 15))
            level.add_points(points)
            game_started = True
        if records.touch(mouse_pos[0], mouse_pos[1]):
            records_show = True
            game_started = True
    elif records_show:
        f_records = open("records.txt")
        i = 0
        for line in f_records:
            recs = list(line.split())
            for r in recs:
                text = font.render(str(r), True, color_red)
                text_rect = text.get_rect()
                text_x = 150 - text_rect.width // 2
                text_y = 30 * (i + 1) - text_rect.height // 2
                DISPLAYSURF.blit(text, (text_x, text_y))
                i += 1
        f_records.close()

    elif not game_over and not win_game:
        level.walls.draw(DISPLAYSURF)
        level.circle.move(level.walls)
        level.circle.collect(level.stars, level.points)
        for enemy in level.enemies:
            enemy.move(level.walls)
        for enemy in level.enemies:
            enemy.draw(DISPLAYSURF)
        lifes.draw(DISPLAYSURF)
        level.points.draw(DISPLAYSURF)
        for star in level.stars.data:
            star.draw(DISPLAYSURF)
        for portal in level.portals:
            portal.draw(DISPLAYSURF)
            level.circle.coll_portal(portal)
        level.circle.draw(DISPLAYSURF)
        level.win_circle.draw(DISPLAYSURF)
        win_game = level.circle.win(level.win_circle)
        if win_game:
            f_records = open("records.txt")
            i = 0
            x = []
            level.circle.to_center()
            for line in f_records:
                x.append(list(map(int, line.split())))
            s_1 = x[0]
            s_2 = x[1]
            f_records.close()
            f_records = open("records.txt", "w")
            if lvl == 1:
                s_1.append(level.points.p)
                s_1.sort(reverse=True)
            if lvl == 2:
                s_2.append(level.points.p)
                s_2.sort(reverse=True)
            s_1 = [str(i) for i in s_1]
            s_2 = [str(i) for i in s_2]
            s_1 = s_1[:3]
            s_2 = s_2[:3]
            s_1 = " ".join(s_1)
            s_2 = " ".join(s_2)
            f_records.write(s_1 + "\n" + s_2)
            f_records.close()
        if level.circle.lose(level.enemies):
            lifes.death()
            level.circle.to_center()
            game_over = (len(lifes.lifes) == 0)
    elif game_over:
        menu.draw(DISPLAYSURF)
        text = font.render('GAME OVER ', True, color_red)
        text_rect = text.get_rect()
        text_x = 150 - text_rect.width // 2
        text_y = 150 - text_rect.height // 2
        DISPLAYSURF.blit(text, (text_x, text_y))
        if menu.touch(mouse_pos[0], mouse_pos[1]):
            game_started = False
            game_over = False
    else:
        menu.draw(DISPLAYSURF)
        text = font.render('YOU WIN ', True, color_blue)
        text_rect = text.get_rect()
        text_x = 150 - text_rect.width // 2
        text_y = 150 - text_rect.height // 2
        DISPLAYSURF.blit(text, (text_x, text_y))
        if menu.touch(mouse_pos[0], mouse_pos[1]):
            game_started = False
            win_game = False

    pg.display.update()
    FramePerSec.tick(fps)
