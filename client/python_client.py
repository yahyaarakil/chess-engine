import socket

ADDRESS = "localhost"
PORT = 5000

class Client:
    def __init__(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.connect((ADDRESS, PORT))

        server_message = self.my_socket.recv(1024).decode()
        while server_message != "terminate":
            print(server_message)
            self.my_socket.send((input("CLIENT >>> ")).encode())
            server_message = self.my_socket.recv(1024).decode()
            # client body procedure end
            tokens = server_message.split(';')
            if tokens[0] == 'welcome':
                self.time = int(tokens[-1])
                self.color = tokens[-2]
                self.in_game()
        print(server_message)
        self.my_socket.close()

    def in_game(self):
        server_message = self.my_socket.recv(1024).decode()
        print(server_message)
        if self.color == "white":
            self.my_socket.send(input("x, y: "))
            while True:
                

if __name__ == "__main__":
    client = Client()