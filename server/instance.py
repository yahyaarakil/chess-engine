import threading
import socket
import sys
sys.path.append("../core/")
sys.path.append("../client/")
from board_patterns import *
from board import *
import random
import debug

class Chess_instance(threading.Thread):
    def __init__(self, player1, player2, board_pattern = "default", player_pattern = "wb"):
        threading.Thread.__init__(self)
        self.board = debug.BoardDebug(board_pattern)
        self.player1 = player1
        self.player2 = player2
        self.active_player = player1
        if player_pattern == "wb":
            self.player1.player = "white"
            self.player2.player = "black"
        else:
            self.player1.player = "black"
            self.player2.player = "white"
        self.player1.time = 5*1000*60
        self.player2.time = 5*1000*60

    def switch_player(self):
        if self.active_player == self.player1:
            self.active_player = self.player2
        else:
            self.active_player = self.player1

    def run(self):
        welcome_string = "welcome;"
        for row in self.board.tiles:
            for tile in row:
                if tile.piece_slot != None:
                    welcome_string += "{},{},{},{},{},(".format(tile.piece_slot.piece_name,
                    tile.piece_slot.owner,
                    tile.pos[0],
                    tile.pos[1],
                    tile.piece_slot.identifier)
                    for move in tile.piece_slot.move + tile.piece_slot.attack:
                        welcome_string += str(move.pos[0])+","+str(move.pos[1])+";"
                    welcome_string += ");"
        print("Welcome string size:", len(welcome_string.encode()))
        self.player1.connection.send((welcome_string+self.player1.player+";"+str(self.player1.time)).encode())
        self.player2.connection.send((welcome_string+self.player2.player+";"+str(self.player2.time)).encode())

        while True:
            los_con = self.board.check_loss(self.active_player.player)
            if los_con == "loss":
                self.active_player.connection.send("loss".encode())
                self.switch_player()
                self.active_player.connection.send("win".encode())
                break
            elif los_con == "stalemate":
                self.active_player.connection.send("stalemate".encode())
                self.switch_player()
                self.active_player.connection.send("stalemate".encode())
                break
            else:
                self.active_player.connection.send("play".encode())
            player_message = self.active_player.connection.recv(1024).decode().split(',')
            changed = self.board.move(self.board.tiles[player_message[1]][player_message[0]],
            self.board.tiles[player_message[3]][player_message[2]], player_message[4])
            response = "{},{},{},{};".format(player_message[0], player_message[1], player_message[2], player_message[3])
            for tile in changed:
                if tile.piece_slot != None:
                    response += "{},(".format(tile.piece_slot.identifier)
                    for move in tile.piece_slot.move + tile.piece_slot.attack:
                        response += str(move.pos[0])+","+str(move.pos[1])+";"
                    response += ");"
            self.active_player.connection.send(response.encode())
            self.switch_player()
            self.active_player.connection.send(response.encode())