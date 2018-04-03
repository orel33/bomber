#!/usr/bin/env python3
# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from model import *
from view import *
from keyboard import *
import sys
import pygame

### python version ###
print("python version: {}.{}.{}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2]))
print("pygame version: ", pygame.version.ver)

################################################################################
#                             EVENT MANAGER                                    #
################################################################################

### Class EventManager ###

class EventManager:

    def __init__(self, model):
        self.model = model

    def keyboard_quit(self):
        print("=> event \"quit\"")
        return False

    def keyboard_move_character(self, direction):
        print("=> event \"keyboard move direction\" {}".format(DIRECTIONS_STR[direction]))
        if not self.model.player: return True
        nickname = self.model.player.nickname
        if direction in DIRECTIONS:
            self.model.move_character(nickname, direction)
        return True

    def keyboard_drop_bomb(self):
        print("=> event \"keyboard drop bomb\"")
        if not self.model.player: return True
        nickname = self.model.player.nickname
        self.model.drop_bomb(nickname)
        return True

################################################################################
#                                 MAIN                                         #
################################################################################

# parse arguments
map_file = DEFAULT_MAP
if len(sys.argv) == 2:
    map_file = sys.argv[1]

# initialization
pygame.display.init()
pygame.font.init()
clock = pygame.time.Clock()
model = Model()
model.load_map(map_file)
for _ in range(10): model.add_fruit()
model.add_character("me", isplayer = True)
evm = EventManager(model)
kb = KeyboardController(evm)
view = GraphicView(model)

# main loop
while True:
    # make sure game doesn't run at more than FPS frames per second
    dt = clock.tick(FPS)
    if not kb.tick(dt): break
    model.tick(dt)
    view.tick(dt)

# quit
print("Game Over!")
pygame.quit()
