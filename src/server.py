import socket
from threading import Thread
from user import User
from channel import Channel

class Server:

    def __init__(self, host, port):
        self.port = port
        self.host = host
        self.channels = {
            "Canal Teste1": Channel("Canal Teste1"),
            "Canal Teste2": Channel("Cannal Teste2")
        }
        self.users = {}
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpSocket.bind((host, port))
    
    def connect(self):
        self.tcpSocket.listen(1)

    def accept_connection(self):
        connection, address = self.tcpSocket.accept()
        
        name = connection.recv(1024)
        print(name)
        user = User(connection = connection, host = address[0], port = address[1], clientName = name, nick="Teste")
        self.users[user.nick] = user
        thread = Thread(target=self.__runTime, args=(
            connection, address, user.nick))
        thread.start()
            

    def __runTime(self, connection: socket.socket, address, nickName):
        while True:
            message = connection.recv(1024)
            if not message:
                break
            print(message.decode())

            if message.decode() == "users":
                print(self.users.keys())

            self.users.pop(nickName)

        connection.close()
        print('Conexão cliente finalizada', address)

server = Server("127.0.0.1", 6500)
server.connect()
server.accept_connection()
server.accept_connection()