# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from model import *
import pygame

################################################################################
#                                 VIEW                                         #
################################################################################

### Constants ###

FPS = 30
WIN_TITLE = "Bomber Man"
SPRITE_SIZE = 30 # 30x30 pixels
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

### Sprites ###

SPRITE_BACKGROUNDS = [ "images/misc/bg0.png", "images/misc/bg1.png", "images/misc/bg2.png" ]
SPRITE_BLANK = "images/misc/blank.png"
SPRITE_WALLS = [ "images/misc/wall0.png", "images/misc/wall1.png", "images/misc/wall2.png" ]
SPRITE_BOMB = "images/misc/bomb.png"
SPRITE_FIRE = "images/misc/fire.png"
SPRITE_FRUITS = [ "images/misc/banana.png", "images/misc/cherry.png" ]
SPRITE_DK = [ "images/dk/left.png", "images/dk/right.png", "images/dk/up.png", "images/dk/down.png" ]
SPRITE_ZELDA = [ "images/zelda/left.png", "images/zelda/right.png", "images/zelda/up.png", "images/zelda/down.png" ]
SPRITE_BATMAN = [ "images/batman/left.png", "images/batman/right.png", "images/batman/up.png", "images/batman/down.png" ]

### Class PyGameView ###

class GraphicView:

    # initialize PyGame graphic view
    def __init__(self, model, playername = ""):
        self.model = model
        self.width = model.map.width*SPRITE_SIZE
        self.height = model.map.height*SPRITE_SIZE
        # create window
        self.win = pygame.display.set_mode((self.width, self.height))
        # load sprites
        self.sprite_walls = [ pygame.image.load(sprite).convert() for sprite in SPRITE_WALLS ]
        self.sprite_backgrounds = [ pygame.image.load(sprite).convert() for sprite in SPRITE_BACKGROUNDS ]
        self.sprite_blank = pygame.image.load(SPRITE_BLANK).convert()
        self.sprite_fruits = [ pygame.image.load(sprite).convert_alpha() for sprite in SPRITE_FRUITS ]
        self.sprite_bomb = pygame.image.load(SPRITE_BOMB).convert_alpha()
        self.sprite_fire = pygame.image.load(SPRITE_FIRE).convert_alpha()
        sprite_dk = [ pygame.image.load(sprite).convert_alpha() for sprite in SPRITE_DK ]
        sprite_zelda = [ pygame.image.load(sprite).convert_alpha() for sprite in SPRITE_ZELDA ]
        sprite_batman = [ pygame.image.load(sprite).convert_alpha() for sprite in SPRITE_BATMAN ]
        self.sprite_characters = [sprite_dk, sprite_zelda, sprite_batman]
        # init view
        pygame.display.set_icon(self.sprite_bomb)
        title = WIN_TITLE
        if playername: title = WIN_TITLE + " (" + playername + ")"
        pygame.display.set_caption(title)
        self.font = pygame.font.SysFont('Consolas', 20)

    # render map view
    def render_map(self, m):
        # win.blit(self.background, (0, 0))
        for y in range(0, m.height):
            for x in range(0, m.width):
                square = m.array[y][x]
                x0 = x*SPRITE_SIZE
                y0 = y*SPRITE_SIZE
                # walls
                if square == 'w':
                    self.win.blit(self.sprite_walls[0], (x0, y0))
                elif square == 'x':
                    self.win.blit(self.sprite_walls[1], (x0, y0))
                elif square == 'z':
                    self.win.blit(self.sprite_walls[2], (x0, y0))
                # backgrounds
                elif square == '0':
                    self.win.blit(self.sprite_backgrounds[0], (x0, y0))
                elif square == '1':
                    self.win.blit(self.sprite_backgrounds[1], (x0, y0))
                elif square == '2':
                    self.win.blit(self.sprite_backgrounds[2], (x0, y0))
                else:
                    self.win.blit(self.sprite_blank, (x0, y0)) # blank

    # render fruit view
    def render_fruit(self, fruit):
        x = fruit.pos[X] * SPRITE_SIZE
        y = fruit.pos[Y] * SPRITE_SIZE
        self.win.blit(self.sprite_fruits[fruit.kind], (x, y))

    def render_bomb_explosion(self, bomb):
        x0 = bomb.pos[X]
        y0 = bomb.pos[Y]
        for x in range(bomb.range[DIRECTION_LEFT], bomb.range[DIRECTION_RIGHT]+1):
            self.win.blit(self.sprite_fire, (x*SPRITE_SIZE, y0*SPRITE_SIZE))
        for y in range(bomb.range[DIRECTION_UP], bomb.range[DIRECTION_DOWN]+1):
            self.win.blit(self.sprite_fire, (x0*SPRITE_SIZE, y*SPRITE_SIZE))

    def render_bomb_drop(self, bomb):
        x = bomb.pos[X] * SPRITE_SIZE
        y = bomb.pos[Y] * SPRITE_SIZE
        self.win.blit(self.sprite_bomb, (x, y))
        x0 = x + SPRITE_SIZE/2
        y0 = y + SPRITE_SIZE/2
        text = self.font.render(str(bomb.countdown), True, YELLOW)
        rect = text.get_rect(center=(x0-5,y0+5))
        self.win.blit(text, rect)

    def render_bomb(self, bomb):
        if(bomb.countdown == 0):
            self.render_bomb_explosion(bomb)
        elif(bomb.countdown > 0):
            self.render_bomb_drop(bomb)

    def render_character(self, character):
        x = character.pos[X] * SPRITE_SIZE
        y = character.pos[Y] * SPRITE_SIZE
        sprite = self.sprite_characters[character.kind][character.direction]
        self.win.blit(sprite, (x, y))

    def render_player(self, player):
        if not player: return
        x = player.pos[X] * SPRITE_SIZE
        y = player.pos[Y] * SPRITE_SIZE
        pygame.draw.rect(self.win, RED, (x, y, SPRITE_SIZE, SPRITE_SIZE), 1)

    # render PyGame graphic view at each clock tick
    def tick(self, dt):
        self.render_map(self.model.map)
        for bomb in self.model.bombs:
            self.render_bomb(bomb)
        for fruit in self.model.fruits:
            self.render_fruit(fruit)
        for character in self.model.characters:
            self.render_character(character)
        self.render_player(self.model.player)
        pygame.display.flip()
