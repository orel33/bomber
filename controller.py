# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

import pygame

################################################################################
#                          KEYBOARD CONTROLLER                                 #
################################################################################


### Class KeyboardController ###

class KeyboardController:

    def __init__(self, evm):
        self.evm = evm
        pygame.key.set_repeat(1,200) # repeat keydown events every 200ms

    def tick(self, dt):

        # process all events
        for event in pygame.event.get():
            cont = True
            if event.type == pygame.QUIT:
                cont = self.evm.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                cont = self.evm.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                cont = self.evm.keyboard_press_space()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                cont = self.evm.keyboard_press_arrow(pygame.K_LEFT)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                cont =self.evm.keyboard_press_arrow(pygame.K_RIGHT)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                cont = self.evm.keyboard_press_arrow(pygame.K_UP)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                cont = self.evm.keyboard_press_arrow(pygame.K_DOWN)
            # don't continue?
            if not cont: return False

        return True
