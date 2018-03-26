#!/usr/bin/env python
# -*- coding: Utf-8 -*
# Created by: https://openclassrooms.com/courses/interface-graphique-pygame-pour-python/tp-dk-labyrinthe
# Modified by: aurelien.esnard@u-bordeaux.fr

from __future__ import print_function
import pygame
import sys
import random

### python version ###
print("python version: {}.{}.{}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2]))
print("pygame version: ", pygame.version.ver)

### Game Parameters ###

sprite_size = 30 # 30x30 pixels
win_title = "What a Maze!"
win_icon = "images/dk/right.png"
img_bg = "images/misc/bg1.png"
img_wall = "images/misc/wall.png"
img_bomb = "images/misc/bomb.png"
img_banana = "images/misc/banana.png"
img_dk_right = "images/dk/right.png"
img_dk_left = "images/dk/left.png"
img_dk_up = "images/dk/up.png"
img_dk_down = "images/dk/down.png"
img_zelda_right = "images/zelda/right.png"
img_zelda_left = "images/zelda/left.png"
img_zelda_up = "images/zelda/up.png"
img_zelda_down = "images/zelda/down.png"
map_file = "map1"
FPS = 30
yellow = (255, 255, 0)
blue = (0,0,255)

### class Map ###

class Map:
    def __init__(self, filename):
        self.filename = filename
        self.array = []
        self.width = 0
        self.height = 0
        self.wall = pygame.image.load(img_wall).convert()
        # self.bg = [ pygame.image.load(img).convert() for img in img_bg ]
        self.bg = pygame.image.load(img_bg).convert()

    def load(self):
        with open(self.filename, "r") as filename:
            _array = []
            for row in filename:
                _row = []
                for square in row:
                    if square != '\n':
                        _row.append(square)
                _array.append(_row)
            self.array = _array
            self.height = len(self.array)
            self.width = len(self.array[0])
            print("load map \"{}\" of size {}x{}".format(self.filename, self.width, self.height))

    def grid(self, win):
        # horizontal lines
        for y in range(0,self.height):
            pygame.draw.line(win, blue, (0, y*sprite_size), (self.width*sprite_size, y*sprite_size), 1)
        # vertical lines
        for x in range(0,self.width):
            pygame.draw.line(win, blue, (x*sprite_size, 0), (x*sprite_size,self.height*sprite_size), 1)

    def render(self, win):
        # win.blit(self.background, (0, 0))
        for y in range(0,self.height):
            for x in range(0,self.width):
                square = self.array[y][x]
                x0 = x*sprite_size
                y0 = y*sprite_size
                if square == 'w':
                    win.blit(self.wall, (x0, y0)) # wall
                elif square == '0':
                    win.blit(self.bg, (x0, y0)) # background

    def debug(self):
        for row in self.array:
            for square in row:
                print(square, end='')
            print()

    def random_square(self, m):
        offset = random.randint(0, self.width*self.height-1)
        while offset > 0:
            for y in range(0, self.height-1):
                for x in range(0, self.width-1):
                    if self.array[y][x] == '0':
                        offset -= 1
                    if offset == 0: break
                if offset == 0: break
        return (x,y)

### class Banana ###

class Banana:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.img = pygame.image.load(img_banana).convert_alpha()
        print("generate random banana at position ({},{})".format(pos_x,pos_y))

    def render(self, win):
        x = self.pos_x * sprite_size
        y = self.pos_y * sprite_size
        win.blit(self.img, (x, y))

### class Bomb ###

class Bomb:
    def __init__(self, pos_x, pos_y, bomb_range=5, time_to_explode=5000):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.bomb_range = bomb_range
        self.time_to_explode = time_to_explode
        self.img = pygame.image.load(img_bomb).convert_alpha()
        self.font = pygame.font.SysFont('Consolas', 20)

    def update(self, dt):
        # subtract the passed time `dt` from the timer each frame.
        if self.time_to_explode > 0:
            self.time_to_explode -= dt

    def explode(self, win):
        # print("boom!")
        x = self.pos_x * sprite_size
        y = self.pos_y * sprite_size
        x0 = x + sprite_size/2
        y0 = y + sprite_size/2
        thick = 2
        pygame.draw.line(win, yellow, (x0,y0-thick/2), (x0+sprite_size/2+(sprite_size*self.bomb_range),y0-thick/2), thick) # horizontal right
        pygame.draw.line(win, yellow, (x0,y0-thick/2), (x0-sprite_size/2-(sprite_size*self.bomb_range),y0-thick/2), thick) # horizontal left
        pygame.draw.line(win, yellow, (x0-thick/2,y0), (x0-thick/2,y0+sprite_size/2+(sprite_size*self.bomb_range)), thick) # vertical down
        pygame.draw.line(win, yellow, (x0-thick/2,y0), (x0-thick/2,y0-sprite_size/2-(sprite_size*self.bomb_range)), thick) # vertical up

    def render(self, win):
        x = self.pos_x * sprite_size
        y = self.pos_y * sprite_size
        win.blit(self.img, (x, y))
        if(self.time_to_explode >= 0):
            x0 = x + sprite_size/2
            y0 = y + sprite_size/2
            count = int(self.time_to_explode / 1000) + 1
            text = self.font.render(str(count), True, yellow)
            rect = text.get_rect(center=(x0,y0))
            win.blit(text, rect)
        if(self.time_to_explode <= 0):
            self.explode(win)

### class Character ###

class Character:
    def __init__(self, img_right, img_left, img_up, img_down, nickname, pos_x, pos_y):
        self.score = 0
        self.nickname = nickname
        self.img_right = pygame.image.load(img_right).convert_alpha()
        self.img_left = pygame.image.load(img_left).convert_alpha()
        self.img_up = pygame.image.load(img_up).convert_alpha()
        self.img_down = pygame.image.load(img_down).convert_alpha()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direction = self.img_right

    def move(self, m, direction):
        x = self.pos_x * sprite_size
        y = self.pos_y * sprite_size
        # move right
        if direction == 'right':
            if self.pos_x < (m.width - 1):  # check board limit
                if m.array[self.pos_y][self.pos_x + 1] != 'w':  # check wall
                    self.pos_x += 1
                    x = self.pos_x * sprite_size
            self.direction = self.img_right
        # move left
        elif direction == 'left':
            if self.pos_x > 0:  # check board limit
                if m.array[self.pos_y][self.pos_x - 1] != 'w':  # check wall
                    self.pos_x -= 1
                    x = self.pos_x * sprite_size
            self.direction = self.img_left
        # move up
        elif direction == 'up':
            if self.pos_y > 0:  # check board limit
                if m.array[self.pos_y - 1][self.pos_x] != 'w':  # check wall
                    self.pos_y -= 1
                    y = self.pos_y * sprite_size
            self.direction = self.img_up
        # move down
        elif direction == 'down':
            if self.pos_y < (m.height - 1):  # check board limit
                if m.array[self.pos_y + 1][self.pos_x] != 'w':  # check wall
                    self.pos_y += 1
                    y = self.pos_y * sprite_size
            self.direction = self.img_down

    def render(self, win):
        x = self.pos_x * sprite_size
        y = self.pos_y * sprite_size
        win.blit(self.direction, (x, y))

### Main Program ###

# args
if len(sys.argv) == 2:
    map_file = sys.argv[1]

# initialization
pygame.init()
win = pygame.display.set_mode((100,100)) # TODO: improve this dummy size
m = Map(map_file)
m.load()
win = pygame.display.set_mode((m.width*sprite_size, m.height*sprite_size))
icon = pygame.image.load(win_icon)
pygame.display.set_icon(icon)
pygame.display.set_caption(win_title)
clock = pygame.time.Clock()
dk = Character(img_dk_right, img_dk_left, img_dk_up, img_dk_down, "dk", 0, 0)
zelda = Character(img_zelda_right, img_zelda_left, img_zelda_up, img_zelda_down, "zelda", 0, 1)
characters = [zelda, dk]
current = dk
bombs = []
bananas = [ Banana(2,1), Banana(1,3) ]

# main loop
cont = 1
while cont:
    # make sure game doesn't run at more than FPS frames per second
    dt = clock.tick(FPS)

    # process all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cont = 0
            elif event.key == pygame.K_d:
                m.debug()
            elif event.key == pygame.K_TAB:
                if current == dk: current = zelda
                else: current = dk
            elif event.key == pygame.K_SPACE:
                bombs.append(Bomb(current.pos_x, current.pos_y))
            elif event.key == pygame.K_RIGHT:
                current.move(m, 'right')
            elif event.key == pygame.K_LEFT:
                current.move(m, 'left')
            elif event.key == pygame.K_UP:
                current.move(m, 'up')
            elif event.key == pygame.K_DOWN:
                current.move(m, 'down')

    # update
    for bomb in bombs: bomb.update(dt)

    # eat banana
    # if m.array[current.pos_y][current.pos_x] == 'b':
    #     m.array[current.pos_y][current.pos_x] = '0'
    #     current.score += 10
    #     print("{}\'s score: {}".format(current.nickname, current.score))

    # render
    m.render(win)
    m.grid(win)
    for bomb in bombs: bomb.render(win)
    for banana in bananas: banana.render(win)
    for character in characters: character.render(win)
    pygame.display.flip()

    # remove items
    # ...

# the end
pygame.quit()
