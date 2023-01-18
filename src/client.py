# Cliente TCP
import socket
from threading import Thread

class Client:
    # Realiza conexão com o servidor.

    def __init__(self, host, port, name, nick) -> None:
        self.host = host
        self.port = port
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name
        self.running = False
        self.nick = nick
        self.connect()

    
    def connect(self):
        self.running = True
        self.tcpSocket.connect((self.host, self.port))
        nameNick = self.name + "-" + self.nick
        self.sendMessage(nameNick.encode())

        threadRMessage = Thread(target=self.reception)
        threadSMessage = Thread(target=self.send)
        threadRMessage.start()
        threadSMessage.start()

    
    def sendMessage(self, message):
        self.tcpSocket.send(message)

    def send(self):
        while self.running:
            message = input()
            self.sendMessage(message.encode())
            if message == "\x18" or message == "QUIT":
                self.closeConnection() # olhar com calma
                self.running = False


    def receiveMessage(self):
        return self.tcpSocket.recv(1024).decode()
    
    def reception(self):
        while self.running:
            message = self.receiveMessage()
            print(message)
    
    def closeConnection(self):
        self.running = False
        self.tcpSocket.close()

client = Client("127.0.0.1", 6500, "Lucas", "luckboy13")
# client.connect()
