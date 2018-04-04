# -*- coding: Utf-8 -*
# Author: aurelien.esnard@u-bordeaux.fr

from model import *
import socket

# COMMANDES CLIENT -> SERVEUR
#   CONNECTION NICK -> met à jour le model, envoie le model au nouveau client, envoie le nouveau joueur au clients déjà connectés, ajoute le nouveau client à la liste de clients
#   MOVE NICK DIR -> mettre à jour le model
#   BOMB NICK
#   PART NICK -> supprime le client de la liste des connections et supprime le joueur de la liste de joueurs dans le modèle et envoie ce changement aux autres clients
# COMMANDES CLIENT -> SERVEUR
#   ADD FRUIT KIND X Y
#   ADD PLAYER NICK KIND X Y
#   REMOVE PLAYER NICK
#   MAP WIDTH HEIGHT DATA

################################################################################
#                          NETWORK SERVER CONTROLLER                           #
################################################################################


class NetworkServerController:

    def __init__(self, model, port):
        self.model = model
        self.port = port
        self.server = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, 0)
        self.server.bind(("", port))
        self.server.setblocking(False)
        self.clients = []

    def send_fruit(self, client, kind, x, y):
        message = "ADD FRUIT "+str(kind)+" "+str(x)+" "+str(y)
        self.server.sendto(message.encode("utf-8"), client)

    def send_player(self, client, nick, kind, x, y):
        message = "ADD PLAYER "+nick+" "+str(kind)+" "+str(x)+" "+str(y)
        self.server.sendto(message.encode("utf-8"), client)

    def send_model(self, client):
        string_map = ""
        for row in self.model.map.array:
            for c in row:
                string_map = string_map + c
        message = "MAP "+str(self.model.map.width)+" "+str(self.model.map.height)+" "+string_map
        self.server.sendto(message.encode("utf-8"), client)
        for player in self.model.characters: self.send_player(client, player.nickname, player.kind, player.pos[0], player.pos[1])
        for fruit in self.model.fruits: self.send_fruit(client, fruit.kind, fruit.pos[0], fruit.pos[1])
        # TODO: gestion des bombes 

    def parse_data(self, data, client):
        data_decoded = data.decode("utf-8")
        message = data_decoded.split(" ")
        message_length = len(message)

        if (message_length == 2 and message[0] == "CONNECTION"):
            if not client in self.clients:
                new_character = self.model.add_character(message[1], True)
                self.send_model(client)
                for c in self.clients:  send_player(c, new_character.nick, new_character.kind, new_character.pos[0], new_character.pos[1])
                self.clients.append(client)
            else:
                print("Client déjà connecté : "+message[1])

        elif (message_length == 2 and message[0] == "PART"):
            if client in self.clients:
                self.clients.remove(client)
                message_to_clients = "REMOVE PLAYER "+message[1]
                for c in self.clients: self.server.sendto(message_to_clients.encode("utf-8"), c)
    
    def tick(self, dt):
        try:
            (data, client) = self.server.recvfrom(1500)
            self.parse_data(data, client)        
        except BlockingIOError:
            return True
        return True

################################################################################
#                          NETWORK CLIENT CONTROLLER                           #
################################################################################

class NetworkClientController:

    def __init__(self, model, host, port, nickname):
        self.model = model
        self.host = host
        self.port = port
        self.nickname = nickname
        self.client = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, 0)
        self.client.setblocking(False)        
        self.server = (host, port)
        message = "CONNECTION "+nickname
        self.client.sendto(message.encode("utf-8"), self.server)
        

    # keyboard events

    def keyboard_quit(self):
        print("=> event \"quit\"")
        message = "PART "+self.nickname
        self.client.sendto(message.encode("utf-8"), self.server)
        return False

    def keyboard_move_character(self, direction):
        print("=> event \"keyboard move direction\" {}".format(DIRECTIONS_STR[direction]))
        return True

    def keyboard_drop_bomb(self):
        print("=> event \"keyboard drop bomb\"")
        return True

    # time event
    def parse_data(self, data):
        pass


    def tick(self, dt):
        try:
            (data, server) = self.client.recvfrom(1500)
        except BlockingIOError:
            return True
        return True
