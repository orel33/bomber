#!/usr/bin/env python3
# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

import pygame
import sys
import random

### python version ###
print("python version: {}.{}.{}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2]))
print("pygame version: ", pygame.version.ver)

### Constants ###

FPS = 30
HEALTH = 50
MAX_RANGE = 5
COUNTDOWN = 5
IMMUNITY = 1500 # in ms
DISARMED = 2000 # in ms
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
X = 0
Y = 1
WALLS = ('w', 'x', 'z')
BACKGROUNDS = ('0', '1', '2')
YELLOW = (255, 255, 0)
BLUE = (0,0,255)
BANANA = 0
CHERRY = 1

### Image Files ###

img_backgrounds = [ "images/misc/bg0.png", "images/misc/bg1.png", "images/misc/bg2.png" ]
img_blank = "images/misc/blank.png"
img_walls = [ "images/misc/wall0.png", "images/misc/wall1.png", "images/misc/wall2.png" ]
img_bomb = "images/misc/bomb.png"
img_fire = "images/misc/fire.png"
img_fruits = [ "images/misc/banana.png", "images/misc/cherry.png" ]
imgs_dk = [ "images/dk/left.png", "images/dk/right.png", "images/dk/up.png", "images/dk/down.png" ]
imgs_zelda = [ "images/zelda/left.png", "images/zelda/right.png", "images/zelda/up.png", "images/zelda/down.png" ]

### Parameters ###

sprite_size = 30 # 30x30 pixels
win_title = "Bomber Man"
win_icon = img_bomb
map_file = "maps/map0"

### Class Map ###

class Map:
    def __init__(self, filename):
        self.filename = filename
        self.array = []
        self.width = 0
        self.height = 0
        self.walls = [ pygame.image.load(img).convert() for img in img_walls ]
        self.backgrounds = [ pygame.image.load(img).convert() for img in img_backgrounds ]
        self.blank = pygame.image.load(img_blank).convert()

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

    def render(self, win):
        # win.blit(self.background, (0, 0))
        for y in range(0,self.height):
            for x in range(0,self.width):
                square = self.array[y][x]
                x0 = x*sprite_size
                y0 = y*sprite_size
                # walls
                if square == 'w':
                    win.blit(self.walls[0], (x0, y0))
                elif square == 'x':
                    win.blit(self.walls[1], (x0, y0))
                elif square == 'z':
                    win.blit(self.walls[2], (x0, y0))
                # backgrounds
                elif square == '0':
                    win.blit(self.backgrounds[0], (x0, y0))
                elif square == '1':
                    win.blit(self.backgrounds[1], (x0, y0))
                elif square == '2':
                    win.blit(self.backgrounds[2], (x0, y0))
                else:
                    win.blit(self.blank, (x0, y0)) # blank


    def random(self):
        offset = random.randint(1, self.width*self.height)
        while offset > 0:
            for y in range(0, self.height):
                for x in range(0, self.width):
                    if self.array[y][x] in BACKGROUNDS:
                        offset -= 1
                    if offset == 0: break
                if offset == 0: break
        return (x,y)

### Class Fruit ###

class Fruit:
    def __init__(self, m, kind, pos):
        self.map = m
        self.pos = pos
        self.imgs = [ pygame.image.load(img).convert_alpha() for img in img_fruits ]
        self.kind = kind
        print("set fruit {} at position ({},{})".format(kind, pos[X],pos[Y]))

    def render(self, win):
        x = self.pos[X] * sprite_size
        y = self.pos[Y] * sprite_size
        win.blit(self.imgs[self.kind], (x, y))

### Class Bomb ###

class Bomb:
    def __init__(self, m, pos):
        self.map = m
        self.pos = pos
        self.max_range = MAX_RANGE
        self.countdown = COUNTDOWN
        self.time_to_explode = (COUNTDOWN+1)*1000-1 # in ms
        self.img_bomb = pygame.image.load(img_bomb).convert_alpha()
        self.img_fire = pygame.image.load(img_fire).convert_alpha()
        self.font = pygame.font.SysFont('Consolas', 20)
        # build bomb range
        for xmax in range(self.pos[X], self.pos[X]+self.max_range+1):
            if xmax >= m.width or self.map.array[self.pos[Y]][xmax] not in BACKGROUNDS: break
        for ymax in range(self.pos[Y], self.pos[Y]+self.max_range+1):
            if ymax >= m.height or self.map.array[ymax][self.pos[X]] not in BACKGROUNDS: break
        for xmin in range(self.pos[X], self.pos[X]-self.max_range-1, -1):
            if xmin < 0 or self.map.array[self.pos[Y]][xmin] not in BACKGROUNDS: break
        for ymin in range(self.pos[Y], self.pos[Y]-self.max_range-1, -1):
            if ymin < 0 or self.map.array[ymin][self.pos[X]] not in BACKGROUNDS: break
        self.range = [xmin+1, xmax-1, ymin+1, ymax-1]
        print("drop bomb at position ({},{})".format(pos[X],pos[Y]))

    def update(self, dt):
        # subtract the passed time `dt` from the timer each frame
        if self.time_to_explode >= 0:
            self.time_to_explode -= dt
            self.countdown = int(self.time_to_explode / 1000)
        else:
            self.countdown = -1

    def explode(self, win):
        x0 = self.pos[X]
        y0 = self.pos[Y]
        for x in range(self.range[LEFT], self.range[RIGHT]+1):
            win.blit(self.img_fire, (x*sprite_size, y0*sprite_size))
        for y in range(self.range[UP], self.range[DOWN]+1):
            win.blit(self.img_fire, (x0*sprite_size, y*sprite_size))

    def draw(self, win):
        x = self.pos[X] * sprite_size
        y = self.pos[Y] * sprite_size
        win.blit(self.img_bomb, (x, y))
        x0 = x + sprite_size/2
        y0 = y + sprite_size/2
        text = self.font.render(str(self.countdown), True, YELLOW)
        rect = text.get_rect(center=(x0-5,y0+5))
        win.blit(text, rect)

    def render(self, win):
        if(self.countdown == 0):
            self.explode(win)
        elif(self.countdown > 0):
            self.draw(win)

### Class Character ###

class Character:
    def __init__(self, nickname, m, imgs, pos):
        self.map = m
        self.health = HEALTH
        self.immunity = 0 # the character gets immunity against bomb during this time (in ms)
        self.disarmed = 0 # the character cannot drop a bomb during this time (in ms)
        self.nickname = nickname
        self.imgs = [ pygame.image.load(img).convert_alpha() for img in imgs ]
        self.pos = pos
        self.direction = RIGHT

    def move(self, direction):
        # move right
        if direction == RIGHT:
            if self.pos[X] < (m.width - 1):
                if self.map.array[self.pos[Y]][self.pos[X] + 1] not in WALLS:
                    self.pos = (self.pos[X]+1, self.pos[Y])
            self.direction = RIGHT
        # move left
        elif direction == LEFT:
            if self.pos[X] > 0:
                if self.map.array[self.pos[Y]][self.pos[X] - 1] not in WALLS:
                    self.pos = (self.pos[X]-1, self.pos[Y])
            self.direction = LEFT
        # move up
        elif direction == UP:
            if self.pos[Y] > 0:
                if self.map.array[self.pos[Y] - 1][self.pos[X]] not in WALLS:
                    self.pos = (self.pos[X], self.pos[Y]-1)
            self.direction = UP
        # move down
        elif direction == DOWN:
            if self.pos[Y] < (m.height - 1):
                if self.map.array[self.pos[Y] + 1][self.pos[X]] not in WALLS:
                    self.pos = (self.pos[X], self.pos[Y]+1)
            self.direction = DOWN

    def eat(self, fruit):
        if fruit.pos[X] == self.pos[X] and fruit.pos[Y] == self.pos[Y]:
            self.health += 10
            print("{}\'s health: {}".format(self.nickname, self.health))
            return True
        return False

    def update(self, dt):
        # subtract the passed time `dt` from the timer each frame
        if self.immunity > 0: self.immunity -= dt
        else: self.immunity = 0
        if self.disarmed > 0: self.disarmed -= dt
        else: self.disarmed = 0

    def explosion(self, bomb):
        if bomb.countdown != 0: return False
        if self.immunity > 0: return False
        horizontal = (self.pos[Y] == bomb.pos[Y] and self.pos[X] >= bomb.range[LEFT] and self.pos[X] <= bomb.range[RIGHT])
        vertical = (self.pos[X] == bomb.pos[X] and self.pos[Y] >= bomb.range[UP] and self.pos[Y] <= bomb.range[DOWN])
        if ( horizontal or vertical ):
            self.health -= 10
            self.immunity = IMMUNITY
            print("{}\'s health: {}".format(self.nickname, self.health))
        if self.health <= 0:
            print("{} is dead!".format(self.nickname))
            return True
        return False

    def render(self, win):
        x = self.pos[X] * sprite_size
        y = self.pos[Y] * sprite_size
        win.blit(self.imgs[self.direction], (x, y))

### Main Program ###

# optional argument
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
dk = Character("dk", m, imgs_dk, m.random() )
zelda = Character("zelda", m, imgs_zelda, m.random())
characters = [zelda, dk]
current = dk
fruits = [ Fruit(m, BANANA, m.random()) for _ in range(5) ]  # 5 bananas
fruits += [ Fruit(m, CHERRY, m.random()) for _ in range(5) ] # 5 cherries
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
            elif event.key == pygame.K_TAB:
                if current == dk: current = zelda
                else: current = dk
            elif event.key == pygame.K_SPACE:
                if current.disarmed == 0:
                    bombs.append(Bomb(m, current.pos))
                    current.disarmed = DISARMED
            elif event.key == pygame.K_RIGHT:
                current.move(RIGHT)
            elif event.key == pygame.K_LEFT:
                current.move(LEFT)
            elif event.key == pygame.K_UP:
                current.move(UP)
            elif event.key == pygame.K_DOWN:
                current.move(DOWN)

    # update bombs (and remove it)
    for bomb in bombs:
        bomb.update(dt)
        if bomb.countdown == -1: bombs.remove(bomb)

    # update characters and eat fruits
    for character in characters:
        character.update(dt)
        for fruit in fruits:
            if character.eat(fruit): fruits.remove(fruit)

    # update characters after bomb explosion
    for bomb in bombs:
        for character in characters:
            if character.explosion(bomb):
                characters.remove(character)

    # render all
    m.render(win)
    for bomb in bombs: bomb.render(win)
    for fruit in fruits: fruit.render(win)
    for character in characters: character.render(win)
    pygame.display.flip()

    # game over
    if not characters:
        print("Game Over!")
        break

# the end
pygame.quit()
