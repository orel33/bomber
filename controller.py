# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from model import *
import pygame

################################################################################
#                          KEYBOARD CONTROLLER                                 #
################################################################################

### Class KeyboardController ###

class KeyboardController:

    def __init__(self, model):
        self.model = model
        pygame.key.set_repeat(1,200) # repeat keydown events every 200ms

    def tick(self, dt):
        # process all events
        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            # player interaction
            elif self.model.player and event.type == pygame.KEYDOWN:
                nickname = self.model.player.nickname
                # drop bomb
                if  event.key == pygame.K_SPACE:
                    self.model.drop(nickname)
                # move
                elif event.key == pygame.K_RIGHT:
                    self.model.move(nickname, DIRECTION_RIGHT)
                elif event.key == pygame.K_LEFT:
                    self.model.move(nickname, DIRECTION_LEFT)
                elif event.key == pygame.K_UP:
                    self.model.move(nickname, DIRECTION_UP)
                elif event.key == pygame.K_DOWN:
                    self.model.move(nickname, DIRECTION_DOWN)

        return True
