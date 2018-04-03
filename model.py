# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

import random
import sys

################################################################################
#                                  MODEL                                       #
################################################################################

### Constants ###

# position / direction
X = 0
Y = 1
DIRECTION_LEFT = 0
DIRECTION_RIGHT = 1
DIRECTION_UP = 2
DIRECTION_DOWN = 3
DIRECTIONS = [DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_UP, DIRECTION_DOWN]
DIRECTIONS_STR = ["left", "right", "up", "down"]

# map
WALLS = ('w', 'x', 'z')
BACKGROUNDS = ('0', '1', '2')
DEFAULT_MAP = "maps/map0"

# fruit
BANANA = 0
CHERRY = 1
FRUITS = [BANANA, CHERRY]
FRUITS_STR = ["banana", "cherry"]

# character
DK = 0
ZELDA = 1
BATMAN = 2
CHARACTERS = [DK, ZELDA, BATMAN]
CHARACTERS_STR = ["dk", "zelda", "batman"]
HEALTH = 50
MAX_RANGE = 5
COUNTDOWN = 5
IMMUNITY = 1500 # in ms
DISARMED = 2000 # in ms

### Class Map ###

class Map:
    def __init__(self):
        self.array = []
        self.width = 0
        self.height = 0

    def load(self, filename):
        with open(filename, "r") as _file:
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
        self.map = Map()
        self.characters = []
        self.fruits = []
        self.bombs = []
        self.player = None

    # look for a character, return None if not found
    def look(self, nickname):
        # https://stackoverflow.com/questions/9542738/python-find-in-list
        character = next( (c for c in self.characters if (c.nickname == nickname)), None) # first occurence
        return character

    # load map from file
    def load_map(self, filename):
        self.map.load(filename)
        print("=> load map \"{}\" of size {}x{}".format(filename, self.map.width, self.map.height))

    # kill a character
    def kill_character(self, nickname):
        character = self.look(nickname)
        if not character:
            print("Error: nickname {} not found!".format(nickname))
            sys.exit(1)
        self.characters.remove(character)
        if self.player == character: self.player = None
        print("=> kill \"{}\"".format(nickname))
        return character

    # quit game
    def quit(self, nickname = None):
        cont = True
        if self.player and self.player.nickname == nickname:
            cont = False
        character = self.look(nickname)
        if character: self.kill_character(nickname)
        print("=> quit \"{}\"".format(nickname))
        return cont

    # add a new fruit
    def add_fruit(self, kind = None, pos = None):
        if pos is None: pos = self.map.random()
        if kind is None: kind = random.choice(FRUITS)
        self.fruits.append(Fruit(kind, self.map, pos))
        print("=> add fruit ({}) at position ({},{})".format(FRUITS_STR[kind], pos[X], pos[Y]))

    # add a new character
    def add_character(self, nickname, isplayer = False, kind = None, pos = None):
        character = self.look(nickname)
        if character:
            print("Error: nickname \"{}\" already used!".format(nickname))
            sys.exit(1)
        if pos is None: pos = self.map.random()
        if kind is None: kind = random.choice(CHARACTERS)
        character = Character(nickname, kind, self.map, pos)
        print("=> add character \"{}\" ({}) as position ({},{})".format(nickname, CHARACTERS_STR[kind], pos[X], pos[Y]))
        self.characters.append(character)
        if isplayer: self.player = character
        return character

    # drop a bomb
    def drop_bomb(self, nickname):
        character = self.look(nickname)
        if not character:
            print("Error: nickname \"{}\" not found!".format(nickname))
            sys.exit(1)
        if character.disarmed == 0:
            self.bombs.append(Bomb(self.map, character.pos))
            character.disarmed = DISARMED
        print("=> drop bomb at position ({},{})".format(character.pos[X], character.pos[Y]))

    # move a character
    def move_character(self, nickname, direction):
        character = self.look(nickname)
        if not character:
            print("Error: nickname \"{}\" not found!".format(nickname))
            sys.exit(1)
        character.move(direction)
        print("=> move {} \"{}\" at position ({},{})".format(DIRECTIONS_STR[direction], nickname, character.pos[X], character.pos[Y]))

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
