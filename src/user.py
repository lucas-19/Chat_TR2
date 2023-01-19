from __future__ import annotations
import uuid

class User:

    def __init__(self, host, port, connection, clientName, nick):
        self.host = host
        self.port = port
        self.currentChannel = None
        self.id = uuid.uuid4()
        self.connection = connection
        self.clientName = clientName
        self.nick = nick

    def getUser(self):
        return f"{self.nick} {self.host} {self.clientName}"
    

    def setCurrentChannel(self, channelName: str):
        self.currentChannel = channelName
    
    def quitCurrentChannel(self):
        self.currentChannel = None