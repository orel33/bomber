# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from model import *

################################################################################
#                         EVENT MANAGER SERVER                                 #
################################################################################

### Class EventManagerServer ###

class EventManagerServer:

    def __init__(self, model):
        self.model = model

    # network events
    # ...

################################################################################
#                          NETWORK SERVER CONTROLLER                           #
################################################################################

class NetworkServerController:

    def __init__(self, evm, port):
        self.evm = evm
        self.port = port
        # ...

    def tick(self, dt):
        # ...
        return True

################################################################################
#                         EVENT MANAGER CLIENT                                 #
################################################################################

### Class EventManagerClient ###

class EventManagerClient:

    def __init__(self, model):
        self.model = model

    def quit(self):
        print("=> event \"quit")
        # ...
        return False

    # keyboard events
    def keyboard_press_arrow(self, key):
        print("=> event \"keyboard press arrow\"")
        # ...
        return True

    def keyboard_press_space(self):
        print("=> event \"keyboard press space\"")
        # ...
        return True

    # network events
    # ...

################################################################################
#                          NETWORK CLIENT CONTROLLER                           #
################################################################################

class NetworkClientController:

    def __init__(self, evm, host, port, nickname):
        self.evm = evm
        self.host = host
        self.port = port
        self.nickname = nickname
        # ...

    def tick(self, dt):
        # ...
        return True
