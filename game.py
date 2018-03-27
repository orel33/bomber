#!/usr/bin/env python3
# -*- coding: Utf-8 -*
# Created by: https://openclassrooms.com/courses/interface-graphique-pygame-pour-python/tp-dk-labyrinthe
# Modified by: aurelien.esnard@u-bordeaux.fr

# from __future__ import print_function # to use print() in Python 2.x
import pygame
import sys
import random

### python version ###
print("python version: {}.{}.{}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2]))
print("pygame version: ", pygame.version.ver)

### Game Constants ###

FPS = 30
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

### Game Parameters ###

sprite_size = 30 # 30x30 pixels
win_title = "What a Maze!"
win_icon = "images/dk/right.png"
img_bg = "images/misc/bg1.png"
img_wall = "images/misc/wall.png"
img_bomb = "images/misc/bomb2.png"
img_banana = "images/misc/banana.png"
imgs_dk = [ "images/dk/left.png", "images/dk/right.png", "images/dk/up.png", "images/dk/down.png" ]
imgs_zelda = [ "images/zelda/left.png", "images/zelda/right.png", "images/zelda/up.png", "images/zelda/down.png" ]
map_file = "map1"
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

    # def debug(self):
    #     for row in self.array:
    #         for square in row:
    #             print(square, end='')
    #         print()

    def random(self):
        offset = random.randint(1, self.width*self.height)
        while offset > 0:
            for y in range(0, self.height):
                for x in range(0, self.width):
                    if self.array[y][x] == '0':
                        offset -= 1
                    if offset == 0: break
                if offset == 0: break
        return (x,y)

### class Banana ###

class Banana:
    def __init__(self, m, pos_x, pos_y):
        self.map = m
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.img = pygame.image.load(img_banana).convert_alpha()
        print("set banana at position ({},{})".format(pos_x,pos_y))

    def render(self, win):
        x = self.pos_x * sprite_size
        y = self.pos_y * sprite_size
        win.blit(self.img, (x, y))

### class Bomb ###

class Bomb:
    def __init__(self, m, pos_x, pos_y, max_range=5, countdown=5):
        self.map = m
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.max_range = max_range
        self.countdown = countdown
        self.time_to_explode = countdown * 1000 # in ms
        self.img = pygame.image.load(img_bomb).convert_alpha()
        self.font = pygame.font.SysFont('Consolas', 20)
        # build bomb range
        for xmax in range(self.pos_x, self.pos_x+self.max_range+1):
            if xmax >= m.width or self.map.array[self.pos_y][xmax] != '0': break
        for ymax in range(self.pos_y, self.pos_y+self.max_range+1):
            if ymax >= m.height or self.map.array[ymax][self.pos_x] != '0': break
        for xmin in range(self.pos_x, self.pos_x-self.max_range-1, -1):
            if xmin < 0 or self.map.array[self.pos_y][xmin] != '0': break
        for ymin in range(self.pos_y, self.pos_y-self.max_range-1, -1):
            if ymin < 0 or self.map.array[ymin][self.pos_x] != '0': break
        self.range = [xmin+1, xmax-1, ymin+1, ymax-1]
        print("set bomb at position ({},{}) with range {}".format(pos_x,pos_y, self.range))

    def update(self, dt):
        if self.time_to_explode > 0:
            self.time_to_explode -= dt # subtract the passed time `dt` from the timer each frame
            self.countdown = int(self.time_to_explode / 1000) + 1
        else:
            self.countdown = 0

    def explode(self, win):
        x = self.pos_x * sprite_size
        y = self.pos_y * sprite_size
        x0 = x + sprite_size/2
        y0 = y + sprite_size/2
        thick = 2
        pygame.draw.line(win, yellow, (sprite_size*self.range[LEFT],y0-thick/2), (sprite_size*(self.range[RIGHT]+1),y0-thick/2), thick) # horizontal line
        pygame.draw.line(win, yellow, (x0-thick/2, sprite_size*self.range[UP]), (x0-thick/2,sprite_size*(self.range[DOWN]+1)), thick) # vertical line

    def render(self, win):
        x = self.pos_x * sprite_size
        y = self.pos_y * sprite_size
        if(self.countdown == 1):
            self.explode(win)
        if(self.countdown > 0):
            win.blit(self.img, (x, y))
            x0 = x + sprite_size/2
            y0 = y + sprite_size/2
            text = self.font.render(str(self.countdown), True, yellow)
            rect = text.get_rect(center=(x0-5,y0+5))
            win.blit(text, rect)

### class Character ###

class Character:
    def __init__(self, nickname, m, imgs, pos_x, pos_y):
        self.map = m
        self.life = 50
        self.nickname = nickname
        self.imgs = [ pygame.image.load(img).convert_alpha() for img in imgs ]
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direction = RIGHT

    def move(self, direction):
        # move right
        if direction == RIGHT:
            if self.pos_x < (m.width - 1):  # check board limit
                if self.map.array[self.pos_y][self.pos_x + 1] != 'w':  # check wall
                    self.pos_x += 1
            self.direction = RIGHT
        # move left
        elif direction == LEFT:
            if self.pos_x > 0:  # check board limit
                if self.map.array[self.pos_y][self.pos_x - 1] != 'w':  # check wall
                    self.pos_x -= 1
            self.direction = LEFT
        # move up
        elif direction == UP:
            if self.pos_y > 0:  # check board limit
                if self.map.array[self.pos_y - 1][self.pos_x] != 'w':  # check wall
                    self.pos_y -= 1
            self.direction = UP
        # move down
        elif direction == DOWN:
            if self.pos_y < (m.height - 1):  # check board limit
                if self.map.array[self.pos_y + 1][self.pos_x] != 'w':  # check wall
                    self.pos_y += 1
            self.direction = DOWN

    def eat(self, banana):
        if banana.pos_x == self.pos_x and banana.pos_y == self.pos_y:
            self.life += 10
            print("{}\'s life: {}".format(self.nickname, self.life))
            return True
        return False

    def explosion(self, bomb):
        horizontal = (self.pos_y == bomb.pos_y and self.pos_x >= bomb.range[LEFT] and self.pos_x <= bomb.range[RIGHT])
        vertical = (self.pos_x == bomb.pos_x and self.pos_y >= bomb.range[UP] and self.pos_y <= bomb.range[DOWN])
        if bomb.countdown == 1 and ( horizontal or vertical ):
            print("{}\'s life: {}".format(self.nickname, self.life))
            self.life -= 10
        if self.life <= 0:
            return True
        return False

    def render(self, win):
        x = self.pos_x * sprite_size
        y = self.pos_y * sprite_size
        win.blit(self.imgs[self.direction], (x, y))

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
dk = Character("dk", m, imgs_dk, 0, 0)
zelda = Character("zelda", m, imgs_zelda, 0, 1)
characters = [zelda, dk]
current = dk
bananas = [ Banana(m, *m.random()) for _ in range(10) ] # 10 bananas
bombs = []

# main loop
pygame.key.set_repeat(1,200) # repeat keydown events every 200ms
cont = 1
while cont:
    # make sure game doesn't run at more than x frames per second
    dt = clock.tick(FPS)

    # process all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cont = 0
            elif event.key == pygame.K_w:
                m.array[current.pos_y][current.pos_x] = 'w'
            elif event.key == pygame.K_b:
                m.array[current.pos_y][current.pos_x] = '0'
            elif event.key == pygame.K_TAB:
                if current == dk: current = zelda
                else: current = dk
            elif event.key == pygame.K_SPACE:
                bombs.append(Bomb(m, current.pos_x, current.pos_y))
            elif event.key == pygame.K_RIGHT:
                current.move(RIGHT)
            elif event.key == pygame.K_LEFT:
                current.move(LEFT)
            elif event.key == pygame.K_UP:
                current.move(UP)
            elif event.key == pygame.K_DOWN:
                current.move(DOWN)

    # update all
    for bomb in bombs:
        bomb.update(dt)
        if bomb.countdown == 0: bombs.remove(bomb)

    for character in characters:
        for bomb in bombs:
            if bomb.countdown == 1 and character.explosion(bomb):
                print("game over!")
                cont = 0
                break
        for banana in bananas:
            if character.eat(banana): bananas.remove(banana)

    # render all
    m.render(win)
    # m.grid(win)
    for bomb in bombs: bomb.render(win)
    for banana in bananas: banana.render(win)
    for character in characters: character.render(win)
    pygame.display.flip()

# the end
pygame.quit()
