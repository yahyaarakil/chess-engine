import threading
import socket
import player
import time
import instance

class Sublet(threading.Thread):
    queue = []

    def __init__(self, player, parent):
        threading.Thread.__init__(self)
        self.player = player
        self.in_game = False
        self.parent = parent

    def run(self):
        self.player.connection.send("CONNECTED".encode())
        mode = int(self.player.connection.recv(1024).decode())
        if mode == 0:
            if len(Sublet.queue)%2 == 0:
                Sublet.queue.append(self)
                while(not self.in_game):
                    time.sleep(1)

            elif len(Sublet.queue)%2 == 1:
                player2 = Sublet.queue.pop(0)
                player2.in_game = True
                self.in_game = True
                game = instance.Chess_instance(self.player, player2.player)
                self.parent.games.append(game)
                game.start()
                del player2
                del self