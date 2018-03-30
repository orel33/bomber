# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

import random

################################################################################
#                                  MODEL                                       #
################################################################################

### Constants ###

HEALTH = 50
MAX_RANGE = 5
COUNTDOWN = 5
IMMUNITY = 1500 # in ms
DISARMED = 2000 # in ms
DIRECTION_LEFT = 0
DIRECTION_RIGHT = 1
DIRECTION_UP = 2
DIRECTION_DOWN = 3
X = 0
Y = 1
WALLS = ('w', 'x', 'z')
BACKGROUNDS = ('0', '1', '2')
DEFAULT_MAP = "maps/map0"
# fruit type
BANANA = 0
CHERRY = 1
FRUITS = [BANANA, CHERRY]
# character type
DK = 0
ZELDA = 1
BATMAN = 2
CHARACTERS = [DK, ZELDA, BATMAN]

### Class Map ###

class Map:
    def __init__(self, filename):
        self.filename = filename
        self.array = []
        # load map file
        with open(self.filename, "r") as _file:
            _array = []
            for row in _file:
                _row = []
                for square in row:
                    if square != '\n':
                        _row.append(square)
                _array.append(_row)
            self.array = _array
            self.height = len(self.array)
            self.width = len(self.array[0])
            print("load map \"{}\" of size {}x{}".format(self.filename, self.width, self.height))

    def random(self):
        while True:
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
            if self.array[y][x] in BACKGROUNDS:
                break
        return (x,y)

### Class Fruit ###

class Fruit:
    def __init__(self, kind, m, pos):
        self.map = m
        self.pos = pos
        self.kind = kind
        print("set fruit {} at position ({},{})".format(kind, pos[X],pos[Y]))

### Class Bomb ###

class Bomb:
    def __init__(self, m, pos):
        self.map = m
        self.pos = pos
        self.max_range = MAX_RANGE
        self.countdown = COUNTDOWN
        self.time_to_explode = (COUNTDOWN+1)*1000-1 # in ms
        # compute bomb range
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

    def tick(self, dt):
        # subtract the passed time `dt` from the timer each frame
        if self.time_to_explode >= 0:
            self.time_to_explode -= dt
            self.countdown = int(self.time_to_explode / 1000)
        else:
            self.countdown = -1

### Class Character ###

class Character:
    def __init__(self, nickname, kind, m, pos):
        self.map = m
        self.kind = kind
        self.health = HEALTH
        self.immunity = 0 # the character gets immunity against bomb during this time (in ms)
        self.disarmed = 0 # the character cannot drop a bomb during this time (in ms)
        self.nickname = nickname
        self.pos = pos
        self.direction = DIRECTION_RIGHT

    def move(self, direction):
        # move right
        if direction == DIRECTION_RIGHT:
            if self.pos[X] < (self.map.width - 1):
                if self.map.array[self.pos[Y]][self.pos[X] + 1] not in WALLS:
                    self.pos = (self.pos[X]+1, self.pos[Y])
            self.direction = DIRECTION_RIGHT
        # move left
        elif direction == DIRECTION_LEFT:
            if self.pos[X] > 0:
                if self.map.array[self.pos[Y]][self.pos[X] - 1] not in WALLS:
                    self.pos = (self.pos[X]-1, self.pos[Y])
            self.direction = DIRECTION_LEFT
        # move up
        elif direction == DIRECTION_UP:
            if self.pos[Y] > 0:
                if self.map.array[self.pos[Y] - 1][self.pos[X]] not in WALLS:
                    self.pos = (self.pos[X], self.pos[Y]-1)
            self.direction = DIRECTION_UP
        # move down
        elif direction == DIRECTION_DOWN:
            if self.pos[Y] < (self.map.height - 1):
                if self.map.array[self.pos[Y] + 1][self.pos[X]] not in WALLS:
                    self.pos = (self.pos[X], self.pos[Y]+1)
            self.direction = DIRECTION_DOWN

    def eat(self, fruit):
        if fruit.pos[X] == self.pos[X] and fruit.pos[Y] == self.pos[Y]:
            self.health += 10
            print("{}\'s health: {}".format(self.nickname, self.health))
            return True
        return False

    def tick(self, dt):
        # subtract the passed time `dt` from the timer each frame
        if self.immunity > 0: self.immunity -= dt
        else: self.immunity = 0
        if self.disarmed > 0: self.disarmed -= dt
        else: self.disarmed = 0

    def explosion(self, bomb):
        if bomb.countdown != 0: return False
        if self.immunity > 0: return False
        horizontal = (self.pos[Y] == bomb.pos[Y] and self.pos[X] >= bomb.range[DIRECTION_LEFT] and self.pos[X] <= bomb.range[DIRECTION_RIGHT])
        vertical = (self.pos[X] == bomb.pos[X] and self.pos[Y] >= bomb.range[DIRECTION_UP] and self.pos[Y] <= bomb.range[DIRECTION_DOWN])
        if ( horizontal or vertical ):
            self.health -= 10
            self.immunity = IMMUNITY
            print("{}\'s health: {}".format(self.nickname, self.health))
        if self.health <= 0:
            print("{} is dead!".format(self.nickname))
            return True
        return False

### Class Model ###

class Model:

    # initialize model
    def __init__(self):
        self.map = None
        self.characters = []
        self.fruits = []
        self.bombs = []
        self.player = None

    def load(self, map_file):
        self.map = Map(map_file)

    # look for a character, return None if not found
    def look(self, nickname):
        # https://stackoverflow.com/questions/9542738/python-find-in-list
        character = next( (c for c in self.characters if (c.nickname == nickname)), None) # first occurence
        return character

    # kill a character
    def kill(self, nickname):
        character = self.look(nickname)
        if not character:
            print("Error: nickname {} not found!".format(nickname))
            return None
        self.characters.remove(character)
        if self.player == character: self.player = None
        print("{} is killed!".format(nickname))
        return character

    # quit
    def quit(self, nickname):
        cont = True
        if self.player and self.player.nickname == nickname:
            cont = False
        character = self.look(nickname)
        if character: self.kill(nickname)
        return cont

    # join as new character
    def join(self, nickname, isplayer, pos = None):
        character = self.look(nickname)
        if character:
            print("Error: nickname {} already used!".format(nickname))
            return None
        if not pos: pos = self.map.random()
        character = Character(nickname, random.choice(CHARACTERS), self.map, pos)
        print("{} is born!".format(character.nickname))
        self.characters.append(character)
        if isplayer: self.player = character
        return character

    # drop a bomb
    def drop(self, nickname):
        character = self.look(nickname)
        if not character:
            print("Error: nickname {} not found!".format(nickname))
            return
        if character.disarmed == 0:
            self.bombs.append(Bomb(self.map, character.pos))
            character.disarmed = DISARMED

    # move a character
    def move(self, nickname, direction):
        character = self.look(nickname)
        if not character:
            print("Error: nickname {} not found!".format(nickname))
            return
        character.move(direction)

    # add fruit
    def fruit(self, kind, pos):
        self.fruits.append(Fruit(kind, self.map, pos))

    # update model at each clock tick
    def tick(self, dt):
        # update bombs (and remove it)
        for bomb in self.bombs:
            bomb.tick(dt)
            if bomb.countdown == -1:
                self.bombs.remove(bomb)

        # update characters and eat fruits
        for character in self.characters:
            character.tick(dt)
            for fruit in self.fruits:
                if character.eat(fruit):
                    self.fruits.remove(fruit)

        # update characters after bomb explosion
        for bomb in self.bombs:
            for character in self.characters:
                if character.explosion(bomb):
                    self.characters.remove(character)
                    self.player = None
