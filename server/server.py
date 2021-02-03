import threading
import socket
import player
import sublet
import instance
        
ADDRESS = "localhost"
PORT = 5000

class Entry_point:
    def __init__(self):
        #creating socket
        self.main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.games = []
        self.players = []

        #binding socket
        print(">Binding socket")
        try:
            self.main_socket.bind((ADDRESS, PORT))
            print(">Socket bound successfully")
        except Exception:
            print("Cannot bind socket")
            exit(1)

        #starting server
        print(">Server started\n>Listening for connections")
        while True:
            self.main_socket.listen()
            connection, address = self.main_socket.accept()
            new_player = player.Player(connection, address, "name")
            worker = sublet.Sublet(new_player, self)
            worker.start()
            self.players.append(new_player)

if __name__ == "__main__":
    entry = Entry_point()