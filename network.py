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
        self.server = None

    def setNetworkServerController(self, server):
        self.server = server

    # network events
    # ...

################################################################################
#                          NETWORK SERVER CONTROLLER                           #
################################################################################

class NetworkServerController:

    def __init__(self, model, evm, port):
        self.model = model
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
        self.client = None

    def setNetworkClientController(self, client):
        self.client = client

    # keyboard events
    def quit(self):
        print("=> event \"quit\"")
        return False

    def keyboard_move_character(self, direction):
        print("=> event \"keyboard move direction\" {}".format(DIRECTIONS_STR[direction]))
        # ...
        return True

    def keyboard_drop_bomb(self):
        print("=> event \"keyboard drop bomb\"")
        # ...
        return True

    # network events
    # ...

################################################################################
#                          NETWORK CLIENT CONTROLLER                           #
################################################################################

class NetworkClientController:

    def __init__(self, model, evm, host, port, nickname):
        self.model = model
        self.evm = evm
        self.host = host
        self.port = port
        self.nickname = nickname
        # ...

    def tick(self, dt):
        # ...
        return True
