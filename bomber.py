#!/usr/bin/env python3
# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from model import *
from view import *
from controller import *
import sys
import pygame

### python version ###
print("python version: {}.{}.{}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2]))
print("pygame version: ", pygame.version.ver)

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
model.load(map_file)
for _ in range(10): model.fruit(random.choice(FRUITS), model.map.random())
model.join("me", True)

kb = KeyboardController(model)
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
