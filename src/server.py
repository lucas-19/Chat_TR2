import socket
from threading import Thread
from user import User
from channel import Channel

class Server:

    def __init__(self, host, port):
        self.port = port
        self.host = host
        self.channels = {
            "CanalTeste1": Channel("CanalTeste1"),
            "CanalTeste2": Channel("CannalTeste2")
        }
        self.users: dict[str, User] = {}
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpSocket.bind((host, port))
    
    def connect(self):
        self.tcpSocket.listen(1)

    def acceptConnection(self):
        connection, address = self.tcpSocket.accept()
        
        nameNick = connection.recv(1024).decode()
        name = nameNick.split("-")[0]
        nick = nameNick.split("-")[1]
        print("Nome: ",name, nick)
        user = User(connection = connection, host = address[0], port = address[1], clientName = name, nick=nick)
        self.users[user.nick] = user

        connection.send(b"Conectado")

        thread = Thread(target=self.__runTime, args=(
            connection, address, user.nick))
        thread.start()
            

    def __runTime(self, connection: socket.socket, address, nick: str):
        while True:
            message = connection.recv(1024)
            if not message:
                break
            
            command = message.decode().split()[0]
            
            
            if command == "JOIN":
                channel = message.decode().split()[1]
                response = self.join(channel, self.users[nick])
            elif command == "PART":
                print("comando PART")
                channel = message.decode().split()[1]
                response = self.part(channel, self.users[nick])
            elif command == "LIST":
                response = self.listChannels()
            elif command == "USER":
                nickNew = message.decode().split()[1]
                users = list(self.users.keys())
                users.append(nickNew)
                self.users = users
                response = "O usuario " + nickNew + " foi criado"
            elif command == "QUIT":
                connection.close()
                print('Conexão cliente finalizada', address)
                break
            elif command == "NICK":
                newNick = message.decode().split()[1]
                users = list(self.users.keys())
                if newNick in users:
                    response = "Esse Nick ja foi escolhido"
                else:
                    self.users[newNick] = self.users.pop(nick)
                    nick = newNick
                    response = "O seu novo nick eh " + self.users[newNick].nick
            else:
                print("ERR UNKNOWNCOMMAND")


            connection.send(response.encode())

        connection.close()
        print('Conexão cliente finalizada', address)


    
    def join(self, channelName: str, user: User):
        if channelName not in self.channels.keys():
            return "Nome de canal invalido"

        userCurrentChannel = self.users[user.nick].currentChannel
        
        if userCurrentChannel != None:
            self.part(user=user, channelName=userCurrentChannel)
        
        self.channels[channelName].addUser(user)
        self.users[user.nick].setCurrentChannel(channelName)

        return "Juntou-se ao " + channelName

    def part(self, channelName: str, user: User):
        if channelName not in self.channels.keys():
            return "Canal invalido"
        if user.nick not in list(self.channels[channelName].users.keys()):
            return "O usuario nao faz parte desse canal"

        self.channels[channelName].removeUser(user.nick)
        self.users[user.nick].quitCurrentChannel()
        
        return "Retirado do " + channelName

    def listChannels(self):
        channelsList = []
        for channelName, channel in self.channels.items():
            channelsList.append(f"{channelName} - {len(list(channel.users.keys()))}")

        return "Lista de Canais: \n" + "\n".join(channelsList)

server = Server("127.0.0.1", 4002)
server.connect()
server.acceptConnection()
server.acceptConnection()